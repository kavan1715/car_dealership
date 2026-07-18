import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Car, LogOut, Menu, X, User as UserIcon } from 'lucide-react';
import toast from 'react-hot-toast';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
  };

  return (
    <nav className="glass-panel sticky top-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2 text-white hover:opacity-90">
          <Car className="w-8 h-8 text-primary-500" />
          <span className="text-xl font-black font-display tracking-wider">
            GARAGE<span className="text-primary-500">ONE</span>
          </span>
        </Link>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-8">
          <Link to="/" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Home
          </Link>
          <Link to="/dashboard" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Inventory
          </Link>
          {user && user.role?.toLowerCase() === 'admin' && (
            <Link to="/admin" className="text-sm font-medium text-primary-400 hover:text-primary-300 transition-colors">
              Admin Panel
            </Link>
          )}

          {user ? (
            <div className="flex items-center gap-6 border-l border-slate-800 pl-6">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-primary-900/50 border border-primary-500/30 flex items-center justify-center">
                  <UserIcon className="w-4 h-4 text-primary-400" />
                </div>
                <span className="text-sm font-semibold text-slate-200">
                  {user.name}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 text-sm font-semibold text-red-400 hover:text-red-300 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <Link to="/login" className="text-sm font-semibold text-slate-300 hover:text-white transition-colors">
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="bg-primary-600 hover:bg-primary-500 text-white text-sm font-bold px-5 py-2.5 rounded-xl border border-primary-500/20 glow-primary transition-all duration-300 active:scale-95"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Icon */}
        <button 
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} 
          className="md:hidden text-slate-300 hover:text-white"
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {isMobileMenuOpen && (
        <div className="md:hidden mt-4 pt-4 border-t border-slate-800 flex flex-col gap-4 animate-fadeIn">
          <Link 
            to="/" 
            onClick={() => setIsMobileMenuOpen(false)}
            className="text-sm font-medium text-slate-300 hover:text-white"
          >
            Home
          </Link>
          <Link 
            to="/dashboard" 
            onClick={() => setIsMobileMenuOpen(false)}
            className="text-sm font-medium text-slate-300 hover:text-white"
          >
            Inventory
          </Link>
          {user && user.role?.toLowerCase() === 'admin' && (
            <Link 
              to="/admin" 
              onClick={() => setIsMobileMenuOpen(false)}
              className="text-sm font-medium text-primary-400 hover:text-primary-300"
            >
              Admin Panel
            </Link>
          )}
          
          {user ? (
            <div className="flex flex-col gap-4 border-t border-slate-800/80 pt-4">
              <div className="flex items-center gap-2">
                <UserIcon className="w-4 h-4 text-primary-400" />
                <span className="text-sm font-semibold text-slate-200">{user.name}</span>
              </div>
              <button
                onClick={() => {
                  setIsMobileMenuOpen(false);
                  handleLogout();
                }}
                className="flex items-center gap-2 text-sm font-semibold text-red-400 hover:text-red-300"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex flex-col gap-3 border-t border-slate-800/80 pt-4">
              <Link 
                to="/login" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-sm font-semibold text-slate-300 hover:text-white"
              >
                Sign In
              </Link>
              <Link 
                to="/register" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="bg-primary-600 hover:bg-primary-500 text-white text-sm font-bold py-2.5 px-4 rounded-xl text-center"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      )}
    </nav>
  );
};
