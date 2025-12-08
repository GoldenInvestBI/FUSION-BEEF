import { useState, useEffect } from "react";
import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { ChevronDown, Search, X } from "lucide-react";

interface Product {
  sku: string;
  nome: string;
  preco_venda_kg: number;
  image_filename: string;
  imagem_url?: string;
  categoria?: string;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>("todas");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<'nome' | 'preco_asc' | 'preco_desc'>('nome');
  const [categories, setCategories] = useState<string[]>([]);

  // Filtrar e ordenar produtos
  const filteredProducts = (() => {
    let filtered = products.filter((product) => {
      const matchesSearch = product.nome.toLowerCase().includes(searchQuery.toLowerCase()) ||
                           product.sku.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = selectedCategory === 'todas' || product.categoria === selectedCategory;
      return matchesSearch && matchesCategory;
    });

    if (sortBy === 'preco_asc') {
      filtered.sort((a, b) => a.preco_venda_kg - b.preco_venda_kg);
    } else if (sortBy === 'preco_desc') {
      filtered.sort((a, b) => b.preco_venda_kg - a.preco_venda_kg);
    } else {
      filtered.sort((a, b) => a.nome.localeCompare(b.nome));
    }

    return filtered;
  })();

  useEffect(() => {
    fetch("/produtos_em_estoque_60percent.json")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        
        const cats = new Set<string>();
        data.forEach((p: Product) => {
          if (p.categoria) cats.add(p.categoria);
        });
        setCategories(Array.from(cats).sort());
        
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar produtos:", err);
        setLoading(false);
      });
  }, []);

  const handleWhatsApp = (productName: string, sku: string) => {
    const message = `Olá! Tenho interesse no produto: ${productName} (SKU: ${sku})`;
    const whatsappUrl = `https://wa.me/5527996187603?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, "_blank");
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="border-b border-border/30 bg-background/95 backdrop-blur-sm sticky top-0 z-50">
        <div className="container py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src="/logo_original.jpg" alt="Fusion Beef" className="h-16 w-auto object-contain rounded-full" />
            <span className="text-xl font-bold text-accent">FUSION</span>
          </div>
          <nav className="flex gap-8">
            <a href="#produtos" className="text-foreground hover:text-accent transition-colors">Produtos</a>
            <a href="#sobre" className="text-foreground hover:text-accent transition-colors">Sobre</a>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="relative h-96 bg-gradient-to-b from-background to-background/50 flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <img src="/images/hero-bg.jpg" alt="" className="w-full h-full object-cover" />
        </div>
        <div className="relative z-10 text-center">
          <h1 className="text-5xl font-bold text-accent mb-4">Excelência em Carnes Premium</h1>
          <p className="text-xl text-muted-foreground mb-8">Seleção exclusiva de bovinos premium para os mais exigentes</p>
          <Button className="bg-accent hover:bg-accent/90 text-background">Explorar Catálogo</Button>
        </div>
      </section>

      {/* Produtos */}
      <section id="produtos" className="py-16 bg-background">
        <div className="container">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-accent mb-2">Nossos Produtos</h2>
            <p className="text-muted-foreground">{filteredProducts.length} de {products.length} produtos selecionados em estoque</p>
          </div>

          {/* Filtros e Ordenação */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
            {/* Pesquisa */}
            <div className="sm:col-span-1">
              <label className="block text-sm text-muted-foreground mb-2">Pesquisar</label>
              <div className="relative">
                <Search className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Nome ou SKU..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-10 py-2 bg-background border border-border/30 rounded-lg text-foreground focus:outline-none focus:border-accent/50"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-3 top-3 text-muted-foreground hover:text-foreground"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>
            </div>

            {/* Ordenação */}
            <div className="sm:col-span-1">
              <label className="block text-sm text-muted-foreground mb-2">Ordenar por</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="w-full px-4 py-2 bg-background border border-border/30 rounded-lg text-foreground focus:outline-none focus:border-accent/50"
              >
                <option value="nome">Nome (A-Z)</option>
                <option value="preco_asc">Preço (Menor)</option>
                <option value="preco_desc">Preço (Maior)</option>
              </select>
            </div>

            {/* Categoria */}
            {categories.length > 0 && (
              <div className="sm:col-span-1">
                <label className="block text-sm text-muted-foreground mb-2">Categoria</label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-4 py-2 bg-background border border-border/30 rounded-lg text-foreground focus:outline-none focus:border-accent/50"
                >
                  <option value="todas">Todas</option>
                  {categories.map((cat) => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Grid de Produtos */}
          {loading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Carregando produtos...</p>
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Nenhum produto encontrado</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProducts.map((product) => (
                <Link key={product.sku} href={`/produto/${product.sku}`}>
                  <div className="group bg-card border border-border/30 rounded-lg overflow-hidden hover:shadow-2xl transition-all duration-300 hover:border-accent/50 cursor-pointer">
                    {/* Imagem */}
                    <div className="relative h-64 bg-black overflow-hidden flex items-center justify-center">
                      {product.imagem_url ? (
                        <img
                          src={product.imagem_url}
                          alt={product.nome}
                          className="max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-300"
                          style={{ imageRendering: 'crisp-edges' }}
                          loading="lazy"
                        />
                      ) : product.image_filename && product.image_filename !== "IMAGEM_INDISPONIVEL.png" ? (
                        <img
                          src={`/images/${product.image_filename}`}
                          alt={product.nome}
                          className="max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-300"
                          style={{ imageRendering: 'crisp-edges' }}
                          loading="lazy"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center bg-black">
                          <span className="text-muted-foreground">Imagem indisponível</span>
                        </div>
                      )}
                    </div>

                    {/* Info */}
                    <div className="p-6">
                      <h3 className="text-lg font-semibold text-foreground mb-2 line-clamp-2 group-hover:text-accent transition-colors">
                        {product.nome}
                      </h3>
                      <p className="text-sm text-muted-foreground mb-4">SKU: {product.sku}</p>
                      <p className="text-2xl font-bold text-accent mb-6">R$ {product.preco_venda_kg.toFixed(2)}/kg</p>
                      <Button
                        onClick={(e) => {
                          e.preventDefault();
                          handleWhatsApp(product.nome, product.sku);
                        }}
                        className="w-full bg-accent hover:bg-accent/90 text-background"
                      >
                        Solicitar Orçamento
                      </Button>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Sobre */}
      <section id="sobre" className="py-16 bg-card border-t border-border/30">
        <div className="container">
          <h2 className="text-3xl font-bold text-accent mb-8">Sobre a Fusion Beef</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <p className="text-foreground mb-4">
                A <strong>Fusion Beef</strong> é uma empresa especializada em comercialização de carnes bovinas premium, oferecendo uma seleção exclusiva de produtos de alta qualidade para os mais exigentes clientes.
              </p>
              <p className="text-foreground mb-4">
                Nossos produtos são cuidadosamente selecionados de fornecedores renomados, garantindo qualidade, frescor e sabor incomparável em cada corte.
              </p>
            </div>
            <div>
              <p className="text-foreground mb-4">
                Com um portfólio diversificado de bovinos premium, estamos comprometidos em fornecer as melhores opções para restaurantes, churrascarias e clientes corporativos.
              </p>
              <p className="text-foreground">
                Cada produto é selecionado com rigor, garantindo que apenas o melhor chegue à sua mesa.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Contato */}
      <section className="py-16 bg-background border-t border-border/30">
        <div className="container text-center">
          <h2 className="text-3xl font-bold text-accent mb-8">Entre em Contato</h2>
          <p className="text-foreground mb-8">Para solicitar orçamentos e informações sobre nossos produtos, entre em contato com nosso representante:</p>
          <div className="bg-card border border-border/30 rounded-lg p-8 max-w-md mx-auto">
            <h3 className="text-2xl font-bold text-accent mb-2">Valckenborgh Borges</h3>
            <p className="text-muted-foreground mb-6">Gerente de Vendas - Fusion Beef</p>
            <Button
              onClick={() => window.open("https://wa.me/5527996187603", "_blank")}
              className="w-full bg-accent hover:bg-accent/90 text-background"
            >
              Enviar Mensagem via WhatsApp
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
