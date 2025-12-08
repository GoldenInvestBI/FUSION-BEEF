#!/usr/bin/env python3
"""
Minerva Products Scraper - MANUAL VERSION
Para executar localmente no seu computador com interface gráfica

INSTRUÇÕES DE USO:
1. Instale as dependências:
   pip install selenium mysql-connector-python requests python-dotenv

2. Baixe o ChromeDriver compatível com seu Chrome:
   https://chromedriver.chromium.org/downloads

3. Configure as variáveis de ambiente no arquivo .env:
   DATABASE_URL=mysql://user:pass@host:port/database

4. Execute o script:
   python scrape_minerva_manual.py

O navegador abrirá em modo visível. Você verá todo o processo de scraping.
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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MINERVA_URL = "https://meuminerva.com/"
CNPJ = "55298629000151"
PASSWORD = "Borgh$2024#$$"
MARKUP_PERCENT = 60.0

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = SCRIPT_DIR.parent
IMAGE_DIR = PROJECT_DIR / "client" / "public" / "images" / "products"

# Parse DATABASE_URL from environment
def get_db_config():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        raise Exception("DATABASE_URL not set in .env file")
    
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
        
    def random_delay(self, min_sec=1, max_sec=3):
        """Add random human-like delay"""
        time.sleep(random.uniform(min_sec, max_sec))
        
    def human_type(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def setup_driver(self):
        """Initialize Selenium WebDriver - VISIBLE MODE"""
        chrome_options = Options()
        
        # VISIBLE MODE - você verá o navegador funcionando
        # chrome_options.add_argument("--headless")  # COMENTADO para modo visível
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
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
                window.chrome = {
                    runtime: {}
                };
            """
        })
        
        print("✅ WebDriver initialized in VISIBLE mode")
        print("   Você verá o navegador funcionando!")
        
    def connect_db(self):
        """Connect to MySQL database"""
        try:
            db_config = get_db_config()
            print(f"🔌 Connecting to database at {db_config['host']}...")
            self.db = mysql.connector.connect(**db_config)
            self.cursor = self.db.cursor(dictionary=True)
            print("✅ Connected to database")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("\nVerifique se:")
            print("1. O arquivo .env existe no diretório do projeto")
            print("2. A variável DATABASE_URL está configurada corretamente")
            print("3. Você tem acesso à rede/VPN necessária")
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
        
    def manual_login(self):
        """Manual login - você fará o login manualmente"""
        print("\n" + "="*60)
        print("🔐 ETAPA DE LOGIN MANUAL")
        print("="*60)
        print("\nO navegador abrirá o portal Minerva.")
        print("Por favor, faça o login MANUALMENTE:")
        print(f"  CNPJ: {CNPJ}")
        print(f"  Senha: {PASSWORD}")
        print("\nApós fazer login e ver a página inicial,")
        print("pressione ENTER aqui no terminal para continuar...")
        print("="*60 + "\n")
        
        # Navigate to homepage
        self.driver.get(MINERVA_URL)
        
        # Wait for manual login
        input("⏸️  Pressione ENTER após fazer login manualmente... ")
        
        # Check if logged in
        current_url = self.driver.current_url
        print(f"\n✅ URL atual: {current_url}")
        
        if "customer/account" in current_url or "dashboard" in current_url or current_url != MINERVA_URL:
            print("✅ Login detectado! Continuando...")
            return True
        else:
            print("⚠️  Não foi possível confirmar o login.")
            response = input("Você fez login com sucesso? (s/n): ")
            return response.lower() == 's'
            
    def scrape_category(self, category_name):
        """Scrape all products from a specific category"""
        print(f"\n📂 Scraping category: {category_name}")
        
        try:
            # Find and click category menu
            category_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{category_name}')]"))
            )
            category_url = category_link.get_attribute("href")
            
            print(f"   Navigating to: {category_url}")
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
                
                page_products = 0
                    
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
                        page_products += 1
                        self.stats["found"] += 1
                        
                        print(f"     ✓ {sku}: {name[:50]}...")
                        
                    except Exception as e:
                        print(f"    ⚠️  Error extracting product: {e}")
                        continue
                
                print(f"  ✅ Extracted {page_products} products from page {page}")
                        
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
            import traceback
            traceback.print_exc()
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
                
                ext = clean_url.split(".")[-1].split("?")[0]
                if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    ext = 'jpg'
                    
                filename = f"{sku}.{ext}"
                filepath = IMAGE_DIR / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                file_size = len(response.content) / 1024  # KB
                print(f"       📥 Downloaded image: {filename} ({file_size:.1f}KB)")
                    
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
            print("\n" + "="*60)
            print("🚀 MINERVA SCRAPER - MODO MANUAL")
            print("="*60)
            print(f"\nDiretório do projeto: {PROJECT_DIR}")
            print(f"Diretório de imagens: {IMAGE_DIR}")
            print(f"Categorias: {len(CATEGORIES)}")
            print(f"Markup: {MARKUP_PERCENT}%")
            print("\n" + "="*60 + "\n")
            
            self.connect_db()
            self.start_log()
            self.setup_driver()
            
            if not self.manual_login():
                raise Exception("Login manual não foi completado")
                
            all_products = []
            
            for i, category in enumerate(CATEGORIES, 1):
                print(f"\n[{i}/{len(CATEGORIES)}] Processing category: {category}")
                products = self.scrape_category(category)
                all_products.extend(products)
                self.random_delay(2, 4)  # Be nice to the server
                
            print(f"\n{'='*60}")
            print(f"💾 Saving {len(all_products)} products to database...")
            print(f"{'='*60}\n")
            
            for i, product in enumerate(all_products, 1):
                print(f"[{i}/{len(all_products)}] Saving {product['sku']}...")
                self.save_product(product)
                
            # Mark products not found as out of stock
            scraped_skus = [p["sku"] for p in all_products]
            self.mark_out_of_stock(scraped_skus)
            
            duration = int(time.time() - start_time)
            minutes = duration // 60
            seconds = duration % 60
            
            print(f"\n{'='*60}")
            print(f"✅ SCRAPING COMPLETED!")
            print(f"{'='*60}")
            print(f"⏱️  Duration: {minutes}m {seconds}s")
            print(f"📊 Statistics:")
            print(f"   • Products found: {self.stats['found']}")
            print(f"   • Products added: {self.stats['added']}")
            print(f"   • Products updated: {self.stats['updated']}")
            print(f"   • Products removed: {self.stats['removed']}")
            print(f"{'='*60}\n")
            
            self.update_log("success")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Scraping interrupted by user")
            self.update_log("error", "Interrupted by user")
            
        except Exception as e:
            print(f"\n❌ Scraping failed: {e}")
            import traceback
            traceback.print_exc()
            self.update_log("error", str(e))
            raise
            
        finally:
            if self.driver:
                print("\n🔒 Closing browser...")
                self.driver.quit()
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
            print("✅ Cleanup completed\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("MINERVA PRODUCTS SCRAPER - MANUAL VERSION")
    print("="*60)
    print("\nEste script abrirá o navegador em modo visível.")
    print("Você precisará fazer login manualmente no portal Minerva.")
    print("\nPressione Ctrl+C a qualquer momento para cancelar.")
    print("="*60 + "\n")
    
    try:
        scraper = MinervaScraper()
        scraper.run()
    except KeyboardInterrupt:
        print("\n\n👋 Scraping cancelado pelo usuário\n")
        sys.exit(0)
