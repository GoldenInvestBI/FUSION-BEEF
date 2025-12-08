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
