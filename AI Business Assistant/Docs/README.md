📦 Enterprise AI Assistant

Como esse projeto vai ser o seu principal projeto de portfólio, eu gostaria que ele tivesse um nível profissional desde o início.

Em vez de criar apenas um chatbot, vamos construir uma plataforma SaaS completa. Pense em algo como um "ChatGPT para empresas", com:

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

Isso demonstra muito mais conhecimento do que um chatbot simples.

Minha proposta

Vamos desenvolver como uma empresa faria:

Sprint 1: Estrutura e interface  -- Foi
    obs: hj existe dados mockados, principalmete ali no sidebar nas conersas recentes, dp que o backend tiver pronto vc pode deletar a pasta data e conectar aos dados reais
Sprint 2: Backend (FastAPI)

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


Sprint 3: Banco de dados
Sprint 4: Autenticação
    principalmente em services e chat pq ta pegadno os usuarios so do id 1 e precisa ser conforme logar
Sprint 5: IA (Ollama + RAG)
Sprint 6: WhatsApp
Sprint 7: Automações
Sprint 8: Docker e Deploy




Comandos:
uvicorn main:app --reload -- Iniciar api local (abrir main.py no terminal) -- Backend
http://127.0.0.1:8000/docs#/ -- para testar os endpoints
cd Frontend; npm run dev -- rodar serve local react  -- Frontend

link database:https://supabase.com/dashboard/project/ynuyddotzgbpezhvxqil/database/schemas
