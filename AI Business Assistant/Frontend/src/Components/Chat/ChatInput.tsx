import { Paperclip, Send } from "lucide-react";


type ChatInputProps = {
  texto: string;
  aoAlterarTexto: (texto: string) => void;
  aoEnviar: () => void;
};

function ChatInput({
  texto,
  aoAlterarTexto,
  aoEnviar,
}: ChatInputProps) {

  return (
    <div className="
      flex
      items-center
      gap-3
      border
      border-slate-800
      rounded-xl
      bg-slate-900
      p-3
    ">

      <button>
        <Paperclip
          className="text-slate-400"
        />
      </button>


      <input
        value={texto}
        onChange={(e) => aoAlterarTexto(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            aoEnviar();
          }
        }}
        placeholder="Digite sua mensagem..."
        className="
          flex-1
          bg-transparent
          outline-none
         text-white
        "
      />


      <button
        onClick={aoEnviar}
        className="
        bg-cyan-500
        p-2
        rounded-lg
        hover:bg-cyan-600
        "
      >

        <Send size={20}/>

      </button>


    </div>
  );
}


export default ChatInput;
