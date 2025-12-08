# Fusion Beef - TODO List

## Deploy e Infraestrutura
- [ ] Atualizar código no GitHub
- [ ] Fazer deploy no Digital Ocean

## Scraping e Dados
- [ ] Completar script de scraping Python para todos os menus
- [ ] Testar scraping em todas as categorias (Azeite, Bovinos, Bovinos Premium, Cordeiros, Empanados, Vegetais, Jerked Beef, Pescados, Suínos, Combos, Promoções)
- [ ] Executar scraping completo e popular banco de dados
- [ ] Verificar download de imagens de alta qualidade

## Automação
- [ ] Configurar cron job para execução a cada 2 horas
- [ ] Testar execução automática do scraper

## Sistema de Notificações
- [ ] Implementar notificações para produtos fora de estoque
- [ ] Implementar notificações para mudanças de preço
- [ ] Configurar envio de notificações ao owner

## Testes Finais
- [ ] Verificar funcionamento completo do site
- [ ] Testar admin dashboard
- [ ] Validar automação do scraping


## Scripts de Scraping Criados
- [x] Script de scraping com técnicas anti-detecção (scrape_minerva_stealth.py)
- [x] Script de scraping manual para execução local (scrape_minerva_manual.py)
- [x] README completo com instruções de uso
- [ ] Executar scraping manual localmente para popular banco de dados


## Sistema de Notificações
- [x] Criar serviço de notificações (notifications.py)
- [x] Integrar notificações no scraper stealth
- [x] Notificação de sucesso do scraping
- [x] Notificação de falha do scraping
- [x] Notificação de produtos fora de estoque
- [x] Notificação de mudanças de preço
- [x] Notificação de estoque baixo

## Automação Configurada
- [x] Script bash para cron job (run_scraper_cron.sh)
- [x] Documentação completa de configuração (CRON_SETUP.md)
- [x] Sistema de logs automático
- [x] Limpeza automática de logs antigos


## Deploy e GitHub Actions
- [x] Guardar tokens (Digital Ocean e GitHub) em arquivo seguro
- [x] Configurar repositório GitHub remoto
- [x] Push do código para GitHub
- [x] Criar workflow GitHub Actions para deploy automático
- [x] Criar documentação completa de configuração (DEPLOY_SETUP.md)
- [ ] Configurar secrets no repositório GitHub
- [ ] Configurar chave SSH no servidor Digital Ocean
- [ ] Executar primeiro deploy via GitHub Actions
- [ ] Testar deploy automático


## Scraping Manual e Autenticação Admin
- [x] Fazer scraping manual de 12 produtos de Bovinos do portal Minerva
- [x] Salvar 12 produtos no banco de dados (total: 19 produtos)
- [x] Implementar sistema de login/senha no dashboard admin
- [x] Testar autenticação (Usuário: admin | Senha: fusion2024)
- [x] Validar produtos no site
- [x] Botão Admin visível no header
- [x] Botão Sair funcionando
- [x] Dashboard mostrando estatísticas corretas


#### Coleta Completa de Produtos
- [x] Coletar produtos da categoria Suínos (8 produtos)
- [x] Coletar produtos da categoria Pescados (8 produtos)
- [x] Salvar 16 novos produtos no banco de dados
- [x] Total no catálogo: 35 produtos
- [ ] Coletar produtos da categoria Cordeiros
- [ ] Coletar produtos da categoria Empanados
- [ ] Coletar produtos da categoria Vegetais
- [ ] Coletar produtos da categoria Jerked Beef
- [ ] Coletar produtos da categoria Azeite
- [ ] Coletar produtos da categoria Combosdutos da categoria Promoções
- [ ] Salvar todos os produtos no banco de dados
## Deploy Automático
- [x] Criar instruções de configuração SSH (INSTRUCOES_DEPLOY_SSH.md)
- [ ] Adicionar chave SSH ao servidor Digital Ocean (manual)
- [ ] Testar deploy via GitHub Actions
- [ ] Validar site em produção GitHub Actions
- [ ] Validar site em produção


## Coleta Completa de Produtos
- [ ] Scraping de produtos da categoria Suínos
- [ ] Scraping de produtos da categoria Pescados
- [ ] Scraping de produtos da categoria Cordeiros
- [ ] Scraping de produtos da categoria Empanados
- [ ] Scraping de produtos da categoria Vegetais
- [ ] Scraping de produtos da categoria Jerked Beef
- [ ] Scraping de produtos da categoria Azeite
- [ ] Scraping de produtos da categoria Combos
- [ ] Scraping de produtos da categoria Promoções
- [ ] Validar URLs das imagens do portal Minerva
- [ ] Salvar todos os produtos no banco de dados

## Deploy Automático
- [ ] Configurar chave SSH no servidor Digital Ocean
- [ ] Testar conexão SSH do GitHub Actions
- [ ] Executar deploy via GitHub Actions
- [ ] Validar site em produção


## Ajustes de Segurança
- [ ] Remover dica de senha padrão da tela de login


## Novas Tarefas
- [x] Coletar produtos da categoria Cordeiros (3 em estoque)
- [x] Coletar produtos da categoria Empanados (5 em estoque)
- [x] Coletar produtos da categoria Vegetais (categoria vazia)
- [x] Coletar produtos da categoria Jerked Beef (2 em estoque)
- [x] Coletar produtos da categoria Azeite (1 em estoque)
- [x] Coletar produtos da categoria Combos (categoria não existe)
- [x] Salvar 11 novos produtos no banco de dados
- [x] Total no catálogo: 46 produtos
- [ ] Adicionar chave SSH ao servidor Digital Ocean (manual)
- [ ] Testar deploy automático via GitHub Actions


## Teste de Deploy Automático
- [ ] Fazer push para o GitHub
- [ ] Monitorar execução do GitHub Actions
- [ ] Validar deploy no servidor Digital Ocean
- [ ] Confirmar site funcionando em produção
