# Configuração do Deploy Automático via GitHub Actions

## 📋 Visão Geral

Este projeto usa **GitHub Actions** para deploy automático no Digital Ocean. Toda vez que você fizer push para a branch `main`, o deploy será executado automaticamente.

## 🔐 Configurar Secrets no GitHub

Para que o deploy funcione, você precisa configurar os seguintes secrets no repositório GitHub:

### Passo 1: Acessar Configurações de Secrets

1. Acesse: https://github.com/smartfusionoficial/FUSION-BEEF/settings/secrets/actions
2. Clique em **"New repository secret"**

### Passo 2: Adicionar os Secrets

Adicione cada um dos seguintes secrets:

#### 1. SSH_PRIVATE_KEY

**Valor**: A chave SSH privada para acesso ao servidor Digital Ocean

Para gerar uma nova chave SSH (se ainda não tiver):

```bash
# No seu computador local
ssh-keygen -t ed25519 -C "github-actions-fusion-beef" -f ~/.ssh/fusion_beef_deploy

# Copiar a chave pública para o servidor
ssh-copy-id -i ~/.ssh/fusion_beef_deploy.pub root@159.65.167.133

# Copiar a chave privada (cole no GitHub Secret)
cat ~/.ssh/fusion_beef_deploy
```

#### 2. DATABASE_URL

**Valor**: 
```
mysql://2bTEBVUrBZTnxL6.root:F9UL1BKmaFP7bs887SBA@gateway02.us-east-1.prod.aws.tidbcloud.com:4000/JsQ8GEA7FLWzMRPSiSqGrK
```

#### 3. JWT_SECRET

**Valor**: (obter do arquivo .env do projeto)

#### 4. OAUTH_SERVER_URL

**Valor**: (obter do arquivo .env do projeto)

#### 5. OWNER_NAME

**Valor**: (obter do arquivo .env do projeto)

#### 6. OWNER_OPEN_ID

**Valor**: (obter do arquivo .env do projeto)

#### 7. VITE_APP_ID

**Valor**: (obter do arquivo .env do projeto)

#### 8. VITE_APP_TITLE

**Valor**: `Fusion Beef - Carnes Premium`

#### 9. VITE_APP_LOGO

**Valor**: `/logo_original.jpg`

## 🚀 Como Fazer Deploy

### Deploy Automático (Recomendado)

Simplesmente faça push para a branch `main`:

```bash
git add .
git commit -m "feat: Nova funcionalidade"
git push origin main
```

O GitHub Actions irá automaticamente:
1. ✅ Fazer checkout do código
2. ✅ Instalar dependências
3. ✅ Fazer build da aplicação
4. ✅ Criar pacote de deploy
5. ✅ Enviar para o servidor Digital Ocean
6. ✅ Fazer backup da versão anterior
7. ✅ Extrair nova versão
8. ✅ Instalar dependências de produção
9. ✅ Reiniciar aplicação com PM2
10. ✅ Verificar se o deploy foi bem-sucedido

### Deploy Manual

Você também pode disparar o deploy manualmente:

1. Acesse: https://github.com/smartfusionoficial/FUSION-BEEF/actions
2. Clique em **"Deploy to Digital Ocean"**
3. Clique em **"Run workflow"**
4. Selecione a branch `main`
5. Clique em **"Run workflow"**

## 📊 Monitorar o Deploy

### Ver Logs do Deploy

1. Acesse: https://github.com/smartfusionoficial/FUSION-BEEF/actions
2. Clique no workflow mais recente
3. Clique em **"deploy"** para ver os logs detalhados

### Verificar Status

O workflow mostra:
- ✅ **Success** - Deploy concluído com sucesso
- ❌ **Failure** - Deploy falhou (verifique os logs)
- 🟡 **In Progress** - Deploy em andamento

## 🔧 Configuração do Servidor

### Pré-requisitos no Servidor Digital Ocean

O servidor precisa ter instalado:

1. **Node.js 22+**
2. **pnpm**
3. **PM2** (gerenciador de processos)
4. **Python 3** (para o scraper)
5. **Chromium** (para o scraper)

### Instalar Pré-requisitos (executar uma vez)

```bash
# Conectar ao servidor
ssh root@159.65.167.133

# Instalar Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs

# Instalar pnpm
npm install -g pnpm

# Instalar PM2
npm install -g pm2

# Instalar Python e dependências
apt-get install -y python3 python3-pip chromium-browser

# Instalar dependências Python do scraper
pip3 install selenium mysql-connector-python requests python-dotenv

# Criar diretório da aplicação
mkdir -p /var/www/fusion-beef

# Criar diretório de backups
mkdir -p /var/backups
```

### Configurar Variáveis de Ambiente no Servidor

```bash
# Criar arquivo .env no servidor
nano /var/www/fusion-beef/.env

# Adicionar todas as variáveis de ambiente necessárias
DATABASE_URL=mysql://...
JWT_SECRET=...
OAUTH_SERVER_URL=...
# ... etc
```

### Configurar Cron Job para Scraper

```bash
# Editar crontab
crontab -e

# Adicionar linha para executar scraper a cada 2 horas
0 */2 * * * /var/www/fusion-beef/scripts/run_scraper_cron.sh >> /var/www/fusion-beef/logs/cron.log 2>&1
```

## 🐛 Troubleshooting

### Deploy falha com erro de SSH

**Problema**: `Permission denied (publickey)`

**Solução**: 
1. Verifique se o secret `SSH_PRIVATE_KEY` está configurado corretamente
2. Confirme que a chave pública foi adicionada ao servidor: `cat ~/.ssh/authorized_keys`

### Deploy falha no build

**Problema**: Erro durante `pnpm run build`

**Solução**:
1. Verifique se todos os secrets estão configurados no GitHub
2. Teste o build localmente: `pnpm install && pnpm run build`

### Aplicação não inicia após deploy

**Problema**: PM2 não consegue iniciar a aplicação

**Solução**:
1. SSH no servidor: `ssh root@159.65.167.133`
2. Verificar logs do PM2: `pm2 logs fusion-beef`
3. Verificar se o arquivo .env existe: `cat /var/www/fusion-beef/.env`
4. Reiniciar manualmente: `cd /var/www/fusion-beef && pm2 restart fusion-beef`

### Site não está acessível

**Problema**: https://www.fusionbeef.com.br não responde

**Solução**:
1. Verificar se a aplicação está rodando: `pm2 status`
2. Verificar se o Nginx está configurado corretamente
3. Verificar logs do Nginx: `tail -f /var/log/nginx/error.log`

## 📝 Estrutura do Deploy

```
/var/www/fusion-beef/
├── dist/              # Frontend build
├── server/            # Backend code
├── drizzle/           # Database schema
├── scripts/           # Scraper scripts
├── logs/              # Application logs
├── .env               # Environment variables
├── package.json
└── pnpm-lock.yaml

/var/backups/
└── fusion-beef-YYYYMMDD-HHMMSS.tar.gz  # Backups automáticos
```

## 🔄 Rollback (Reverter Deploy)

Se algo der errado, você pode reverter para uma versão anterior:

```bash
# SSH no servidor
ssh root@159.65.167.133

# Listar backups disponíveis
ls -lh /var/backups/fusion-beef-*.tar.gz

# Restaurar backup (substitua a data)
cd /var/www/fusion-beef
tar -xzf /var/backups/fusion-beef-20241208-143000.tar.gz

# Reiniciar aplicação
pm2 restart fusion-beef
```

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs do GitHub Actions
2. Verifique os logs do PM2 no servidor
3. Verifique os logs do Nginx
4. Entre em contato com o suporte técnico

## 🎯 Checklist Pós-Deploy

Após cada deploy bem-sucedido, verifique:

- [ ] Site está acessível: https://www.fusionbeef.com.br
- [ ] Admin dashboard funciona: https://www.fusionbeef.com.br/admin
- [ ] Produtos estão sendo exibidos corretamente
- [ ] Scraper está configurado no cron
- [ ] PM2 está salvando o processo: `pm2 save`
- [ ] Logs estão sendo gerados corretamente
