import React from 'react';
import { Car, Github, Twitter, Instagram } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-[#080b13] border-t border-slate-900 px-6 py-12">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        
        {/* Brand Info */}
        <div className="md:col-span-2">
          <div className="flex items-center gap-2 mb-4">
            <Car className="w-6 h-6 text-primary-500" />
            <span className="text-lg font-black font-display tracking-wider">
              ANTIGRAVITY<span className="text-primary-500">MOTORS</span>
            </span>
          </div>
          <p className="text-slate-400 text-sm max-w-sm leading-relaxed">
            Experience next-level luxury and performance. We curate the world's most advanced and pristine vehicles, providing an exceptional acquisition workflow.
          </p>
        </div>

        {/* Links */}
        <div>
          <h4 className="text-white font-bold text-sm mb-4 uppercase tracking-wider">Quick Links</h4>
          <ul className="flex flex-col gap-2.5 text-slate-400 text-sm">
            <li><a href="#" className="hover:text-white transition-colors">Featured Listings</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Test Drives</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Financing</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Acquisitions</a></li>
          </ul>
        </div>

        {/* Social Links */}
        <div>
          <h4 className="text-white font-bold text-sm mb-4 uppercase tracking-wider">Connect With Us</h4>
          <div className="flex gap-4 mb-6">
            <a href="#" className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors">
              <Twitter className="w-5 h-5" />
            </a>
            <a href="#" className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors">
              <Instagram className="w-5 h-5" />
            </a>
            <a href="#" className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white transition-colors">
              <Github className="w-5 h-5" />
            </a>
          </div>
          <p className="text-xs text-slate-500">
            &copy; 2026 Antigravity Motors. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};
