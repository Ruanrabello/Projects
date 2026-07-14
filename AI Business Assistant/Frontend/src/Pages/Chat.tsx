import ChatWindow from "../Components/Chat/ChatWindow";
import { useParams } from "react-router-dom";

function Chat() {

  const { id } = useParams();

  return (
    <div>

      <h1 className="text-3xl font-bold">
        Chat
      </h1>

      <p className="text-slate-400 mt-2">
        Converse com seu assistente inteligente.
      </p>

      <div className="mt-8">
        <ChatWindow  conversaId={id} />
      </div>
    </div>
  );
}

export default Chat;
