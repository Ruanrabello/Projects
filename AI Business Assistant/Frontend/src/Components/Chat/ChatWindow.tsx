import ChatInput from "./ChatInput";
import { useState } from "react";
import MensagemChat from "./ChatMessage";


type MensagemChatPropriedades = {
    id: number;
    usuario: "user" | "ai";
    texto: string;
};

type ChatWindowProps = {
  conversaId?: string;
};


function ChatWindow({ conversaId }: ChatWindowProps){

const [mensagens, setMensagens] = useState<MensagemChatPropriedades[]>([
  {
    id: 1,
    usuario: "ai",
    texto: "Olá! Sou seu assistente de IA. Como posso ajudar?",
  },
]);

<h1>{conversaId}</h1>

const [texto, setTexto] = useState("");

function enviarMensagem() {
  if (texto.trim() === "") return;

  const novaMensagem = {
    id: mensagens.length + 1,
    usuario: "user" as const,
    texto: texto,
  };

  setMensagens([...mensagens, novaMensagem]);

  setTexto("");
}

return (

<div className="
flex
flex-col
h-[calc(100vh-160px)]
">




<div className="
flex-1
space-y-4
overflow-y-auto
p-6
border
border-slate-800
rounded-xl
bg-slate-950
">


{mensagens.map((mensagem) => (
  <MensagemChat
    key={mensagem.id}
    texto={mensagem.texto}
    usuario={mensagem.usuario}
  />
))}

</div>


<div className="mt-4">
<ChatInput
    texto={texto}
    aoAlterarTexto={setTexto}
    aoEnviar={enviarMensagem}
/>
</div>


</div>

);


}


export default ChatWindow;
