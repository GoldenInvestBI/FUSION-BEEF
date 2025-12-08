# Configuração do Cron Job - Minerva Scraper

## 📋 Visão Geral

Este guia explica como configurar o scraper para executar automaticamente a cada 2 horas usando cron job.

## 🔧 Configuração no Servidor (Linux/Ubuntu)

### Passo 1: Verificar o Script

Certifique-se de que o script está executável:

```bash
chmod +x /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### Passo 2: Testar o Script Manualmente

Antes de configurar o cron, teste o script:

```bash
cd /home/ubuntu/fusion_beef_portfolio/scripts
./run_scraper_cron.sh
```

Verifique se:
- ✅ O script executa sem erros
- ✅ Os logs são criados em `/home/ubuntu/fusion_beef_portfolio/logs/`
- ✅ Os produtos são salvos no banco de dados

### Passo 3: Editar o Crontab

Abra o editor de crontab:

```bash
crontab -e
```

### Passo 4: Adicionar a Linha do Cron

Adicione a seguinte linha ao final do arquivo:

```cron
# Minerva Scraper - Executa a cada 2 horas
0 */2 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh >> /home/ubuntu/fusion_beef_portfolio/logs/cron.log 2>&1
```

**Explicação**:
- `0 */2 * * *` = A cada 2 horas (00:00, 02:00, 04:00, etc.)
- `/home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh` = Script a executar
- `>> /home/ubuntu/fusion_beef_portfolio/logs/cron.log 2>&1` = Redireciona saída para log

### Passo 5: Salvar e Sair

- **nano**: Pressione `Ctrl+X`, depois `Y`, depois `Enter`
- **vim**: Pressione `Esc`, digite `:wq`, pressione `Enter`

### Passo 6: Verificar o Cron

Liste os cron jobs configurados:

```bash
crontab -l
```

Você deve ver a linha que acabou de adicionar.

## 🕐 Horários de Execução

Com a configuração `0 */2 * * *`, o scraper executará nos seguintes horários:

- 00:00 (meia-noite)
- 02:00
- 04:00
- 06:00
- 08:00
- 10:00
- 12:00 (meio-dia)
- 14:00
- 16:00
- 18:00
- 20:00
- 22:00

## 📝 Logs

### Logs do Scraper

Cada execução cria um log individual:

```
/home/ubuntu/fusion_beef_portfolio/logs/scraper_YYYYMMDD_HHMMSS.log
```

Exemplo:
```
/home/ubuntu/fusion_beef_portfolio/logs/scraper_20241208_140000.log
```

### Log do Cron

O log geral do cron está em:

```
/home/ubuntu/fusion_beef_portfolio/logs/cron.log
```

### Visualizar Logs Recentes

```bash
# Ver últimos logs do scraper
ls -lt /home/ubuntu/fusion_beef_portfolio/logs/scraper_*.log | head -5

# Ver conteúdo do último log
tail -100 $(ls -t /home/ubuntu/fusion_beef_portfolio/logs/scraper_*.log | head -1)

# Ver log do cron
tail -100 /home/ubuntu/fusion_beef_portfolio/logs/cron.log
```

### Limpeza Automática de Logs

O script automaticamente remove logs com mais de 30 dias para economizar espaço.

## 🔄 Outras Frequências de Execução

Se quiser alterar a frequência, use estas configurações:

### A cada 1 hora
```cron
0 * * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### A cada 3 horas
```cron
0 */3 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### A cada 4 horas
```cron
0 */4 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### A cada 6 horas
```cron
0 */6 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### Uma vez por dia (às 2h da manhã)
```cron
0 2 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

### Duas vezes por dia (6h e 18h)
```cron
0 6,18 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

## 🛑 Pausar/Desabilitar o Cron

Para desabilitar temporariamente sem remover:

```bash
crontab -e
```

Adicione `#` no início da linha:

```cron
# 0 */2 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
```

Para remover completamente:

```bash
crontab -e
```

Delete a linha e salve.

## 🔍 Monitoramento

### Verificar se o Cron está Rodando

```bash
# Ver processos do cron
ps aux | grep cron

# Ver logs do sistema do cron
grep CRON /var/log/syslog | tail -20
```

### Verificar Última Execução

```bash
# Ver timestamp do último log
ls -lt /home/ubuntu/fusion_beef_portfolio/logs/scraper_*.log | head -1
```

### Verificar Status no Banco de Dados

```sql
-- Ver últimos logs de scraping
SELECT * FROM scrape_logs ORDER BY createdAt DESC LIMIT 10;

-- Ver estatísticas do último scraping
SELECT 
    status,
    productsFound,
    productsAdded,
    productsUpdated,
    productsRemoved,
    startedAt,
    completedAt,
    TIMESTAMPDIFF(MINUTE, startedAt, completedAt) as duration_minutes
FROM scrape_logs 
ORDER BY createdAt DESC 
LIMIT 1;
```

## 🐛 Troubleshooting

### Cron não está executando

1. **Verificar se o cron está ativo**:
   ```bash
   sudo systemctl status cron
   ```

2. **Reiniciar o cron**:
   ```bash
   sudo systemctl restart cron
   ```

3. **Verificar permissões**:
   ```bash
   ls -l /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
   ```
   Deve mostrar `-rwxr-xr-x` (executável)

### Script falha ao executar via cron

1. **Verificar variáveis de ambiente**:
   O cron não carrega o mesmo ambiente que seu shell. Certifique-se de que o arquivo `.env` existe e está acessível.

2. **Usar caminhos absolutos**:
   O script já usa caminhos absolutos, mas verifique se todos os arquivos necessários existem.

3. **Verificar logs de erro**:
   ```bash
   tail -100 /home/ubuntu/fusion_beef_portfolio/logs/cron.log
   ```

### Scraper está falhando

1. **Executar manualmente para ver erros**:
   ```bash
   cd /home/ubuntu/fusion_beef_portfolio/scripts
   ./run_scraper_cron.sh
   ```

2. **Verificar conexão com banco de dados**:
   ```bash
   mysql -h gateway02.us-east-1.prod.aws.tidbcloud.com -P 4000 -u 2bTEBVUrBZTnxL6.root -p
   ```

3. **Verificar se o ChromeDriver está instalado**:
   ```bash
   which chromium-browser
   chromium-browser --version
   ```

## 📧 Notificações por Email (Opcional)

Para receber emails quando o scraper falhar:

1. **Instalar mailutils**:
   ```bash
   sudo apt-get install mailutils
   ```

2. **Modificar o cron para enviar email**:
   ```cron
   MAILTO=seu-email@exemplo.com
   0 */2 * * * /home/ubuntu/fusion_beef_portfolio/scripts/run_scraper_cron.sh
   ```

## 🎯 Melhores Práticas

1. ✅ **Monitore regularmente** os logs de scraping
2. ✅ **Verifique o banco de dados** semanalmente para garantir que os produtos estão atualizados
3. ✅ **Ajuste a frequência** conforme necessário (mais ou menos vezes por dia)
4. ✅ **Mantenha backups** do banco de dados
5. ✅ **Teste manualmente** após mudanças no portal Minerva

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs em `/home/ubuntu/fusion_beef_portfolio/logs/`
2. Consulte a tabela `scrape_logs` no banco de dados
3. Execute o script manualmente para debug
4. Entre em contato com o suporte técnico
