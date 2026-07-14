import {
  LayoutDashboard,
  MessageSquare,
  FileText,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight
} from "lucide-react";



import { NavLink } from "react-router-dom";

import ConversasRecentes from "./RecentActivities";


const menu = [
  {
    icon: LayoutDashboard,
    label: "Dashboard",
    path: "/"
  },

  {
    icon: MessageSquare,
    label: "Chat",
    path: "/chat"
  },

  {
    icon: FileText,
    label: "Documentos",
    path: "/documents"
  },

  {
    icon: Settings,
    label: "Configurações",
    path: "/settings"
  },

   {
    icon: BarChart3,
    label: "Relatórios",
    path: "/relatorio"
  },

];

interface Sidebar_Estado_Minimizado_Cheia {
  collapsed: boolean;
  onToggle: () => void;
}

function Sidebar({ collapsed, onToggle }: Sidebar_Estado_Minimizado_Cheia) {
  return (

    <aside
      className={`
        ${collapsed ? "w-20" : "w-75"}
        bg-slate-900
        border-r
        border-slate-800
        p-1.5
        flex
        flex-col
        transition-all
        duration-300
      `}
    >

      <div className="flex items-center justify-between">
        <div>
          {!collapsed ? (
            <div className="rounded-lg pl-2 pr-3 py-3">
              <img
                src="public/logo.png"
                alt="Logo"
                className="w-18 h-14 object-contain -ml-4"
              />
            </div>
          ) : (
            <div className="p-3 flex items-center justify-center">
              <img
                src="public/logo.png"
                alt="Logo"
                className="w-6 h-6 object-contain"
              />
            </div>
          )}
        </div>

        <div className="p-3">
          <button
            onClick={onToggle}
            className="p-1 rounded-lg hover:bg-slate-800 text-slate-300"
          >
            {collapsed ? <ChevronRight size={18}/> : <ChevronLeft size={18}/>}
          </button>
        </div>
      </div>


      <nav className="mt-10 space-y-2">

        {menu.map(({ icon: Icon, label, path }) => (

          <NavLink
            key={label}
            to={path}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg p-3 transition ${
                isActive
                ? "bg-slate-700 text-white"
                : "hover:bg-slate-800 text-slate-300"
              }`
            }
          >

            <Icon size={15}/>

            {!collapsed && (
              <span>{label}</span>
            )}

          </NavLink>

        ))}

      </nav>


      <div className="flex-1 overflow-y-auto pt-6 pb-6 px-3">
        {!collapsed && (
          <ConversasRecentes />
        )}
      </div>


      <div className="p-6 border-t border-slate-800">

        <div className="flex items-center gap-3">

          <div className="h-8 w-8 rounded-full bg-cyan-500 flex items-center justify-center font-bold">
            R
          </div>

          {!collapsed && (
            <div>
              <p className="text-sm text-white font-medium">
                Ruan
              </p>

              <p className="text-xs text-slate-400">
                Plano Free
              </p>
            </div>
          )}

        </div>

      </div>


    </aside>

  );
}

export default Sidebar;







