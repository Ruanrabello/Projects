# 🌍 Previsão do Tempo

Aplicação web para consultar previsões meteorológicas em tempo real. Utiliza a API OpenWeatherMap para obter dados atualizados.

## 📸 Características

- ✅ Interface limpa e moderna com design responsivo
- ✅ Busca rápida por qualquer cidade do mundo
- ✅ Informações detalhadas: temperatura, umidade, pressão, velocidade do vento
- ✅ Validação de entrada robusta
- ✅ Feedback visual com loader durante carregamento
- ✅ Tratamento de erros amigável em português
- ✅ API segura com CORS restrito
- ✅ Timeout configurável para requisições

## 🏗️ Arquitetura

```
Previsao-Tempo/
├── Backend/                 # API FastAPI
│   ├── main.py             # Endpoint e lógica
│   ├── requirements.txt     # Dependências Python
│   └── .env                # Variáveis de ambiente
├── Frontend/               # Interface web
│   ├── index.html          # HTML com estrutura
│   ├── style.css           # Estilos responsivos
│   ├── script.js           # Lógica JavaScript
│   └── package.json        # Dependências Node
└── .gitignore             # Arquivo de ignores do Git
```

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.9+**
- **Node.js 14+** (opcional, se usar servidor local para frontend)
- **Chave da API OpenWeatherMap** (obtida em https://openweathermap.org/api)

### 1️⃣ Configurar Backend

```bash
# Navegar para o diretório Backend
cd Backend

# Criar arquivo .env com sua chave da API
echo API_KEY="sua_chave_aqui" > .env

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn main.py --host 127.0.0.1 --port 8000 --reload
```

O backend estará disponível em `http://localhost:8000`

### 2️⃣ Servir Frontend

**Opção 1: Servidor local Python**
```bash
cd Frontend
python -m http.server 3000
```
Abra no navegador: `http://localhost:3000`

**Opção 2: Abrir arquivo direto**
```bash
cd Frontend
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

## 📚 Documentação da API

### Endpoint: Obter Previsão

**Requisição:**
```
GET /weather/{cidade}
```

**Parâmetros:**
- `cidade` (string, 2-50 caracteres): Nome da cidade (ex: "São Paulo", "Paris", "Tóquio")

**Exemplo:**
```bash
curl "http://localhost:8000/weather/São%20Paulo"
```

**Resposta (200 OK):**
```json
{
  "Cidade": "São Paulo",
  "País": "BR",
  "Temperatura": 28.5,
  "Descrição": "céu limpo",
  "Umidade": 65,
  "Sensação Térmica": 27.1,
  "Velocidade do Vento": 3.5,
  "Pressão": 1013
}
```

**Erros:**
- `400 Bad Request`: Cidade inválida (menos de 2 caracteres ou caracteres não permitidos)
- `404 Not Found`: Cidade não encontrada
- `503 Service Unavailable`: Serviço de previsão indisponível
- `504 Gateway Timeout`: Timeout ao conectar ao serviço

### Endpoint: Health Check

**Requisição:**
```
GET /health
```

**Resposta:**
```json
{
  "status": "ok"
}
```

## 🔒 Segurança

- **CORS restrito**: Apenas localhost pode acessar a API
- **Validação de entrada**: Cidade validada com regex
- **Timeout**: Requisições têm limite de 10 segundos
- **Sem API_KEY exposta**: Chave armazenada em `.env` (não commitada)
- **Logging**: Erros são registrados no servidor

## 🔧 Variáveis de Ambiente

Crie um arquivo `.env` no diretório `Backend`:

```env
API_KEY=sua_chave_da_api_openweather
```

**Como obter a chave:**
1. Acesse https://openweathermap.org/api
2. Registre-se (gratuitamente)
3. Gere uma API key na sua conta
4. Copie a chave para o arquivo `.env`

## 📦 Dependências

### Backend
- **fastapi** (0.135.3): Framework web moderno
- **uvicorn** (0.44.0): Servidor ASGI
- **requests** (2.32.5): HTTP client
- **python-dotenv** (1.2.2): Carregamento de .env

### Frontend
- Vanilla JavaScript (sem dependências)
- CSS puro com media queries para responsividade

## 🐛 Troubleshooting

### "API_KEY não configurada"
- Verifique se o arquivo `.env` existe em `Backend/`
- Confirme que tem a linha `API_KEY="sua_chave"`

### "Erro de conexão"
- Verifique se o backend está rodando em `http://localhost:8000`
- Tente acessar `http://localhost:8000/health` no navegador

### "Cidade não encontrada"
- Verifique a grafia (OpenWeatherMap é sensível a acentuação)
- Tente usar o nome em inglês (ex: "Sao Paulo" ou "São Paulo")

### "Timeout"
- A API OpenWeatherMap pode estar lenta
- Tente novamente em alguns segundos
- Verifique sua conexão com a internet

### "CORS error no frontend"
- Verifique se o backend está rodando em `http://localhost:8000`
- Verifique se o frontend está em `http://localhost:3000` ou abrindo localmente

## 💡 Melhorias Futuras

- [ ] Previsão de 5 dias
- [ ] Geolocalização automática
- [ ] Favoritos/histórico de buscas
- [ ] Modo escuro
- [ ] Alertas de clima severo
- [ ] Gráficos de temperatura
- [ ] Suporte a múltiplas unidades (Fahrenheit, Kelvin)

## 📄 Licença

Este projeto é educacional e de código aberto.

## ✍️ Autor

Desenvolvido durante estudos de desenvolvimento full-stack.

---

**Dúvidas?** Consulte a documentação do OpenWeatherMap: https://openweathermap.org/api
