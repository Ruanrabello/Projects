function Configurações() {
  return (
    <div className="max-w-4xl">

      <h1 className="text-3xl font-bold">
        Configurações
      </h1>

      <p className="text-slate-400 mt-2">
        Gerencie as configurações do seu assistente de IA.
      </p>

      {/* Perfil */}
      <div className="mt-10 rounded-xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="text-xl font-semibold">
          👤 Perfil
        </h2>

        <div className="mt-5">

          <label className="text-sm text-slate-400">
            Nome
          </label>

          <input
            type="text"
            placeholder="Seu nome"
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-cyan-500"
          />

        </div>

      </div>

      {/* IA */}

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="text-xl font-semibold">
          🤖 Modelo de IA
        </h2>

        <select
          className="mt-5 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3"
        >
          <option>GPT-4o</option>
          <option>GPT-4.1</option>
          <option>GPT-4.1 Mini</option>
        </select>

      </div>

      {/* Documentos */}

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="text-xl font-semibold">
          📄 Documentos
        </h2>

        <div className="mt-5">

          <label className="text-sm text-slate-400">
            Tamanho máximo
          </label>

          <input
            type="number"
            defaultValue={20}
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3"
          />

        </div>

        <div className="mt-5">

          <label className="text-sm text-slate-400">
            Formatos permitidos
          </label>

          <input
            type="text"
            defaultValue="PDF, DOCX, XLSX"
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3"
          />

        </div>

      </div>

      {/* API */}

      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="text-xl font-semibold">
          🔑 API
        </h2>

        <div className="mt-5">

          <label className="text-sm text-slate-400">
            Chave da OpenAI
          </label>

          <input
            type="password"
            placeholder="sk-********************************"
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3"
          />

        </div>

        <button
          className="mt-6 rounded-lg bg-cyan-500 px-5 py-3 font-medium hover:bg-cyan-600 transition"
        >
          Testar conexão
        </button>

      </div>

    </div>
  );
}

export default Configurações;
