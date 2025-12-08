import { useState, useEffect } from "react";
import AdminLogin from "@/components/AdminLogin";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "sonner";
import { RefreshCw, Settings, Database, TrendingUp } from "lucide-react";

export default function Admin() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [newMarkup, setNewMarkup] = useState("60");

  useEffect(() => {
    const loggedIn = localStorage.getItem("admin_logged_in") === "true";
    setIsAuthenticated(loggedIn);
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_logged_in");
    setIsAuthenticated(false);
    toast.success("Logout realizado com sucesso!");
  };
  
  const { data: products = [] } = trpc.products.getAll.useQuery({ inStockOnly: false });
  const { data: logs = [] } = trpc.products.getScrapeLogs.useQuery({ limit: 20 });
  const { data: settings = {} } = trpc.products.getSettings.useQuery();
  
  const updateMarkupMutation = trpc.products.updateMarkup.useMutation({
    onSuccess: (data) => {
      toast.success(`Markup atualizado! ${data.updatedCount} produtos recalculados.`);
    },
    onError: (error) => {
      toast.error(`Erro ao atualizar markup: ${error.message}`);
    },
  });

  const handleUpdateMarkup = () => {
    const markup = parseFloat(newMarkup);
    if (isNaN(markup) || markup < 0 || markup > 200) {
      toast.error("Markup deve ser um número entre 0 e 200");
      return;
    }
    updateMarkupMutation.mutate({ markup });
  };

  // Show login screen if not authenticated
  if (!isAuthenticated) {
    return <AdminLogin onLogin={handleLogin} />;
  }

  const currentMarkup = settings.default_markup || "60";
  const inStockCount = products.filter((p: any) => p.inStock === 1).length;
  const totalProducts = products.length;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/30 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-accent">Admin Dashboard</h1>
            <p className="text-sm text-muted-foreground">Painel Administrativo - Fusion Beef</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => window.location.href = "/"}>
              Voltar ao Site
            </Button>
            <Button variant="destructive" onClick={handleLogout}>
              Sair
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Produtos em Estoque</CardTitle>
              <Database className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{inStockCount}</div>
              <p className="text-xs text-muted-foreground">
                de {totalProducts} produtos totais
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Markup Atual</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{currentMarkup}%</div>
              <p className="text-xs text-muted-foreground">
                Aplicado a todos os produtos
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Última Atualização</CardTitle>
              <RefreshCw className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {logs.length > 0 ? new Date(logs[0].createdAt).toLocaleDateString('pt-BR') : 'N/A'}
              </div>
              <p className="text-xs text-muted-foreground">
                Último scraping do Minerva
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="settings" className="space-y-4">
          <TabsList>
            <TabsTrigger value="settings">
              <Settings className="h-4 w-4 mr-2" />
              Configurações
            </TabsTrigger>
            <TabsTrigger value="products">
              <Database className="h-4 w-4 mr-2" />
              Produtos
            </TabsTrigger>
            <TabsTrigger value="logs">
              <RefreshCw className="h-4 w-4 mr-2" />
              Logs de Scraping
            </TabsTrigger>
          </TabsList>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Ajustar Markup</CardTitle>
                <CardDescription>
                  Altere o markup aplicado a todos os produtos. Os preços serão recalculados automaticamente.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="markup">Markup (%)</Label>
                  <Input
                    id="markup"
                    type="number"
                    min="0"
                    max="200"
                    value={newMarkup}
                    onChange={(e) => setNewMarkup(e.target.value)}
                    placeholder="60"
                  />
                  <p className="text-sm text-muted-foreground">
                    Markup atual: {currentMarkup}%
                  </p>
                </div>
                <Button
                  onClick={handleUpdateMarkup}
                  disabled={updateMarkupMutation.isPending}
                  className="w-full"
                >
                  {updateMarkupMutation.isPending ? "Atualizando..." : "Atualizar Markup"}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Forçar Atualização de Estoque</CardTitle>
                <CardDescription>
                  Execute o scraper manualmente para buscar novos produtos do Minerva.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full" disabled>
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Executar Scraper (Em breve)
                </Button>
                <p className="text-sm text-muted-foreground mt-2">
                  O scraper automático roda a cada 2 horas no servidor.
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Products Tab */}
          <TabsContent value="products" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Lista de Produtos</CardTitle>
                <CardDescription>
                  {inStockCount} produtos em estoque de {totalProducts} totais
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {products.map((product: any) => (
                    <div
                      key={product.id}
                      className="flex items-center justify-between p-3 border border-border rounded-lg"
                    >
                      <div className="flex-1">
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-muted-foreground">
                          SKU: {product.sku} | {product.category}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-accent">
                          R$ {parseFloat(product.priceWithMarkup).toFixed(2)}/kg
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Original: R$ {parseFloat(product.priceOriginal).toFixed(2)}
                        </p>
                      </div>
                      <div className="ml-4">
                        {product.inStock === 1 ? (
                          <span className="px-2 py-1 text-xs bg-green-500/20 text-green-500 rounded">
                            Em Estoque
                          </span>
                        ) : (
                          <span className="px-2 py-1 text-xs bg-red-500/20 text-red-500 rounded">
                            Fora de Estoque
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Logs Tab */}
          <TabsContent value="logs" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Histórico de Scraping</CardTitle>
                <CardDescription>
                  Últimas 20 execuções do scraper do Minerva
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {logs.length === 0 ? (
                    <p className="text-center text-muted-foreground py-8">
                      Nenhum log de scraping encontrado
                    </p>
                  ) : (
                    logs.map((log: any) => (
                      <div
                        key={log.id}
                        className="flex items-center justify-between p-3 border border-border rounded-lg"
                      >
                        <div>
                          <p className="font-medium">
                            {new Date(log.createdAt).toLocaleString('pt-BR')}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {log.productsFound} produtos encontrados | {log.productsUpdated} atualizados
                          </p>
                        </div>
                        <div>
                          {log.status === 'success' ? (
                            <span className="px-2 py-1 text-xs bg-green-500/20 text-green-500 rounded">
                              Sucesso
                            </span>
                          ) : (
                            <span className="px-2 py-1 text-xs bg-red-500/20 text-red-500 rounded">
                              Erro
                            </span>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
