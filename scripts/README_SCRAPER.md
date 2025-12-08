# Minerva Products Scraper - Guia de Uso

## 📋 Visão Geral

Este scraper automatiza a coleta de produtos do portal Minerva (https://meuminerva.com/), aplicando markup de 60% e salvando no banco de dados do Fusion Beef.

## 🎯 Versões Disponíveis

### 1. `scrape_minerva_manual.py` ⭐ RECOMENDADO

**Script manual para executar no seu computador local**

- ✅ Navegador visível - você vê tudo acontecendo
- ✅ Login manual - você faz o login normalmente
- ✅ Mais confiável - evita bloqueios anti-bot
- ✅ Fácil de debugar

### 2. `scrape_minerva_stealth.py`

**Script automatizado com técnicas anti-detecção**

- ⚠️ Pode ser bloqueado pelo portal Minerva
- ⚠️ Requer ambiente headless funcional
- ℹ️ Útil para automação via cron job

## 🚀 Como Usar o Scraper Manual

### Pré-requisitos

1. **Python 3.7+** instalado
2. **Google Chrome** instalado
3. **ChromeDriver** compatível com sua versão do Chrome

### Passo 1: Instalar Dependências

```bash
pip install selenium mysql-connector-python requests python-dotenv
```

### Passo 2: Baixar ChromeDriver

1. Verifique sua versão do Chrome:
   - Abra Chrome
   - Digite `chrome://version` na barra de endereços
   - Anote a versão (ex: 120.0.6099.109)

2. Baixe o ChromeDriver correspondente:
   - Acesse: https://chromedriver.chromium.org/downloads
   - Baixe a versão compatível com seu Chrome
   - Extraia o arquivo `chromedriver.exe` (Windows) ou `chromedriver` (Mac/Linux)

3. Adicione o ChromeDriver ao PATH:
   - **Windows**: Coloque em `C:\Windows\System32\` ou adicione ao PATH
   - **Mac/Linux**: Coloque em `/usr/local/bin/` ou adicione ao PATH

### Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env` no diretório do projeto com:

```env
DATABASE_URL=mysql://2bTEBVUrBZTnxL6.root:F9UL1BKmaFP7bs887SBA@gateway02.us-east-1.prod.aws.tidbcloud.com:4000/JsQ8GEA7FLWzMRPSiSqGrK
```

### Passo 4: Executar o Scraper

```bash
cd /caminho/para/fusion_beef_portfolio/scripts
python scrape_minerva_manual.py
```

### Passo 5: Fazer Login Manual

1. O navegador Chrome abrirá automaticamente
2. Você verá o portal Minerva
3. Faça login normalmente:
   - **CNPJ**: 55298629000151
   - **Senha**: Borgh$2024#$$
4. Após fazer login, volte ao terminal
5. Pressione **ENTER** para continuar

### Passo 6: Aguardar Conclusão

O script irá:
- ✅ Navegar por todas as categorias
- ✅ Extrair produtos em estoque (RESFRIADO/CONGELADO)
- ✅ Baixar imagens em alta qualidade
- ✅ Aplicar markup de 60%
- ✅ Salvar no banco de dados
- ✅ Marcar produtos fora de estoque

**Tempo estimado**: 15-30 minutos (dependendo da quantidade de produtos)

## 📊 Categorias Scraped

O scraper coleta produtos de TODAS as categorias:

1. Azeite
2. Bovinos
3. Bovinos Premium
4. Cordeiros
5. Empanados
6. Vegetais
7. Jerked Beef
8. Pescados
9. Suínos
10. Combos
11. Promoções

## 💾 Dados Salvos

Para cada produto, o scraper salva:

- **SKU**: Código único do produto
- **Nome**: Nome completo
- **Categoria**: Categoria do menu
- **Preço Original**: Preço do portal Minerva
- **Preço com Markup**: Preço original + 60%
- **Markup**: Percentual aplicado (60%)
- **URL da Imagem**: Link original da imagem
- **Caminho Local**: Caminho da imagem baixada
- **Status de Estoque**: RESFRIADO ou CONGELADO
- **URL Minerva**: Link do produto no portal
- **Em Estoque**: Booleano (1 = sim, 0 = não)
- **Última Raspagem**: Data/hora da última atualização

## 🔄 Automação (Cron Job)

Para executar automaticamente a cada 2 horas:

### Linux/Mac

```bash
# Editar crontab
crontab -e

# Adicionar linha (executar a cada 2 horas)
0 */2 * * * cd /caminho/para/fusion_beef_portfolio/scripts && python3 scrape_minerva_stealth.py >> /var/log/minerva_scraper.log 2>&1
```

### Windows (Task Scheduler)

1. Abra o **Agendador de Tarefas**
2. Criar Tarefa Básica
3. Nome: "Minerva Scraper"
4. Gatilho: Diariamente, repetir a cada 2 horas
5. Ação: Iniciar programa
   - Programa: `python`
   - Argumentos: `scrape_minerva_stealth.py`
   - Iniciar em: `C:\caminho\para\fusion_beef_portfolio\scripts`

## 🐛 Troubleshooting

### Erro: "ChromeDriver not found"

**Solução**: Certifique-se de que o ChromeDriver está no PATH ou no mesmo diretório do script.

### Erro: "Database connection failed"

**Solução**: 
1. Verifique se o arquivo `.env` existe
2. Confirme que a `DATABASE_URL` está correta
3. Teste a conexão com o banco de dados

### Erro: "Element not interactable"

**Solução**: Use o script manual (`scrape_minerva_manual.py`) em vez do automático.

### Produtos não estão sendo encontrados

**Solução**:
1. Verifique se você fez login corretamente
2. Confirme que está na região correta (Nordeste/Centro-Oeste/Sudeste)
3. Verifique se há produtos em estoque no portal Minerva

## 📝 Logs

O scraper registra todas as ações no banco de dados na tabela `scrape_logs`:

- **ID**: Identificador único do log
- **Status**: success, error, running
- **Produtos Encontrados**: Total de produtos scraped
- **Produtos Adicionados**: Novos produtos
- **Produtos Atualizados**: Produtos existentes atualizados
- **Produtos Removidos**: Produtos marcados como fora de estoque
- **Mensagem de Erro**: Detalhes de erros (se houver)
- **Iniciado Em**: Data/hora de início
- **Completado Em**: Data/hora de conclusão

## 🔐 Segurança

- ⚠️ **Nunca compartilhe** o arquivo `.env` com credenciais
- ⚠️ **Não faça commit** do `.env` no Git
- ✅ O `.gitignore` já está configurado para ignorar `.env`

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs no banco de dados (`scrape_logs`)
2. Execute o script manual para ver erros em tempo real
3. Capture screenshots dos erros
4. Entre em contato com o suporte técnico

## 🎯 Próximos Passos

Após executar o scraper com sucesso:

1. ✅ Verifique os produtos no admin dashboard
2. ✅ Confirme que as imagens foram baixadas
3. ✅ Teste o site público (https://www.fusionbeef.com.br)
4. ✅ Configure o cron job para automação
5. ✅ Monitore os logs regularmente
