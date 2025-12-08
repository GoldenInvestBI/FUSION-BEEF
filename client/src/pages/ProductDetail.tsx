import { useEffect, useState } from 'react';
import { useRoute } from 'wouter';
import { Button } from '@/components/ui/button';
import { Share2, ArrowLeft, MessageCircle } from 'lucide-react';

interface Product {
  sku: string;
  nome: string;
  preco_venda_kg: number;
  imagem_url?: string;
  image_filename?: string;
  categoria?: string;
}

export default function ProductDetail() {
  const [, params] = useRoute('/produto/:sku');
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch('/produtos_em_estoque_60percent.json');
        const products = await response.json();
        const found = products.find((p: Product) => p.sku === params?.sku);
        setProduct(found || null);
      } catch (error) {
        console.error('Erro ao carregar produto:', error);
      } finally {
        setLoading(false);
      }
    };

    if (params?.sku) {
      fetchProduct();
    }
  }, [params?.sku]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-foreground">Carregando...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-foreground mb-4">Produto não encontrado</h1>
          <a href="/" className="text-accent hover:underline">Voltar ao catálogo</a>
        </div>
      </div>
    );
  }

  const handleWhatsApp = () => {
    const message = `Olá! Tenho interesse no produto: ${product.nome} (SKU: ${product.sku})`;
    const whatsappUrl = `https://wa.me/5511999999999?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/95 backdrop-blur border-b border-border/30">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <a href="/" className="flex items-center gap-2 text-accent hover:text-accent/80 transition-colors">
            <ArrowLeft className="w-5 h-5" />
            <span>Voltar</span>
          </a>
          <h1 className="text-lg font-semibold text-foreground">Detalhes do Produto</h1>
          <div className="w-20" />
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Imagem */}
          <div className="flex items-center justify-center">
            <div className="w-full aspect-square bg-black rounded-lg overflow-hidden flex items-center justify-center">
              {product.imagem_url ? (
                <img
                  src={product.imagem_url}
                  alt={product.nome}
                  className="w-full h-full object-contain"
                />
              ) : product.image_filename ? (
                <img
                  src={`/images/${product.image_filename}`}
                  alt={product.nome}
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-muted-foreground">Imagem indisponível</div>
              )}
            </div>
          </div>

          {/* Informações */}
          <div className="space-y-6">
            {/* Título e SKU */}
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">{product.nome}</h1>
              <p className="text-muted-foreground">SKU: {product.sku}</p>
            </div>

            {/* Preço */}
            <div className="bg-card border border-border/30 rounded-lg p-6">
              <p className="text-muted-foreground text-sm mb-2">Preço por KG</p>
              <p className="text-4xl font-bold text-accent">R$ {product.preco_venda_kg.toFixed(2)}</p>
            </div>

            {/* Descrição */}
            <div className="bg-card border border-border/30 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Características</h3>
              <ul className="space-y-2 text-foreground">
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Bovino Premium de alta qualidade</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Selecionado de fornecedores renomados</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Garantia de frescor e sabor incomparável</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-accent mt-1">•</span>
                  <span>Ideal para restaurantes e churrascarias</span>
                </li>
              </ul>
            </div>

            {/* Ações */}
            <div className="flex gap-3">
              <Button
                onClick={handleWhatsApp}
                className="flex-1 bg-accent hover:bg-accent/90 text-background gap-2"
              >
                <MessageCircle className="w-4 h-4" />
                Solicitar Orçamento
              </Button>
              <Button
                variant="outline"
                className="px-4"
              >
                <Share2 className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
