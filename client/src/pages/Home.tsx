import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronDown, Search, X } from "lucide-react";

interface Product {
  sku: string;
  nome: string;
  preco_venda_kg: number;
  image_filename: string;
  imagem_url?: string;
}

/**
 * Design: Luxo Rústico Premium
 * - Tipografia: Playfair Display (títulos), Lora (corpo), Montserrat (acentos)
 * - Cores: Marrom escuro, ouro/cobre, bege claro
 * - Textura: Fundo com textura de couro
 * - Layout: Assimétrico com imagens grandes e impactantes
 */
export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  // Filtrar produtos baseado na pesquisa
  const filteredProducts = products.filter((product) =>
    product.nome.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.sku.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    // Carregar dados dos produtos
    fetch("/produtos_em_estoque_60percent.json")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar produtos:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header com Logo */}
      <header className="border-b border-border/30 bg-background/95 backdrop-blur-sm sticky top-0 z-50">
        <div className="container py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="/fusion-beef-logo.png"
              alt="Fusion Beef Logo"
              className="h-20 w-20"
            />
          </div>
          <nav className="hidden md:flex gap-8">
            <a href="#produtos" className="text-foreground hover:text-accent transition-colors">
              Produtos
            </a>
            <a href="#sobre" className="text-foreground hover:text-accent transition-colors">
              Sobre
            </a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="/hero-banner.jpg"
            alt="Premium Beef Cuts"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/40"></div>
        </div>

        <div className="relative z-10 text-center max-w-2xl mx-auto px-4">
          <h2 className="text-6xl md:text-7xl font-bold text-accent mb-6 drop-shadow-lg">
            Excelência em Carnes Premium
          </h2>
          <p className="text-xl md:text-2xl text-foreground mb-8 drop-shadow-md">
            Seleção exclusiva de bovinos premium para os mais exigentes
          </p>
          <a href="#produtos">
            <Button
              size="lg"
              className="bg-accent hover:bg-accent/90 text-accent-foreground text-lg px-8"
            >
              Explorar Catálogo
              <ChevronDown className="ml-2 h-5 w-5" />
            </Button>
          </a>
        </div>
      </section>

      {/* Seção de Produtos */}
      <section id="produtos" className="py-20 bg-background">
        <div className="container">
          <div className="mb-16 text-center">
            <h2 className="text-5xl font-bold text-accent mb-4">
              Nossos Produtos
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              {products.length} produtos selecionados em estoque, prontos para
              sua mesa
            </p>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <p className="text-lg text-muted-foreground">Carregando produtos...</p>
            </div>
          ) : (
            <>
              {/* Campo de Pesquisa */}
              <div className="mb-8 flex items-center gap-2">
                <div className="relative flex-1 max-w-md">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <input
                    type="text"
                    placeholder="Pesquisar produtos por nome ou SKU..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-10 py-2 rounded-lg border border-border/30 bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery("")}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  )}
                </div>
                <span className="text-sm text-muted-foreground ml-4">
                  {filteredProducts.length} de {products.length} produtos
                </span>
              </div>

              {/* Mensagem quando nenhum produto é encontrado */}
              {filteredProducts.length === 0 ? (
                <div className="text-center py-12 col-span-full">
                  <p className="text-lg text-muted-foreground">Nenhum produto encontrado para "{searchQuery}"</p>
                  <Button
                    variant="outline"
                    className="mt-4 border-accent text-accent hover:bg-accent hover:text-accent-foreground"
                    onClick={() => setSearchQuery("")}
                  >
                    Limpar Pesquisa
                  </Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 col-span-full">
                  {filteredProducts.map((product) => (
                <div
                  key={product.sku}
                  className="group bg-card border border-border/30 rounded-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:border-accent/50"
                >
                  {/* Imagem do Produto */}
                  <div className="relative h-64 bg-black overflow-hidden">
                    {product.imagem_url ? (
                      <img
                        src={product.imagem_url}
                        alt={product.nome}
                        className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 bg-black"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = '/images/placeholder.png';
                        }}
                      />
                    ) : product.image_filename && product.image_filename !== "IMAGEM_INDISPONIVEL.png" ? (
                      <img
                        src={`/images/${product.image_filename}`}
                        alt={product.nome}
                        className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 bg-black"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-black">
                        <span className="text-muted-foreground">Imagem indisponível</span>
                      </div>
                    )}
                  </div>

                  {/* Informações do Produto */}
                  <div className="p-6">
                    <h3 className="text-lg font-semibold text-foreground mb-2 line-clamp-2 group-hover:text-accent transition-colors">
                      {product.nome}
                    </h3>

                    <div className="flex items-baseline justify-between mb-4">
                      <span className="text-sm text-muted-foreground">SKU: {product.sku}</span>
                    </div>

                    <div className="border-t border-border/30 pt-4">
                      <div className="flex items-baseline justify-between">
                        <span className="text-sm text-muted-foreground">Preço por Kg</span>
                        <span className="text-2xl font-bold text-accent">
                          R$ {product.preco_venda_kg.toFixed(2)}
                        </span>
                      </div>
                    </div>

                    <Button
                      variant="outline"
                      className="w-full mt-6 border-accent text-accent hover:bg-accent hover:text-accent-foreground cursor-pointer"
                      onClick={() => {
                        const message = `Olá Valckenborgh, gostaria de solicitar um orçamento para o produto: ${product.nome} (SKU: ${product.sku})`;
                        window.open(
                          `https://wa.me/5527996187603?text=${encodeURIComponent(message)}`,
                          '_blank'
                        );
                      }}
                    >
                      Solicitar Orçamento
                    </Button>
                  </div>
                </div>
                ))}
                </div>
              )}
            </>
          )}
        </div>
      </section>

      {/* Seção Sobre */}
      <section id="sobre" className="py-20 bg-secondary/10 border-t border-border/30">
        <div className="container max-w-3xl">
          <h2 className="text-4xl font-bold text-accent mb-8 text-center">
            Sobre a Fusion Beef
          </h2>

          <div className="prose prose-invert max-w-none text-foreground">
            <p className="text-lg leading-relaxed mb-6">
              A <strong>Fusion Beef</strong> é uma empresa especializada em
              comercialização de carnes bovinas premium, oferecendo uma seleção
              exclusiva de produtos de alta qualidade para os mais exigentes
              clientes.
            </p>

            <p className="text-lg leading-relaxed mb-6">
              Nossos produtos são cuidadosamente selecionados de fornecedores
              renomados, garantindo qualidade, frescor e sabor incomparável em
              cada corte.
            </p>

            <p className="text-lg leading-relaxed">
              Com um portfólio diversificado de bovinos premium, estamos
              comprometidos em fornecer as melhores opções para restaurantes,
              churrascarias e clientes corporativos.
            </p>
          </div>
        </div>
      </section>

      {/* Seção de Contato */}
      <section className="bg-secondary/20 border-t border-border/30 py-16">
        <div className="container max-w-2xl">
          <h2 className="text-4xl font-bold text-accent mb-8 text-center">
            Entre em Contato
          </h2>

          <div className="bg-card border border-border/30 rounded-lg p-8 text-center">
            <p className="text-lg text-foreground mb-6">
              Para solicitar orçamentos e informações sobre nossos produtos,
              entre em contato com nosso representante:
            </p>

            <div className="mb-8">
              <h3 className="text-2xl font-bold text-accent mb-2">
                Valckenborgh Borges
              </h3>
              <p className="text-lg text-muted-foreground mb-6">
                Gerente de Vendas - Fusion Beef
              </p>

              <div className="flex items-center justify-center gap-3 mb-6">
                <svg
                  className="w-6 h-6 text-accent"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.67-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.076 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.403h-.004a9.87 9.87 0 00-4.255.949c-1.238.503-2.37 1.236-3.355 2.22-1.798 1.799-2.823 4.15-2.823 6.556 0 2.405 1.025 4.757 2.823 6.555 1.798 1.798 4.15 2.823 6.556 2.823 2.405 0 4.757-1.025 6.556-2.823 1.798-1.798 2.823-4.15 2.823-6.556 0-2.405-1.025-4.757-2.823-6.556-.984-.984-2.117-1.717-3.355-2.22a9.87 9.87 0 00-4.255-.949" />
                </svg>
                <a
                  href="https://wa.me/5527996187603?text=Olá%20Valckenborgh%2C%20gostaria%20de%20solicitar%20um%20orçamento%20de%20produtos%20Fusion%20Beef"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xl font-bold text-accent hover:text-accent/80 transition-colors"
                >
                  (27) 99618-7603
                </a>
              </div>

              <p className="text-sm text-muted-foreground bg-accent/10 border border-accent/20 rounded px-4 py-3">
                ⚠️ <strong>Contato exclusivamente via WhatsApp</strong>
              </p>
            </div>

            <Button
              size="lg"
              className="bg-accent hover:bg-accent/90 text-accent-foreground"
              onClick={() => {
                window.open(
                  'https://wa.me/5527996187603?text=Olá%20Valckenborgh%2C%20gostaria%20de%20solicitar%20um%20orçamento%20de%20produtos%20Fusion%20Beef',
                  '_blank'
                );
              }}
            >
              Enviar Mensagem via WhatsApp
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-background border-t border-border/30 py-12">
        <div className="container text-center">
          <p className="text-muted-foreground mb-4">
            © 2024 Fusion Beef - Prime Cuts & Grill. Todos os direitos
            reservados.
          </p>
          <p className="text-sm text-muted-foreground">
            Contato: Valckenborgh Borges | WhatsApp: (27) 99618-7603
          </p>
        </div>
      </footer>
    </div>
  );
}
