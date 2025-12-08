#!/usr/bin/env python3
"""
Notification System for Minerva Scraper
Sends notifications about stock changes and price updates
"""

import os
import sys
import requests
from datetime import datetime
from typing import List, Dict, Optional

# Manus Notification API
NOTIFICATION_API_URL = os.getenv("BUILT_IN_FORGE_API_URL", "") + "/notification"
NOTIFICATION_API_KEY = os.getenv("BUILT_IN_FORGE_API_KEY", "")
OWNER_OPEN_ID = os.getenv("OWNER_OPEN_ID", "")
APP_ID = os.getenv("VITE_APP_ID", "")

class NotificationService:
    """Service for sending notifications to project owner"""
    
    def __init__(self):
        self.api_url = NOTIFICATION_API_URL
        self.api_key = NOTIFICATION_API_KEY
        self.owner_id = OWNER_OPEN_ID
        self.app_id = APP_ID
        
    def send_notification(self, title: str, content: str) -> bool:
        """
        Send notification to project owner
        
        Args:
            title: Notification title
            content: Notification content (supports markdown)
            
        Returns:
            True if successful, False otherwise
        """
        if not all([self.api_url, self.api_key, self.owner_id, self.app_id]):
            print("⚠️  Notification service not configured")
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "appId": self.app_id,
                "userId": self.owner_id,
                "title": title,
                "content": content,
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Notification sent: {title}")
                return True
            else:
                print(f"⚠️  Notification failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending notification: {e}")
            return False
    
    def notify_scrape_success(self, stats: Dict) -> bool:
        """Notify about successful scrape completion"""
        title = "✅ Scraping Minerva Concluído com Sucesso"
        
        content = f"""
## Resumo do Scraping

**Data/Hora**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

### Estatísticas

- **Produtos Encontrados**: {stats.get('found', 0)}
- **Produtos Adicionados**: {stats.get('added', 0)}
- **Produtos Atualizados**: {stats.get('updated', 0)}
- **Produtos Removidos**: {stats.get('removed', 0)}

### Status

Todos os produtos do portal Minerva foram sincronizados com sucesso.
"""
        
        return self.send_notification(title, content)
    
    def notify_scrape_failure(self, error_message: str) -> bool:
        """Notify about scrape failure"""
        title = "❌ Erro no Scraping Minerva"
        
        content = f"""
## Falha no Scraping

**Data/Hora**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

### Erro

```
{error_message}
```

### Ação Necessária

Por favor, verifique os logs e execute o scraper manualmente se necessário.
"""
        
        return self.send_notification(title, content)
    
    def notify_stock_changes(self, out_of_stock: List[Dict], back_in_stock: List[Dict]) -> bool:
        """Notify about stock changes"""
        if not out_of_stock and not back_in_stock:
            return True
            
        title = "📦 Alterações de Estoque Detectadas"
        
        content = f"""
## Mudanças no Estoque

**Data/Hora**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

"""
        
        if out_of_stock:
            content += f"""
### ❌ Produtos Fora de Estoque ({len(out_of_stock)})

"""
            for product in out_of_stock[:10]:  # Limit to 10
                content += f"- **{product['name']}** (SKU: {product['sku']})\n"
                
            if len(out_of_stock) > 10:
                content += f"\n*... e mais {len(out_of_stock) - 10} produtos*\n"
        
        if back_in_stock:
            content += f"""
### ✅ Produtos de Volta ao Estoque ({len(back_in_stock)})

"""
            for product in back_in_stock[:10]:  # Limit to 10
                content += f"- **{product['name']}** (SKU: {product['sku']})\n"
                
            if len(back_in_stock) > 10:
                content += f"\n*... e mais {len(back_in_stock) - 10} produtos*\n"
        
        return self.send_notification(title, content)
    
    def notify_price_changes(self, price_changes: List[Dict]) -> bool:
        """Notify about significant price changes"""
        if not price_changes:
            return True
            
        title = "💰 Alterações de Preço Detectadas"
        
        content = f"""
## Mudanças de Preço

**Data/Hora**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

### Produtos com Alteração de Preço ({len(price_changes)})

"""
        
        for change in price_changes[:15]:  # Limit to 15
            old_price = float(change['old_price'])
            new_price = float(change['new_price'])
            diff = new_price - old_price
            diff_percent = (diff / old_price * 100) if old_price > 0 else 0
            
            emoji = "📈" if diff > 0 else "📉"
            sign = "+" if diff > 0 else ""
            
            content += f"""
**{change['name']}** (SKU: {change['sku']})
- Preço Anterior: R$ {old_price:.2f}
- Preço Novo: R$ {new_price:.2f}
- Variação: {emoji} {sign}R$ {diff:.2f} ({sign}{diff_percent:.1f}%)

"""
        
        if len(price_changes) > 15:
            content += f"\n*... e mais {len(price_changes) - 15} produtos*\n"
        
        return self.send_notification(title, content)
    
    def notify_low_stock_count(self, total_in_stock: int, threshold: int = 50) -> bool:
        """Notify if total products in stock is below threshold"""
        if total_in_stock >= threshold:
            return True
            
        title = "⚠️ Alerta: Poucos Produtos em Estoque"
        
        content = f"""
## Estoque Baixo Detectado

**Data/Hora**: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

### Situação

Apenas **{total_in_stock} produtos** estão em estoque no portal Minerva.

### Ação Recomendada

- Verificar o portal Minerva manualmente
- Contatar o fornecedor se necessário
- Atualizar os clientes sobre disponibilidade limitada
"""
        
        return self.send_notification(title, content)

# Example usage
if __name__ == "__main__":
    service = NotificationService()
    
    # Test notification
    success = service.send_notification(
        "🧪 Teste de Notificação",
        "Este é um teste do sistema de notificações do Fusion Beef."
    )
    
    if success:
        print("✅ Notification system is working!")
    else:
        print("❌ Notification system failed!")
        sys.exit(1)
