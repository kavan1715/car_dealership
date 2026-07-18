import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { AlertTriangle, Home } from 'lucide-react';

export const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col justify-between">
      <Navbar />

      <main className="max-w-md mx-auto px-6 py-24 text-center relative z-10 flex flex-col items-center justify-center">
        <div className="w-16 h-16 rounded-2xl bg-amber-950/40 border border-amber-500/30 flex items-center justify-center mb-6">
          <AlertTriangle className="w-8 h-8 text-amber-400" />
        </div>
        <h1 className="text-6xl font-black font-display text-white mb-2 leading-none">404</h1>
        <h2 className="text-xl font-bold text-slate-200 mb-4 uppercase tracking-wider font-display">
          Page Not Found
        </h2>
        <p className="text-slate-400 text-sm mb-10 leading-relaxed">
          The high-performance coordinates you are trying to reach do not exist in our catalog maps.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 bg-[#131929] hover:bg-[#1a2136] text-slate-200 font-bold px-6 py-3.5 rounded-xl border border-slate-800 transition-colors active:scale-95"
        >
          <Home className="w-4 h-4" />
          <span>Return Home</span>
        </Link>
      </main>

      <Footer />
    </div>
  );
};
