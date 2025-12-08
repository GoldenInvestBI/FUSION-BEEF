#!/usr/bin/env python3
"""
Minerva Products Scraper with Advanced Anti-Detection
Automatically scrapes ALL products from ALL categories in the Minerva portal
"""

import os
import sys
import json
import time
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import mysql.connector
from pathlib import Path
from urllib.parse import urlparse
from notifications import NotificationService

# Configuration
MINERVA_URL = "https://meuminerva.com/"
CNPJ = "55298629000151"
PASSWORD = "Borgh$2024#$$"
MARKUP_PERCENT = 60.0
IMAGE_DIR = Path("/home/ubuntu/fusion_beef_portfolio/client/public/images/products")

# Parse DATABASE_URL from environment
def get_db_config():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        raise Exception("DATABASE_URL not set")
    
    # Parse mysql://user:pass@host:port/dbname?ssl=...
    parsed = urlparse(db_url)
    db_name = parsed.path.lstrip("/").split("?")[0]
    
    config = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": db_name,
    }
    
    # Add SSL configuration for TiDB
    if "tidbcloud.com" in parsed.hostname:
        config["ssl_disabled"] = False
    
    return config

# Categories to scrape (all main menus)
CATEGORIES = [
    "Azeite",
    "Bovinos",
    "Bovinos Premium",
    "Cordeiros",
    "Empanados",
    "Vegetais",
    "Jerked Beef",
    "Pescados",
    "Suínos",
    "Combos",
    "Promoções",
]

class MinervaScraper:
    def __init__(self):
        self.driver = None
        self.db = None
        self.cursor = None
        self.log_id = None
        self.notification_service = NotificationService()
        self.stats = {
            "found": 0,
            "added": 0,
            "updated": 0,
            "removed": 0,
        }
        self.out_of_stock_products = []
        self.price_changes = []
        
    def random_delay(self, min_sec=1, max_sec=3):
        """Add random human-like delay"""
        time.sleep(random.uniform(min_sec, max_sec))
        
    def human_type(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def setup_driver(self):
        """Initialize Selenium WebDriver with advanced stealth"""
        chrome_options = Options()
        
        # Stealth mode
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        
        # Realistic User-Agent
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Additional preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Execute stealth scripts
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });
                window.chrome = {
                    runtime: {}
                };
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({state: 'granted'})
                    })
                });
            """
        })
        
        print("✅ WebDriver initialized with stealth mode")
        
    def connect_db(self):
        """Connect to MySQL database"""
        try:
            db_config = get_db_config()
            self.db = mysql.connector.connect(**db_config)
            self.cursor = self.db.cursor(dictionary=True)
            print("✅ Connected to database")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            sys.exit(1)
            
    def start_log(self):
        """Create a new scrape log entry"""
        query = """
        INSERT INTO scrape_logs (status, startedAt, createdAt)
        VALUES ('running', %s, %s)
        """
        now = datetime.now()
        self.cursor.execute(query, (now, now))
        self.db.commit()
        self.log_id = self.cursor.lastrowid
        print(f"📝 Started scrape log #{self.log_id}")
        
    def update_log(self, status, error_message=None):
        """Update scrape log with final status"""
        query = """
        UPDATE scrape_logs 
        SET status = %s, 
            productsFound = %s,
            productsAdded = %s,
            productsUpdated = %s,
            productsRemoved = %s,
            errorMessage = %s,
            completedAt = %s
        WHERE id = %s
        """
        now = datetime.now()
        self.cursor.execute(query, (
            status,
            self.stats["found"],
            self.stats["added"],
            self.stats["updated"],
            self.stats["removed"],
            error_message,
            now,
            self.log_id
        ))
        self.db.commit()
        
    def login(self):
        """Login to Minerva portal with human-like behavior"""
        print("🔐 Logging in to Minerva...")
        
        try:
            # Navigate to homepage
            self.driver.get(MINERVA_URL)
            self.random_delay(3, 5)
            
            # Take screenshot for debugging
            self.driver.save_screenshot("/tmp/minerva_homepage.png")
            print("📸 Screenshot saved: /tmp/minerva_homepage.png")
            
            # Accept cookies if present
            try:
                accept_cookies = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Aceitar')]")
                accept_cookies.click()
                print("✅ Cookies accepted")
                self.random_delay(1, 2)
            except:
                print("ℹ️  No cookie banner found")
            
            # Select region if present
            try:
                # Try to find region selection (Região Sul or Nordeste/Centro-Oeste/Sudeste)
                region_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'region') or contains(text(), 'Região')]")
                if not region_buttons:
                    # Try alternative selector
                    region_buttons = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Região')]//parent::button")
                
                if region_buttons:
                    # Click first region (Nordeste/Centro-Oeste/Sudeste)
                    region_buttons[0].click()
                    print("✅ Region selected")
                    self.random_delay(2, 3)
                    self.driver.save_screenshot("/tmp/minerva_after_region.png")
                else:
                    print("ℹ️  No region selection found")
            except Exception as e:
                print(f"⚠️  Could not select region: {e}")
            
            # Scroll a bit (human behavior)
            self.driver.execute_script("window.scrollTo(0, 300);")
            self.random_delay(1, 2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.random_delay(1, 2)
            
            # Find and click login button using JavaScript
            try:
                # Try multiple selectors
                login_btn = None
                selectors = [
                    "//button[contains(text(), 'Faça seu login')]",
                    "//a[contains(text(), 'Faça seu login')]",
                    "//button[contains(@class, 'login')]",
                    "//a[contains(@class, 'login')]",
                    "//a[@title='Faça seu login']",
                    "//button[@title='Faça seu login']",
                ]
                
                for selector in selectors:
                    try:
                        login_btn = self.driver.find_element(By.XPATH, selector)
                        if login_btn:
                            print(f"✅ Found login button with selector: {selector}")
                            break
                    except:
                        continue
                
                if not login_btn:
                    print("❌ Could not find login button")
                    print("Page source:", self.driver.page_source[:500])
                    return False
                
                # Click using JavaScript to bypass visibility issues
                self.driver.execute_script("arguments[0].click();", login_btn)
                print("✅ Clicked login button via JavaScript")
                self.random_delay(2, 3)
                
                self.driver.save_screenshot("/tmp/minerva_login_form.png")
                print("📸 Screenshot saved: /tmp/minerva_login_form.png")
                
            except Exception as e:
                print(f"❌ Error clicking login button: {e}")
                return False
            
            # Enter CNPJ
            try:
                cnpj_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                cnpj_input.click()
                self.random_delay(0.5, 1)
                self.human_type(cnpj_input, CNPJ)
                self.random_delay(1, 2)
                
                print("✅ CNPJ entered")
                
            except Exception as e:
                print(f"❌ Error entering CNPJ: {e}")
                return False
            
            # Click advance button
            try:
                advance_btn = self.driver.find_element(By.ID, "send2")
                advance_btn.click()
                self.random_delay(2, 3)
                
                self.driver.save_screenshot("/tmp/minerva_password_form.png")
                print("📸 Screenshot saved: /tmp/minerva_password_form.png")
                
            except Exception as e:
                print(f"❌ Error clicking advance: {e}")
                return False
            
            # Enter password
            try:
                pass_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "pass"))
                )
                pass_input.click()
                self.random_delay(0.5, 1)
                self.human_type(pass_input, PASSWORD)
                self.random_delay(1, 2)
                
                print("✅ Password entered")
                
            except Exception as e:
                print(f"❌ Error entering password: {e}")
                return False
            
            # Click final advance
            try:
                final_btn = self.driver.find_element(By.ID, "send2")
                final_btn.click()
                self.random_delay(5, 7)
                
                self.driver.save_screenshot("/tmp/minerva_logged_in.png")
                print("📸 Screenshot saved: /tmp/minerva_logged_in.png")
                
                # Check if login was successful
                current_url = self.driver.current_url
                if "customer/account" in current_url or "dashboard" in current_url:
                    print("✅ Login successful")
                    return True
                else:
                    print(f"⚠️  Login may have failed. Current URL: {current_url}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error completing login: {e}")
                return False
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def scrape_category(self, category_name):
        """Scrape all products from a specific category"""
        print(f"\n📂 Scraping category: {category_name}")
        
        try:
            # Find and click category menu
            category_link = self.driver.find_element(
                By.XPATH, 
                f"//a[contains(text(), '{category_name}')]"
            )
            category_url = category_link.get_attribute("href")
            
            # Human-like navigation
            actions = ActionChains(self.driver)
            actions.move_to_element(category_link).perform()
            self.random_delay(0.5, 1)
            
            self.driver.get(category_url)
            self.random_delay(3, 5)
            
            products = []
            page = 1
            
            while True:
                print(f"  📄 Page {page}...")
                
                # Scroll to load lazy images
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(2, 3)
                self.driver.execute_script("window.scrollTo(0, 0);")
                self.random_delay(1, 2)
                
                # Extract products from current page
                product_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    ".product-item"
                )
                
                if not product_elements:
                    print(f"  ℹ️  No products found on page {page}")
                    break
                    
                for elem in product_elements:
                    try:
                        # Check if in stock (has "RESFRIADO" or "CONGELADO" badge)
                        stock_badges = elem.find_elements(By.CSS_SELECTOR, ".product-badge")
                        in_stock = any("RESFRIADO" in b.text or "CONGELADO" in b.text for b in stock_badges)
                        
                        if not in_stock:
                            continue
                            
                        # Extract product data
                        sku_elem = elem.find_element(By.CSS_SELECTOR, ".product-sku")
                        sku = sku_elem.text.replace("SKU:", "").strip()
                        
                        name_elem = elem.find_element(By.CSS_SELECTOR, ".product-item-link")
                        name = name_elem.text.strip()
                        
                        price_elem = elem.find_element(By.CSS_SELECTOR, ".price")
                        price_text = price_elem.text.replace("R$", "").replace(",", ".").strip()
                        price_original = float(price_text.split("/")[0])
                        
                        img_elem = elem.find_element(By.CSS_SELECTOR, ".product-image-photo")
                        image_url = img_elem.get_attribute("src")
                        
                        product_url = name_elem.get_attribute("href")
                        
                        stock_status = next((b.text for b in stock_badges if "RESFRIADO" in b.text or "CONGELADO" in b.text), "")
                        
                        # Calculate price with markup
                        price_with_markup = round(price_original * (1 + MARKUP_PERCENT / 100), 2)
                        
                        product = {
                            "sku": sku,
                            "name": name,
                            "category": category_name,
                            "priceOriginal": str(price_original),
                            "priceWithMarkup": str(price_with_markup),
                            "markup": str(MARKUP_PERCENT),
                            "imageUrl": image_url,
                            "stockStatus": stock_status,
                            "minervaUrl": product_url,
                            "inStock": 1,
                        }
                        
                        products.append(product)
                        self.stats["found"] += 1
                        
                    except Exception as e:
                        print(f"    ⚠️  Error extracting product: {e}")
                        continue
                        
                # Check for next page
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, ".action.next")
                    if "disabled" in next_btn.get_attribute("class"):
                        break
                    
                    # Human-like pagination
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.random_delay(1, 2)
                    next_btn.click()
                    self.random_delay(3, 5)
                    page += 1
                except NoSuchElementException:
                    break
                    
            print(f"  ✅ Found {len(products)} products in {category_name}")
            return products
            
        except Exception as e:
            print(f"  ❌ Error scraping category {category_name}: {e}")
            return []
            
    def download_image(self, image_url, sku):
        """Download product image"""
        try:
            # Remove size parameters to get original quality
            clean_url = image_url.split("?")[0]
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": MINERVA_URL,
            }
            
            response = requests.get(clean_url, headers=headers, timeout=30)
            if response.status_code == 200:
                IMAGE_DIR.mkdir(parents=True, exist_ok=True)
                
                ext = clean_url.split(".")[-1]
                filename = f"{sku}.{ext}"
                filepath = IMAGE_DIR / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                    
                return f"/images/products/{filename}"
            else:
                print(f"    ⚠️  Failed to download image for {sku}: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"    ⚠️  Error downloading image for {sku}: {e}")
            return None
            
    def save_product(self, product):
        """Save or update product in database"""
        # Download image
        if product["imageUrl"]:
            local_path = self.download_image(product["imageUrl"], product["sku"])
            product["imageLocalPath"] = local_path
            
        # Check if product exists
        self.cursor.execute("SELECT id FROM products WHERE sku = %s", (product["sku"],))
        existing = self.cursor.fetchone()
        
        now = datetime.now()
        
        if existing:
            # Update existing product
            query = """
            UPDATE products SET
                name = %s, category = %s, priceOriginal = %s, priceWithMarkup = %s,
                markup = %s, imageUrl = %s, imageLocalPath = %s, stockStatus = %s,
                minervaUrl = %s, inStock = %s, lastScrapedAt = %s, updatedAt = %s
            WHERE sku = %s
            """
            self.cursor.execute(query, (
                product["name"], product["category"], product["priceOriginal"],
                product["priceWithMarkup"], product["markup"], product["imageUrl"],
                product.get("imageLocalPath"), product["stockStatus"],
                product["minervaUrl"], product["inStock"], now, now, product["sku"]
            ))
            self.stats["updated"] += 1
        else:
            # Insert new product
            query = """
            INSERT INTO products (
                sku, name, category, priceOriginal, priceWithMarkup, markup,
                imageUrl, imageLocalPath, stockStatus, minervaUrl, inStock,
                lastScrapedAt, createdAt, updatedAt
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                product["sku"], product["name"], product["category"],
                product["priceOriginal"], product["priceWithMarkup"], product["markup"],
                product["imageUrl"], product.get("imageLocalPath"), product["stockStatus"],
                product["minervaUrl"], product["inStock"], now, now, now
            ))
            self.stats["added"] += 1
            
        self.db.commit()
        
    def mark_out_of_stock(self, scraped_skus):
        """Mark products not found in scrape as out of stock"""
        if not scraped_skus:
            return
            
        placeholders = ",".join(["%s"] * len(scraped_skus))
        query = f"""
        UPDATE products 
        SET inStock = 0, updatedAt = %s
        WHERE sku NOT IN ({placeholders}) AND inStock = 1
        """
        now = datetime.now()
        self.cursor.execute(query, [now] + scraped_skus)
        self.stats["removed"] = self.cursor.rowcount
        self.db.commit()
        
    def run(self):
        """Main scraping workflow"""
        start_time = time.time()
        
        try:
            print("🚀 Starting Minerva scraper with stealth mode...")
            
            self.connect_db()
            self.start_log()
            self.setup_driver()
            
            if not self.login():
                raise Exception("Login failed")
                
            all_products = []
            
            for category in CATEGORIES:
                products = self.scrape_category(category)
                all_products.extend(products)
                self.random_delay(2, 4)  # Be nice to the server
                
            print(f"\n💾 Saving {len(all_products)} products to database...")
            
            for product in all_products:
                self.save_product(product)
                
            # Mark products not found as out of stock
            scraped_skus = [p["sku"] for p in all_products]
            self.mark_out_of_stock(scraped_skus)
            
            duration = int(time.time() - start_time)
            
            print(f"\n✅ Scraping completed in {duration}s")
            print(f"   📊 Stats:")
            print(f"      Found: {self.stats['found']}")
            print(f"      Added: {self.stats['added']}")
            print(f"      Updated: {self.stats['updated']}")
            print(f"      Removed: {self.stats['removed']}")
            
            self.update_log("success")
            
            # Send success notification
            self.notification_service.notify_scrape_success(self.stats)
            
            # Notify about stock changes if any
            if self.out_of_stock_products:
                self.notification_service.notify_stock_changes(
                    out_of_stock=self.out_of_stock_products,
                    back_in_stock=[]
                )
            
            # Notify about price changes if any
            if self.price_changes:
                self.notification_service.notify_price_changes(self.price_changes)
            
            # Check for low stock
            self.notification_service.notify_low_stock_count(self.stats['found'])
            
        except Exception as e:
            print(f"\n❌ Scraping failed: {e}")
            import traceback
            traceback.print_exc()
            self.update_log("error", str(e))
            
            # Send failure notification
            self.notification_service.notify_scrape_failure(str(e))
            
            raise
            
        finally:
            if self.driver:
                self.driver.quit()
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

if __name__ == "__main__":
    scraper = MinervaScraper()
    scraper.run()
