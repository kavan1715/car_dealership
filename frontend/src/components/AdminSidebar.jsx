import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Car, PlusCircle, ArrowLeft, Shield } from 'lucide-react';

export const AdminSidebar = () => {
  const location = useLocation();

  const links = [
    { path: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/vehicles', label: 'Vehicles', icon: Car },
    { path: '/admin/add-vehicle', label: 'Add Vehicle', icon: PlusCircle },
  ];

  return (
    <aside className="w-64 bg-[#080b13] border-r border-slate-900 flex flex-col justify-between p-6 h-screen sticky top-0 shrink-0">
      <div className="space-y-8">
        
        {/* Admin Header Brand */}
        <div className="flex items-center gap-2 border-b border-slate-800 pb-6">
          <Shield className="w-8 h-8 text-primary-500" />
          <div>
            <h1 className="text-sm font-black font-display tracking-widest text-white leading-none">
              ADMIN<span className="text-primary-500">PANEL</span>
            </h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">Management Console</p>
          </div>
        </div>

        {/* Links Menu */}
        <nav className="flex flex-col gap-2">
          {links.map((link) => {
            const isActive = location.pathname === link.path;
            const Icon = link.icon;
            
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl font-semibold text-sm transition-all duration-300 ${
                  isActive
                    ? 'bg-primary-950/40 text-primary-400 border border-primary-500/20 glow-primary'
                    : 'text-slate-400 hover:text-white border border-transparent hover:bg-slate-900/50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Return to Showroom */}
      <Link
        to="/dashboard"
        className="flex items-center gap-2.5 px-4 py-3 text-sm font-bold text-slate-400 hover:text-white transition-colors border-t border-slate-900 pt-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Return to Showroom</span>
      </Link>
    </aside>
  );
};
