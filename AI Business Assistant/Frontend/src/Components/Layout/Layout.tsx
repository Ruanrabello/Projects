import Sidebar from "./Sidebar";
import Header from "./Header";
import { useState } from "react";

import { Outlet } from "react-router-dom";

function Layout() {
  const [cheia, minimizada] = useState<boolean>(false);
  return (

    <div className="flex min-h-screen bg-slate-950 text-white">
      <Sidebar
       collapsed={cheia}
       onToggle={() => minimizada(!cheia)}

      />

      <div className="flex-1 flex flex-col">
        <Header />

        <main className="p-8">

          <Outlet />

        </main>

      </div>

    </div>
  );
}

export default Layout;
