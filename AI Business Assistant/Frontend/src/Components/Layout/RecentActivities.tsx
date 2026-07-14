import { NavLink } from "react-router-dom";

const Conversas = [
    {
        id: 1,
        titulo: "Posicionar Avatar Sidebar"
    },
    {
        id: 2,
        titulo: "Erro no path do menu"
    },
    {
        id: 3,
        titulo: "Problema Netflix opera"
    },
    {
        id: 4,
        titulo: "Guia React"
    }
];

function ConversasRecentes() {
    return(
        <div className="
            h-full
            flex
            flex-col
            rounded-xl
            border
            border-slate-800
            bg-slate-900
            p-4
        ">

            <h2 className="
                text-sm
                font-semibold
                text-white
                mb-4
            ">
                Conversas Recentes
            </h2>


            <div className="
                flex-1
                overflow-y-auto
                pr-2
                space-y-1
            ">

                {Conversas.map((conversa) => (

                    <NavLink
                        key={conversa.id}
                        to={`/chat/${conversa.id}`}
                        className="
                            flex
                            items-center
                            gap-2
                            rounded-md
                            p-2
                            hover:bg-slate-800
                            cursor-pointer
                            transition
                        "
                    >

                        <div className="
                            h-2
                            w-2
                            rounded-full
                            bg-cyan-400
                        ">
                        </div>


                        <p className="
                            text-sm
                            text-slate-300
                            truncate
                        ">
                            {conversa.titulo}
                        </p>


                    </NavLink>

                ))}

            </div>

        </div>
    );
}


export default ConversasRecentes;
