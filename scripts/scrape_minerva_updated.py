#!/usr/bin/env python3
"""
Minerva Products Scraper
Automatically scrapes ALL products from ALL categories in the Minerva portal
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import mysql.connector
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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
        self.stats = {
            "found": 0,
            "added": 0,
            "updated": 0,
            "removed": 0,
        }
        
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
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
        """Login to Minerva portal"""
        print("🔐 Logging in to Minerva...")
        self.driver.get(MINERVA_URL)
        time.sleep(3)
        
        try:
            # Click login button
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Faça seu login')]"))
            )
            login_btn.click()
            time.sleep(2)
            
            # Enter CNPJ
            cnpj_input = self.driver.find_element(By.ID, "username")
            cnpj_input.clear()
            cnpj_input.send_keys(CNPJ)
            time.sleep(1)
            
            # Click advance
            advance_btn = self.driver.find_element(By.ID, "send2")
            advance_btn.click()
            time.sleep(2)
            
            # Enter password
            pass_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "pass"))
            )
            pass_input.clear()
            pass_input.send_keys(PASSWORD)
            time.sleep(1)
            
            # Click final advance
            final_btn = self.driver.find_element(By.ID, "send2")
            final_btn.click()
            time.sleep(5)
            
            print("✅ Login successful")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
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
            self.driver.get(category_url)
            time.sleep(3)
            
            products = []
            page = 1
            
            while True:
                print(f"  📄 Page {page}...")
                
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
                    next_btn.click()
                    time.sleep(3)
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
            
            response = requests.get(clean_url, timeout=30)
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
            print("🚀 Starting Minerva scraper...")
            
            self.connect_db()
            self.start_log()
            self.setup_driver()
            
            if not self.login():
                raise Exception("Login failed")
                
            all_products = []
            
            for category in CATEGORIES:
                products = self.scrape_category(category)
                all_products.extend(products)
                time.sleep(2)  # Be nice to the server
                
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
            
        except Exception as e:
            print(f"\n❌ Scraping failed: {e}")
            self.update_log("error", str(e))
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
