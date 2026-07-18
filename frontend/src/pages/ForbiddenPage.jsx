import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, Home } from 'lucide-react';

export const ForbiddenPage = () => {
  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col justify-center items-center px-6 py-24 text-center bg-grid-lines relative">
      <div className="absolute inset-0 bg-radial-gradient pointer-events-none" />

      <div className="relative z-10 max-w-md mx-auto flex flex-col items-center justify-center">
        <div className="w-16 h-16 rounded-2xl bg-red-950/40 border border-red-500/30 flex items-center justify-center mb-6 text-red-400">
          <ShieldAlert className="w-8 h-8" />
        </div>
        
        <h1 className="text-6xl font-black font-display text-white mb-2 leading-none">403</h1>
        <h2 className="text-xl font-bold text-slate-200 mb-4 uppercase tracking-wider font-display">
          Access Denied
        </h2>
        <p className="text-slate-400 text-sm mb-10 leading-relaxed">
          You do not possess the required administrator credentials to enter this coordinate dashboard.
        </p>

        <Link
          to="/dashboard"
          className="inline-flex items-center gap-2 bg-[#131929] hover:bg-[#1a2136] text-slate-200 font-bold px-6 py-3.5 rounded-xl border border-slate-800 transition-colors active:scale-95"
        >
          <Home className="w-4 h-4" />
          <span>Return to Showroom</span>
        </Link>
      </div>
    </div>
  );
};
