import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import ProductDetail from "./pages/ProductDetail";


function Router() {
  return (
    <Switch>
       <Route path="/" component={Home} />
      <Route path="/produto/:sku" component={ProductDetail} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

/**
 * Design: Luxo Rústico Premium
 * - Tema: Light (fundo escuro marrom, texto bege claro)
 * - Paleta: Marrom escuro, ouro/cobre, bege claro
 * - Tipografia: Playfair Display (títulos), Lora (corpo), Montserrat (acentos)
 */
function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
