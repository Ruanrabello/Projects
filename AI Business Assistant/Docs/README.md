📦 Enterprise AI Assistant

Comandos Importantes:

uvicorn main:app --reload -- Iniciar api local (abrir main.py no terminal) -- Backend
http://127.0.0.1:8000/docs#/ -- para testar os endpoints
cd Frontend; npm run dev -- rodar serve local react  -- Frontend

Links importantes:
link database:https://supabase.com/dashboard/project/ynuyddotzgbpezhvxqil/database/schemas


🤖 Agente de IA
💬 WhatsApp
📄 Leitura de PDFs, Word e Excel
🧠 RAG
📊 Dashboard
👥 Login de usuários
📈 Estatísticas
📂 Upload de documentos
⚙️ Automações (relatórios, e-mails, planilhas)
🔌 Integração com APIs



Minha proposta

Vamos desenvolver como uma empresa faria:

Sprint 1: Estrutura e interface  -- Foi
    obs: hj existe dados mockados, principalmete ali no sidebar nas conersas recentes, dp que o backend tiver pronto vc pode deletar a pasta data e conectar aos dados reais

Sprint 2: Backend (FastAPI) -- Em andamento
    aonde parei conectei o sidebar das conversas recentes com o banco
    Parei na parte que vou Criar um botao chamado nova conversa e a ia vai gerar um titulo IA gera automaticamente (mais profissional)


Sprint 3: Banco de dados
Sprint 4: Autenticação
    principalmente em services e chat pq atualmente esta pegando os usuarios so do id 1 e precisa ser conforme logar, porem precisa do sistema para logar
Sprint 5: IA (Ollama + RAG)
Sprint 6: WhatsApp
Sprint 7: Automações
Sprint 8: Docker e Deploy

Outras pendencias:

VERIFICAR O GITIGNORE, PQ VC JA SUBIU NO GITHUB UMA VERSAO, DEPENDENDO VAI PRECISAR DELETAR E SUBIR DNV

consolitar as variaveis com tipos no arquivo tipos

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dps verificar isso que colocou no seu main.py pq ele abre muitas portas de seguranca






organizacao das tabelas banco:
┌──────────────────────────────┐
│          usuarios            │
├──────────────────────────────┤
│ id                           │
│ nome                         │
│ email                        │
│ created_at                   │
└───────────────┬──────────────┘
                │ 1:N
                │
                ▼
┌──────────────────────────────┐
│         conversas            │
├──────────────────────────────┤
│ id                           │
│ titulo                       │
│ usuario_id                   │
│ created_at                   │
└───────────────┬──────────────┘
                │ 1:N
                │
                ▼
┌──────────────────────────────┐
│         mensagens            │
├──────────────────────────────┤
│ id                           │
│ conversa_id                  │
│ usuario ("user"/"ai")        │
│ texto                        │
│ created_at                   │
└──────────────────────────────┘


┌──────────────────────────────┐
│        documentos            │
├──────────────────────────────┤
│ id                           │
│ nome                         │
│ tipo                         │
│ caminho_storage              │
│ status                       │
│ created_at                   │
└──────────────────────────────┘

