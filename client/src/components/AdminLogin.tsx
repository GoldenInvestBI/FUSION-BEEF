import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Lock } from "lucide-react";

interface AdminLoginProps {
  onLogin: () => void;
}

export default function AdminLogin({ onLogin }: AdminLoginProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Credenciais hardcoded (em produção, usar autenticação real)
    const ADMIN_USERNAME = "admin";
    const ADMIN_PASSWORD = "fusion2024";

    setTimeout(() => {
      if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
        localStorage.setItem("admin_logged_in", "true");
        toast.success("Login realizado com sucesso!");
        onLogin();
      } else {
        toast.error("Usuário ou senha incorretos");
      }
      setLoading(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-orange-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-2xl border-amber-200">
        <CardHeader className="space-y-3 text-center">
          <div className="mx-auto w-16 h-16 bg-amber-600 rounded-full flex items-center justify-center">
            <Lock className="w-8 h-8 text-white" />
          </div>
          <CardTitle className="text-3xl font-bold text-amber-900">
            Painel Administrativo
          </CardTitle>
          <CardDescription className="text-base">
            Fusion Beef - Área Restrita
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-sm font-medium">
                Usuário
              </Label>
              <Input
                id="username"
                type="text"
                placeholder="Digite seu usuário"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="h-12"
                autoComplete="username"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-sm font-medium">
                Senha
              </Label>
              <Input
                id="password"
                type="password"
                placeholder="Digite sua senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="h-12"
                autoComplete="current-password"
              />
            </div>
            <Button
              type="submit"
              className="w-full h-12 bg-amber-600 hover:bg-amber-700 text-white font-semibold text-base"
              disabled={loading}
            >
              {loading ? "Entrando..." : "Entrar"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
