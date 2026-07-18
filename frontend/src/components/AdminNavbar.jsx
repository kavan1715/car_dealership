import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LogOut, User as UserIcon } from 'lucide-react';
import toast from 'react-hot-toast';

export const AdminNavbar = ({ title }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  return (
    <header className="glass-panel sticky top-0 z-40 px-8 py-4 flex items-center justify-between border-b border-slate-900">
      <div>
        <h2 className="text-xl font-bold font-display text-white uppercase tracking-wide">
          {title}
        </h2>
      </div>

      <div className="flex items-center gap-6">
        {/* User Info */}
        <div className="flex items-center gap-2 border-r border-slate-800 pr-6">
          <div className="w-8 h-8 rounded-full bg-primary-900/50 border border-primary-500/30 flex items-center justify-center">
            <UserIcon className="w-4 h-4 text-primary-400" />
          </div>
          <div className="text-left leading-none">
            <p className="text-sm font-semibold text-slate-200">{user?.name}</p>
            <span className="text-[10px] font-bold text-primary-400 uppercase tracking-widest mt-0.5 inline-block">
              {user?.role}
            </span>
          </div>
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 text-sm font-semibold text-red-400 hover:text-red-300 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
};
