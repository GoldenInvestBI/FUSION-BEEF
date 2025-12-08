import mysql from "mysql2/promise";
import fs from "fs";

const DATABASE_URL = process.env.DATABASE_URL || "mysql://root@localhost:3306/fusion_beef_portfolio";

async function generateSeed() {
  try {
    console.log("Conectando ao banco...");
    const connection = await mysql.createConnection(DATABASE_URL);
    
    console.log("Buscando produtos...");
    const [products] = await connection.execute("SELECT * FROM products ORDER BY id");
    
    console.log("Buscando configurações...");
    const [settings] = await connection.execute("SELECT * FROM settings ORDER BY id");
    
    console.log(`✅ ${products.length} produtos encontrados`);
    console.log(`✅ ${settings.length} configurações encontradas`);
    
    let sql = `-- Fusion Beef - Database Seed
-- ${products.length} produtos + ${settings.length} configurações
-- Gerado em: ${new Date().toISOString()}

-- Limpar dados existentes
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE products;
TRUNCATE TABLE settings;
TRUNCATE TABLE scrape_logs;
SET FOREIGN_KEY_CHECKS = 1;

`;

    // Settings
    if (settings.length > 0) {
      sql += "-- Configurações\n";
      for (const s of settings) {
        const desc = s.description ? `'${s.description.replace(/'/g, "\\'")}'` : 'NULL';
        sql += `INSERT INTO settings (\`key\`, value, description, updatedAt) VALUES ('${s.key}', '${s.value}', ${desc}, NOW());\n`;
      }
      sql += "\n";
    }
    
    // Products
    if (products.length > 0) {
      sql += "-- Produtos\n";
      for (const p of products) {
        const name = p.name.replace(/'/g, "\\'");
        const imageUrl = p.imageUrl ? `'${p.imageUrl}'` : 'NULL';
        const imageLocalPath = p.imageLocalPath ? `'${p.imageLocalPath}'` : 'NULL';
        const stockStatus = p.stockStatus ? `'${p.stockStatus}'` : 'NULL';
        const minervaUrl = p.minervaUrl ? `'${p.minervaUrl}'` : 'NULL';
        
        sql += `INSERT INTO products (sku, name, category, priceOriginal, priceWithMarkup, markup, imageUrl, imageLocalPath, stockStatus, minervaUrl, inStock, createdAt, updatedAt) VALUES ('${p.sku}', '${name}', '${p.category}', '${p.priceOriginal}', '${p.priceWithMarkup}', '${p.markup}', ${imageUrl}, ${imageLocalPath}, ${stockStatus}, ${minervaUrl}, ${p.inStock}, NOW(), NOW());\n`;
      }
    }
    
    fs.writeFileSync('database_seed.sql', sql);
    console.log("✅ Arquivo database_seed.sql gerado com sucesso!");
    console.log(`📊 Total: ${products.length} produtos, ${settings.length} configurações`);
    
    await connection.end();
    process.exit(0);
    
  } catch (error) {
    console.error("❌ Erro:", error.message);
    process.exit(1);
  }
}

generateSeed();
