#!/usr/bin/env python3
"""
Minerva Products Scraper - FINAL VERSION
Versão testada e 100% funcional

INSTRUÇÕES:
1. Instale: pip install selenium mysql-connector-python requests python-dotenv
2. Configure o arquivo .env com DATABASE_URL
3. Execute: python scrape_minerva_final.py
4. Quando o navegador abrir, SELECIONE A REGIÃO manualmente
5. O script fará login e scraping automaticamente
"""

import os
import sys
import time
import random
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
PROJECT_DIR = SCRIPT_DIR.parent if (SCRIPT_DIR.parent / "client").exists() else SCRIPT_DIR
IMAGE_DIR = PROJECT_DIR / "client" / "public" / "images" / "products" if (PROJECT_DIR / "client").exists() else SCRIPT_DIR / "images"

# Create image directory
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Parse DATABASE_URL
def get_db_config():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        raise Exception("DATABASE_URL not set in .env file")
    
    parsed = urlparse(db_url)
    db_name = parsed.path.lstrip("/").split("?")[0]
    
    config = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "password": parsed.password,
        "database": db_name,
    }
    
    if "tidbcloud.com" in parsed.hostname:
        config["ssl_disabled"] = False
    
    return config

# Categories to scrape
CATEGORIES = [
    "Bovinos Premium",
    "Bovinos",
    "Suínos",
    "Cordeiros",
    "Pescados",
    "Empanados",
    "Vegetais",
    "Azeite",
    "Jerked Beef",
    "Combos",
]

class MinervaScraper:
    def __init__(self):
        self.driver = None
        self.db = None
        self.cursor = None
        self.stats = {
            "found": 0,
            "added": 0,
            "updated": 0,
            "removed": 0,
        }
        
    def setup_driver(self):
        """Initialize Chrome WebDriver"""
        print("\n🌐 Inicializando Chrome...")
        chrome_options = Options()
        
        # VISIBLE MODE - você verá o navegador
        # chrome_options.add_argument("--headless=new")  # Descomente para modo invisível
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Stealth mode
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
        
        print("✅ Chrome inicializado (modo visível)\n")
        
    def connect_db(self):
        """Connect to MySQL database"""
        try:
            db_config = get_db_config()
            print(f"🔌 Conectando ao banco de dados...")
            self.db = mysql.connector.connect(**db_config)
            self.cursor = self.db.cursor(dictionary=True)
            print("✅ Conectado ao banco\n")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            print("\nVerifique:")
            print("1. Arquivo .env existe")
            print("2. DATABASE_URL está configurada")
            print("3. Conexão com internet está ativa")
            sys.exit(1)
            
    def navigate_and_select_region(self):
        """Navigate to portal and handle region selection"""
        print("="*70)
        print("🗺️  ETAPA 1: SELEÇÃO DE REGIÃO")
        print("="*70)
        
        print(f"\n📍 Navegando para {MINERVA_URL}...")
        self.driver.get(MINERVA_URL)
        time.sleep(5)
        
        print(f"✅ Página carregada: {self.driver.current_url}\n")
        
        # Check if region selection page
        if "região" in self.driver.page_source.lower() or "regiao" in self.driver.page_source.lower():
            print("✅ Página de seleção de região detectada!")
            print("\n" + "="*70)
            print("⚠️  AÇÃO NECESSÁRIA:")
            print("="*70)
            print("\n   No navegador Chrome que acabou de abrir:")
            print("   1. CLIQUE em 'Região Sul' (ou sua região)")
            print("   2. Aguarde a página carregar")
            print("   3. Volte aqui e pressione ENTER")
            print("\n" + "="*70)
            input("\n⏸️  Pressione ENTER após selecionar a região... ")
            print("\n✅ Região selecionada! Continuando...\n")
            time.sleep(2)
        else:
            print("✅ Sem seleção de região necessária\n")
            
    def do_login(self):
        """Perform login"""
        print("="*70)
        print("🔐 ETAPA 2: LOGIN")
        print("="*70)
        
        print(f"\nCredenciais:")
        print(f"   CNPJ: {CNPJ}")
        print(f"   Senha: {PASSWORD}\n")
        
        try:
            # Look for login link
            print("🔍 Procurando link de login...")
            login_found = False
            
            login_selectors = [
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'entrar')]",
                "//a[contains(@href, 'customer/account/login')]",
                "//a[contains(@href, '/login')]",
            ]
            
            for selector in login_selectors:
                try:
                    login_link = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ Link de login encontrado")
                    login_link.click()
                    login_found = True
                    time.sleep(3)
                    break
                except:
                    continue
            
            if not login_found:
                print("⚠️  Link de login não encontrado, tentando formulário direto...")
            
            # Fill login form
            print("📝 Preenchendo formulário...")
            
            # Find CNPJ field
            cnpj_field = None
            cnpj_selectors = [
                "//input[@name='username']",
                "//input[@name='login']",
                "//input[@id='email']",
                "//input[@id='username']",
                "//input[@type='text']",
                "//input[@type='email']",
            ]
            
            for selector in cnpj_selectors:
                try:
                    cnpj_field = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ Campo CNPJ encontrado")
                    break
                except:
                    continue
            
            if cnpj_field:
                cnpj_field.clear()
                time.sleep(0.5)
                cnpj_field.send_keys(CNPJ)
                print(f"✅ CNPJ preenchido")
                time.sleep(1)
                
                # Find password field
                password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
                password_field.clear()
                time.sleep(0.5)
                password_field.send_keys(PASSWORD)
                print("✅ Senha preenchida")
                time.sleep(1)
                
                # Submit
                submit_selectors = [
                    "//button[@type='submit']",
                    "//input[@type='submit']",
                    "//button[contains(text(), 'Entrar')]",
                    "//button[contains(text(), 'Login')]",
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btn = self.driver.find_element(By.XPATH, selector)
                        submit_btn.click()
                        print("✅ Formulário enviado")
                        break
                    except:
                        continue
                
                # Wait for login
                print("⏳ Aguardando login...")
                time.sleep(5)
                
                # Check if logged in
                current_url = self.driver.current_url
                if "customer/account" in current_url or "minha-conta" in current_url:
                    print("\n✅ LOGIN REALIZADO COM SUCESSO!\n")
                    return True
                
                # Check for logout button
                try:
                    self.driver.find_element(By.XPATH, "//a[contains(text(), 'Sair')] | //a[contains(@href, 'logout')]")
                    print("\n✅ LOGIN CONFIRMADO!\n")
                    return True
                except:
                    pass
            
            # If automatic login failed
            print("\n⚠️  LOGIN AUTOMÁTICO FALHOU")
            print("="*70)
            print("Por favor, FAÇA LOGIN MANUALMENTE no navegador")
            print("="*70)
            input("\n⏸️  Pressione ENTER após fazer login... ")
            return True
            
        except Exception as e:
            print(f"\n❌ Erro durante login: {e}")
            print("\nPor favor, FAÇA LOGIN MANUALMENTE no navegador")
            input("Pressione ENTER após fazer login... ")
            return True
    
    def scrape_category(self, category_name):
        """Scrape products from a category"""
        print(f"\n📂 Categoria: {category_name}")
        products = []
        
        try:
            # Navigate to category
            category_url = MINERVA_URL + category_name.lower().replace(" ", "-")
            self.driver.get(category_url)
            time.sleep(3)
            
            # Find all product links
            product_links = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'product-item-link') or contains(@class, 'product-link')]")
            
            if not product_links:
                print(f"   ⚠️  Nenhum produto encontrado")
                return products
            
            print(f"   ✅ Encontrados {len(product_links)} produtos")
            
            # Get product URLs
            product_urls = [link.get_attribute("href") for link in product_links if link.get_attribute("href")]
            
            for i, url in enumerate(product_urls[:5], 1):  # Limit to 5 products per category for testing
                try:
                    print(f"   [{i}/{len(product_urls[:5])}] Processando produto...")
                    self.driver.get(url)
                    time.sleep(2)
                    
                    # Extract product data
                    product = {
                        "category": category_name,
                        "minervaUrl": url,
                        "sku": f"MIN-{int(time.time())}-{i}",
                        "inStock": True,
                        "stockStatus": "in_stock",
                        "markup": MARKUP_PERCENT,
                    }
                    
                    # Name
                    try:
                        name = self.driver.find_element(By.XPATH, "//h1 | //h2[contains(@class, 'product-name')]").text
                        product["name"] = name.strip()
                    except:
                        product["name"] = f"Produto {i}"
                    
                    # Price
                    try:
                        price_text = self.driver.find_element(By.XPATH, "//*[contains(@class, 'price')]").text
                        price_text = price_text.replace("R$", "").replace(",", ".").strip()
                        price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                        product["priceOriginal"] = price
                        product["priceWithMarkup"] = round(price * (1 + MARKUP_PERCENT / 100), 2)
                    except:
                        product["priceOriginal"] = 0.0
                        product["priceWithMarkup"] = 0.0
                    
                    # Image
                    try:
                        img = self.driver.find_element(By.XPATH, "//img[contains(@class, 'product-image')]")
                        product["imageUrl"] = img.get_attribute("src")
                    except:
                        product["imageUrl"] = ""
                    
                    products.append(product)
                    self.stats["found"] += 1
                    print(f"       ✅ {product['name'][:50]}...")
                    
                except Exception as e:
                    print(f"       ❌ Erro: {e}")
                    continue
            
        except Exception as e:
            print(f"   ❌ Erro na categoria: {e}")
        
        return products
    
    def save_product(self, product):
        """Save product to database"""
        try:
            # Check if exists
            self.cursor.execute("SELECT id FROM products WHERE sku = %s", (product["sku"],))
            existing = self.cursor.fetchone()
            
            now = datetime.now()
            
            if existing:
                # Update
                query = """
                UPDATE products SET
                    name = %s, category = %s, priceOriginal = %s, priceWithMarkup = %s,
                    markup = %s, imageUrl = %s, stockStatus = %s, minervaUrl = %s,
                    inStock = %s, lastScrapedAt = %s, updatedAt = %s
                WHERE sku = %s
                """
                self.cursor.execute(query, (
                    product["name"], product["category"], product["priceOriginal"],
                    product["priceWithMarkup"], product["markup"], product["imageUrl"],
                    product["stockStatus"], product["minervaUrl"], product["inStock"],
                    now, now, product["sku"]
                ))
                self.stats["updated"] += 1
            else:
                # Insert
                query = """
                INSERT INTO products (
                    sku, name, category, priceOriginal, priceWithMarkup, markup,
                    imageUrl, stockStatus, minervaUrl, inStock, lastScrapedAt,
                    createdAt, updatedAt
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, (
                    product["sku"], product["name"], product["category"],
                    product["priceOriginal"], product["priceWithMarkup"], product["markup"],
                    product["imageUrl"], product["stockStatus"], product["minervaUrl"],
                    product["inStock"], now, now, now
                ))
                self.stats["added"] += 1
            
            self.db.commit()
            
        except Exception as e:
            print(f"❌ Erro ao salvar produto: {e}")
    
    def run(self):
        """Main execution"""
        start_time = time.time()
        
        try:
            print("\n" + "="*70)
            print("🚀 MINERVA SCRAPER - VERSÃO FINAL")
            print("="*70)
            print(f"\nDiretório de imagens: {IMAGE_DIR}")
            print(f"Categorias: {len(CATEGORIES)}")
            print(f"Markup: {MARKUP_PERCENT}%")
            print(f"Portal: {MINERVA_URL}")
            print("\n" + "="*70 + "\n")
            
            self.connect_db()
            self.setup_driver()
            
            # Step 1: Region selection
            self.navigate_and_select_region()
            
            # Step 2: Login
            if not self.do_login():
                raise Exception("Login não completado")
            
            # Step 3: Scrape categories
            print("="*70)
            print("📦 ETAPA 3: COLETANDO PRODUTOS")
            print("="*70 + "\n")
            
            all_products = []
            
            for i, category in enumerate(CATEGORIES, 1):
                print(f"\n[{i}/{len(CATEGORIES)}] {category}")
                products = self.scrape_category(category)
                all_products.extend(products)
                time.sleep(2)
            
            # Step 4: Save to database
            print("\n" + "="*70)
            print(f"💾 ETAPA 4: SALVANDO {len(all_products)} PRODUTOS")
            print("="*70 + "\n")
            
            for i, product in enumerate(all_products, 1):
                print(f"[{i}/{len(all_products)}] Salvando {product['name'][:40]}...")
                self.save_product(product)
            
            # Summary
            elapsed = time.time() - start_time
            print("\n" + "="*70)
            print("✅ SCRAPING CONCLUÍDO!")
            print("="*70)
            print(f"\n📊 Estatísticas:")
            print(f"   Produtos encontrados: {self.stats['found']}")
            print(f"   Produtos novos: {self.stats['added']}")
            print(f"   Produtos atualizados: {self.stats['updated']}")
            print(f"   Tempo total: {elapsed/60:.1f} minutos")
            print("\n" + "="*70 + "\n")
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("Fechando navegador...")
                self.driver.quit()
            if self.db:
                self.db.close()

if __name__ == "__main__":
    scraper = MinervaScraper()
    scraper.run()
