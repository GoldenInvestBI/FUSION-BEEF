# Instruções para Configurar Deploy Automático via GitHub Actions

## Passo 1: Adicionar Chave SSH ao Servidor Digital Ocean

1. **Acesse seu servidor Digital Ocean via SSH**:
   ```bash
   ssh root@159.65.167.133
   ```

2. **Adicione a chave pública do GitHub Actions**:
   ```bash
   echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEi79lU/6PMj+PKZMSnYlD9u3BXpYPE1MtRZOEDUWMtC github-actions-fusion-beef" >> ~/.ssh/authorized_keys
   ```

3. **Verifique as permissões**:
   ```bash
   chmod 600 ~/.ssh/authorized_keys
   chmod 700 ~/.ssh
   ```

## Passo 2: Testar Deploy Automático

Após adicionar a chave SSH, o deploy automático via GitHub Actions será ativado automaticamente.

**Como funciona**:
- Toda vez que você fizer `git push` para o repositório GitHub
- O GitHub Actions executará automaticamente o deploy no Digital Ocean
- O site será atualizado em https://www.fusionbeef.com.br

## Passo 3: Monitorar Deploys

Você pode monitorar os deploys em:
- https://github.com/smartfusionoficial/FUSION-BEEF/actions

## Troubleshooting

Se o deploy falhar:
1. Verifique se a chave SSH foi adicionada corretamente
2. Verifique os logs no GitHub Actions
3. Certifique-se de que o servidor tem Node.js e PM2 instalados

## Deploy Manual (Alternativa)

Se preferir fazer deploy manual:

```bash
# No seu computador local
cd /caminho/para/fusion_beef_portfolio
git pull origin main

# Fazer build
pnpm install
pnpm build

# Enviar para o servidor
rsync -avz --delete dist/ root@159.65.167.133:/var/www/fusionbeef/
rsync -avz --delete server/ root@159.65.167.133:/var/www/fusionbeef/server/

# No servidor
ssh root@159.65.167.133
cd /var/www/fusionbeef
pm2 restart fusionbeef
```

## Credenciais Importantes

**GitHub**:
- Repositório: https://github.com/smartfusionoficial/FUSION-BEEF
- Token já configurado nos secrets

**Digital Ocean**:
- IP: 159.65.167.133
- Token já configurado nos secrets

**Portal Minerva**:
- URL: https://meuminerva.com/
- CNPJ: 55298629000151
- Senha: Borgh$2024#$$
