import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { VehicleCard } from '../components/VehicleCard';
import api from '../services/api';
import { ArrowRight, ShieldCheck, Award, Zap, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';

export const LandingPage = () => {
  const [featuredVehicles, setFeaturedVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load first 3 vehicles for featured showcase
  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        const response = await api.get('/vehicles?page=1&limit=3');
        setFeaturedVehicles(response.data.items);
      } catch (error) {
        // Fallback silently if database is empty/disconnected
      } finally {
        setLoading(false);
      }
    };
    fetchFeatured();
  }, []);

  const handlePurchaseMock = () => {
    toast('Please log in to purchase this vehicle', { icon: '🔑' });
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <header className="relative flex-grow flex items-center justify-center py-24 px-6 bg-grid-lines overflow-hidden">
        {/* Glowing Ambient Light overlay */}
        <div className="absolute inset-0 bg-radial-gradient pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-950/50 border border-primary-500/30 text-xs font-bold text-primary-400 uppercase tracking-widest mb-6 animate-pulse">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Discover Elite Inventory</span>
          </div>
          
          <h1 className="text-4xl sm:text-6xl font-black font-display tracking-tight text-white mb-6 leading-[1.1] uppercase">
            Acquire the <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-indigo-400 glow-text">Extraordinary</span>
          </h1>
          
          <p className="text-slate-400 sm:text-xl max-w-2xl mx-auto leading-relaxed mb-10">
            Explore our curated catalog of elite engineering, state-of-the-art performance, and timeless automotive designs.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/dashboard"
              className="w-full sm:w-auto bg-primary-600 hover:bg-primary-500 text-white font-bold px-8 py-4 rounded-xl flex items-center justify-center gap-2 border border-primary-500/20 glow-primary transition-all duration-300 active:scale-95"
            >
              <span>Explore Collection</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/register"
              className="w-full sm:w-auto bg-[#131929] hover:bg-[#1a2136] text-slate-200 font-bold px-8 py-4 rounded-xl border border-slate-800 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Featured Grid Showcase */}
      {featuredVehicles.length > 0 && (
        <section className="py-24 px-6 max-w-7xl mx-auto w-full">
          <h2 className="text-2xl sm:text-4xl font-extrabold font-display text-white mb-2 uppercase tracking-wide">
            Featured <span className="text-primary-500">Models</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base mb-12">Handpicked masterpieces currently available in our showroom.</p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {featuredVehicles.map((vehicle) => (
              <VehicleCard 
                key={vehicle.id} 
                vehicle={vehicle} 
                onPurchase={handlePurchaseMock} 
              />
            ))}
          </div>
        </section>
      )}

      {/* Selling Points (Why choose us) */}
      <section className="py-24 px-6 border-t border-slate-900 bg-[#080b13]/60 w-full">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl sm:text-4xl font-extrabold font-display text-center text-white mb-16 uppercase tracking-wide">
            The GarageOne <span className="text-primary-500">Standard</span>
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass-panel p-8 rounded-2xl flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-xl bg-primary-950/40 border border-primary-500/30 flex items-center justify-center mb-6">
                <ShieldCheck className="w-6 h-6 text-primary-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Guaranteed Provenance</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Every vehicle undergoes rigorous inspections, multi-point checks, and documentation audits.
              </p>
            </div>

            <div className="glass-panel p-8 rounded-2xl flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-xl bg-primary-950/40 border border-primary-500/30 flex items-center justify-center mb-6">
                <Award className="w-6 h-6 text-primary-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Award-Winning Services</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Enjoy customized financing options, personal brokers, and white-glove concierge home delivery.
              </p>
            </div>

            <div className="glass-panel p-8 rounded-2xl flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-xl bg-primary-950/40 border border-primary-500/30 flex items-center justify-center mb-6">
                <Zap className="w-6 h-6 text-primary-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Instant Transactions</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Stateless cryptographic token integration provides quick and seamless purchase validation.
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};
