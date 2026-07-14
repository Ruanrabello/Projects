/* Esse componente representa uma mensagem. */
type MensagemChatPropriedades = {
    texto: string;
    usuario: "user" | "ai";
};

function MensagemChat({texto, usuario}: MensagemChatPropriedades) {

    const isUser = usuario === "user";
    return (
        <div
            className={`flex ${
            isUser ? "justify-end" : "justify-start"
            }`}
        >
         <div
            className={`
                max-w-[70%]
                rounded-xl
                px-4
                py-3
                ${
                    isUser
                    ? "bg-cyan-500 text-white"
                    : "bg-slate-800 text-slate-200"
                }
            `}
      >
        {texto}
      </div>

        </div>

    );
}

export default MensagemChat
