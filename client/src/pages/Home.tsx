import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ChevronDown } from "lucide-react";

interface Product {
  sku: string;
  nome: string;
  preco_venda_kg: number;
  image_filename: string;
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

  useEffect(() => {
    // Carregar dados dos produtos
    fetch("/produtos_em_estoque.json")
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
              src="/Gemini_Generated_Image_5w0vd85w0vd85w0v.png"
              alt="Fusion Beef Logo"
              className="h-12 w-12"
            />
            <div>
              <h1 className="text-2xl font-bold text-accent">Fusion Beef</h1>
              <p className="text-sm text-muted-foreground">Prime Cuts & Grill</p>
            </div>
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.map((product) => (
                <div
                  key={product.sku}
                  className="group bg-card border border-border/30 rounded-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:border-accent/50"
                >
                  {/* Imagem do Produto */}
                  <div className="relative h-64 bg-secondary/20 overflow-hidden">
                    {product.image_filename && product.image_filename !== "IMAGEM_INDISPONIVEL.png" ? (
                      <img
                        src={`/images/${product.image_filename}`}
                        alt={product.nome}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-secondary to-secondary/50">
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
                      className="w-full mt-6 border-accent text-accent hover:bg-accent hover:text-accent-foreground"
                    >
                      Solicitar Orçamento
                    </Button>
                  </div>
                </div>
              ))}
            </div>
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

      {/* Footer */}
      <footer className="bg-background border-t border-border/30 py-12">
        <div className="container text-center">
          <p className="text-muted-foreground mb-4">
            © 2024 Fusion Beef - Prime Cuts & Grill. Todos os direitos
            reservados.
          </p>
          <p className="text-sm text-muted-foreground">
            Para dúvidas ou solicitações, entre em contato conosco.
          </p>
        </div>
      </footer>
    </div>
  );
}
