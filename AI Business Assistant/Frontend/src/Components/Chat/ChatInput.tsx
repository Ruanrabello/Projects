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


  function enviar() {

    if (texto.trim() === "") return;

    aoEnviar();

  }


  return (

    <div
      className="
        flex
        items-center
        gap-3
        rounded-2xl
        border
        border-slate-700
        bg-slate-900
        px-4
        py-3
      "
    >

      <button
        className="
          text-slate-400
          hover:text-white
          transition
        "
      >
        <Paperclip size={20}/>
      </button>


      <input

        value={texto}

        onChange={(e) =>
          aoAlterarTexto(e.target.value)
        }

        onKeyDown={(e) => {

          if(e.key === "Enter") {
            enviar();
          }

        }}

        placeholder="Envie uma mensagem..."

        className="
          flex-1
          bg-transparent
          outline-none
          text-white
          placeholder:text-slate-500
        "

      />


      <button
        onClick={enviar}
        disabled={texto.trim() === ""}
        className="
          rounded-xl
         bg-white
          p-2
         text-black
         hover:bg-slate-200
          disabled:opacity-40
         transition
        "
      >
        <Send size={20}/>

      </button>


    </div>

  );
}


export default ChatInput;
