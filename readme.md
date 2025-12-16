Com base no script de deploy, aqui está como iniciar o projeto localmente:

## 🚀 Passo a passo para rodar localmente:

**1. Instalar dependências globais:**
```bash
# Instalar pnpm se não tiver
npm install -g pnpm
```

**2. Instalar dependências do projeto:**
```bash
# Na raiz do projeto
pnpm install
```

**3. Configurar variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:

```bash
# Database
DATABASE_URL="mysql://root:SUA_SENHA@localhost:3306/fusion_beef"

# Server
NODE_ENV=development
PORT=3000

# JWT
JWT_SECRET="fusion-beef-secret-key-2024-ultra-secure"

# Manus OAuth
OAUTH_SERVER_URL="http://localhost:3000"
VITE_OAUTH_PORTAL_URL="http://localhost:3000"
VITE_APP_ID="fusion-beef-app"
OWNER_OPEN_ID="admin"
OWNER_NAME="Fusion Beef Admin"

# Forge API
BUILT_IN_FORGE_API_URL="http://localhost:3000"
BUILT_IN_FORGE_API_KEY="local-dev-key"
VITE_FRONTEND_FORGE_API_KEY="local-dev-key"
VITE_FRONTEND_FORGE_API_URL="http://localhost:3000"

# Analytics
VITE_ANALYTICS_ENDPOINT=""
VITE_ANALYTICS_WEBSITE_ID="fusion-beef"

# App
VITE_APP_TITLE="Fusion Beef - Carnes Premium"
VITE_APP_LOGO="/logo_original.jpg"
```

**4. Configurar o banco de dados MySQL:**
```bash
# Entrar no MySQL
mysql -u root -p

# Criar o banco
CREATE DATABASE fusion_beef CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

**5. Sincronizar o schema do banco:**
```bash
pnpm db:push
```

**6. Importar os dados dos produtos (46 produtos):**
```bash
mysql -u root -p fusion_beef < database_seed.sql
```

**7. Iniciar o projeto em modo desenvolvimento:**
```bash
pnpm dev
```

Ou se tiver scripts separados:
```bash
# Terminal 1 - Backend
pnpm dev:server

# Terminal 2 - Frontend  
pnpm dev:client
```

**8. Acessar a aplicação:**
- Frontend: `http://localhost:5173` (Vite padrão)
- Backend/API: `http://localhost:3000`
- Admin: `http://localhost:5173/admin`

---

## 📝 Comandos úteis:

```bash
# Ver scripts disponíveis
pnpm run

# Build para produção
pnpm build

# Rodar em produção local
pnpm start
```

## ⚠️ Possíveis problemas:

Se o `pnpm install` falhar por causa dos patches, remova temporariamente a seção `pnpm.patchedDependencies` do `package.json` antes de instalar.

Algum erro específico ao tentar rodar?