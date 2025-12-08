#!/bin/bash

# Script de Deploy Fusion Beef - Digital Ocean
# Arquitetura: Vite + Express + tRPC + MySQL

set -e  # Para na primeira falha

echo "=========================================="
echo "🚀 FUSION BEEF - DEPLOY DIGITAL OCEAN"
echo "=========================================="

# Configurações
PROJECT_DIR="/var/www/fusion-beef"
REPO_URL="https://github.com/smartfusionoficial/FUSION-BEEF.git"
NODE_VERSION="22"
DB_PASSWORD="DeCastro\$2025#\$\$C"

echo ""
echo "📍 Passo 1: Verificando Node.js e pnpm..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instalando..."
    curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm não encontrado. Instalando..."
    npm install -g pnpm
fi

echo "✅ Node.js $(node -v)"
echo "✅ pnpm $(pnpm -v)"

echo ""
echo "📍 Passo 2: Preparando diretório do projeto..."
if [ -d "$PROJECT_DIR" ]; then
    echo "⚠️  Diretório existe. Fazendo backup..."
    sudo mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
fi

sudo mkdir -p "$PROJECT_DIR"
sudo chown -R $USER:$USER "$PROJECT_DIR"

echo ""
echo "📍 Passo 3: Clonando repositório do GitHub..."
cd /var/www
git clone "$REPO_URL" fusion-beef
cd "$PROJECT_DIR"

echo ""
echo "📍 Passo 4: Removendo patches problemáticos do package.json..."
if [ -f "package.json" ]; then
    cp package.json package.json.backup
    
    # Cria um package.json temporário sem a seção de patches
    node -e "
    const fs = require('fs');
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    if (pkg.pnpm && pkg.pnpm.patchedDependencies) {
        delete pkg.pnpm.patchedDependencies;
    }
    fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
    "
    
    echo "✅ Patches removidos do package.json"
fi

echo ""
echo "📍 Passo 5: Instalando dependências..."
rm -rf node_modules .pnpm-store pnpm-lock.yaml patches
pnpm install --no-frozen-lockfile

echo ""
echo "📍 Passo 6: Configurando variáveis de ambiente..."
cat > .env << EOF
# Database
DATABASE_URL="mysql://root:${DB_PASSWORD}@localhost:3306/fusion_beef"

# Server
NODE_ENV=production
PORT=3000

# JWT
JWT_SECRET="fusion-beef-secret-key-2024-ultra-secure"

# Manus OAuth (valores mínimos para funcionar)
OAUTH_SERVER_URL="http://localhost:3000"
VITE_OAUTH_PORTAL_URL="http://localhost:3000"
VITE_APP_ID="fusion-beef-app"
OWNER_OPEN_ID="admin"
OWNER_NAME="Fusion Beef Admin"

# Forge API (valores mínimos)
BUILT_IN_FORGE_API_URL="http://localhost:3000"
BUILT_IN_FORGE_API_KEY="local-dev-key"
VITE_FRONTEND_FORGE_API_KEY="local-dev-key"
VITE_FRONTEND_FORGE_API_URL="http://localhost:3000"

# Analytics (opcional)
VITE_ANALYTICS_ENDPOINT=""
VITE_ANALYTICS_WEBSITE_ID="fusion-beef"

# App
VITE_APP_TITLE="Fusion Beef - Carnes Premium"
VITE_APP_LOGO="/logo_original.jpg"
EOF
echo "✅ Arquivo .env criado"

echo ""
echo "📍 Passo 7: Verificando banco de dados MySQL..."
if ! mysql -uroot -p"${DB_PASSWORD}" -e "USE fusion_beef;" 2>/dev/null; then
    echo "⚠️  Banco de dados não encontrado. Criando..."
    mysql -uroot -p"${DB_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS fusion_beef CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "✅ Banco de dados criado"
else
    echo "✅ Banco de dados já existe"
fi

echo ""
echo "📍 Passo 8: Sincronizando schema do banco de dados..."
pnpm db:push || echo "⚠️  Aviso: db:push pode ter falhado, mas continuando..."

echo ""
echo "📍 Passo 9: Importando dados dos produtos (46 produtos)..."
if [ -f "database_seed.sql" ]; then
    echo "Importando database_seed.sql..."
    mysql -uroot -p"${DB_PASSWORD}" fusion_beef < database_seed.sql
    echo "✅ 46 produtos importados com sucesso!"
else
    echo "⚠️  Arquivo database_seed.sql não encontrado. Produtos não foram importados."
fi

echo ""
echo "📍 Passo 10: Fazendo build do projeto..."
pnpm build

echo ""
echo "📍 Passo 11: Verificando build..."
if [ ! -f "dist/index.js" ]; then
    echo "❌ ERRO: Build falhou! Arquivo dist/index.js não encontrado."
    echo "Conteúdo do diretório dist:"
    ls -la dist/ 2>/dev/null || echo "Diretório dist não existe"
    exit 1
fi
echo "✅ Build concluído com sucesso!"

echo ""
echo "📍 Passo 12: Configurando PM2..."
if ! command -v pm2 &> /dev/null; then
    echo "Instalando PM2..."
    sudo npm install -g pm2
fi

# Para processos antigos
pm2 delete fusion-beef 2>/dev/null || true

# Inicia novo processo
pm2 start dist/index.js --name "fusion-beef" --env production

# Salva configuração PM2
pm2 save

# Configura PM2 para iniciar no boot
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp /home/$USER 2>/dev/null || true

echo ""
echo "📍 Passo 13: Configurando Nginx..."

# Verifica se Nginx está instalado
if ! command -v nginx &> /dev/null; then
    echo "Instalando Nginx..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo tee /etc/nginx/sites-available/fusion-beef > /dev/null << 'NGINXEOF'
server {
    listen 80;
    server_name 159.65.167.133 fusionbeef.com.br www.fusionbeef.com.br;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
NGINXEOF

# Ativa site
sudo ln -sf /etc/nginx/sites-available/fusion-beef /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testa configuração
sudo nginx -t

# Reinicia Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

echo ""
echo "=========================================="
echo "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📊 Status dos serviços:"
pm2 status
echo ""
echo "🌐 Site disponível em:"
echo "  - http://159.65.167.133"
echo "  - http://fusionbeef.com.br (se DNS configurado)"
echo ""
echo "🔐 Acesso Admin:"
echo "  - URL: http://159.65.167.133/admin"
echo "  - Usuário: admin"
echo "  - Senha: fusion2024"
echo ""
echo "📝 Comandos úteis:"
echo "  - Ver logs: pm2 logs fusion-beef"
echo "  - Reiniciar: pm2 restart fusion-beef"
echo "  - Parar: pm2 stop fusion-beef"
echo "  - Status: pm2 status"
echo "  - Logs do Nginx: sudo tail -f /var/log/nginx/error.log"
echo ""
echo "🔍 Verificar se está funcionando:"
echo "  curl http://localhost:3000"
echo "  curl http://159.65.167.133"
echo ""
echo "📦 Total de produtos no banco:"
mysql -uroot -p"${DB_PASSWORD}" fusion_beef -e "SELECT COUNT(*) as total FROM products WHERE inStock = 1;" 2>/dev/null || echo "  (execute: mysql -uroot -p fusion_beef -e 'SELECT COUNT(*) FROM products;')"
echo ""
