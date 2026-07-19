import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { Spinner } from '../components/Spinner';
import api from '../services/api';
import { ArrowLeft, Sparkles, Shield, Compass, ShoppingBag } from 'lucide-react';
import toast from 'react-hot-toast';

export const VehicleDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [purchaseLoading, setPurchaseLoading] = useState(false);

  useEffect(() => {
    const fetchVehicle = async () => {
      try {
        const response = await api.get(`/vehicles/${id}`);
        setVehicle(response.data);
      } catch (error) {
        toast.error('Vehicle specifications could not be loaded.');
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    };
    fetchVehicle();
  }, [id, navigate]);

  const handlePurchase = async () => {
    setPurchaseLoading(true);
    try {
      const response = await api.post(`/vehicles/${id}/purchase`);
      toast.success('Vehicle purchased successfully!');
      setVehicle(response.data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to complete purchase.');
    } finally {
      setPurchaseLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b0f19] flex flex-col justify-between">
        <Navbar />
        <Spinner size="lg" />
        <Footer />
      </div>
    );
  }

  const formatPrice = (value) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(parseFloat(value));
  };

  const isOutOfStock = vehicle.quantity === 0;

  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-12 flex-grow w-full">
        {/* Back link */}
        <Link 
          to="/dashboard" 
          className="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white mb-8 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Showroom</span>
        </Link>

        {/* Details Layout Split */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          
          {/* Left: Car Large Backdrop */}
          <div className="relative rounded-2xl overflow-hidden bg-slate-900 border border-slate-800 shadow-2xl h-96 lg:h-[450px]">
            <img
              src={vehicle.image_src || "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1200"}
              alt={`${vehicle.make} ${vehicle.model}`}
              className="w-full h-full object-cover opacity-85"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent" />
            <span className="absolute top-6 left-6 glass-panel px-4 py-1.5 text-xs font-bold tracking-widest text-primary-300 uppercase rounded-full">
              {vehicle.category}
            </span>
          </div>

          {/* Right: Specifications & CTA */}
          <div className="space-y-8">
            <div>
              <h1 className="text-4xl lg:text-5xl font-black font-display text-white tracking-wide leading-tight">
                {vehicle.make}
              </h1>
              <p className="text-xl text-slate-400 font-display mt-1">{vehicle.model}</p>
            </div>

            <div className="border-y border-slate-800/80 py-6 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Price</p>
                <p className="text-3xl font-black text-emerald-400 font-display mt-1">
                  {formatPrice(vehicle.price)}
                </p>
              </div>
              <div className="text-right">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Availability</p>
                <div className="mt-2">
                  {isOutOfStock ? (
                    <span className="text-red-400 font-bold px-3 py-1 bg-red-950/40 border border-red-900/50 rounded-lg">
                      Out of Stock
                    </span>
                  ) : (
                    <span className="text-emerald-400 font-bold px-3 py-1 bg-emerald-950/40 border border-emerald-900/50 rounded-lg">
                      {vehicle.quantity} Units Available
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Spec Sheet Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="glass-panel p-4 rounded-xl flex items-center gap-3">
                <Sparkles className="w-5 h-5 text-primary-400 shrink-0" />
                <div>
                  <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Condition</p>
                  <p className="text-sm font-semibold text-slate-200">Pristine</p>
                </div>
              </div>
              <div className="glass-panel p-4 rounded-xl flex items-center gap-3">
                <Shield className="w-5 h-5 text-primary-400 shrink-0" />
                <div>
                  <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Warranty</p>
                  <p className="text-sm font-semibold text-slate-200">3-Year Included</p>
                </div>
              </div>
              <div className="glass-panel p-4 rounded-xl flex items-center gap-3">
                <Compass className="w-5 h-5 text-primary-400 shrink-0" />
                <div>
                  <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Acquisition</p>
                  <p className="text-sm font-semibold text-slate-200">Concierge</p>
                </div>
              </div>
            </div>

            {/* Purchase CTA */}
            <button
              onClick={handlePurchase}
              disabled={isOutOfStock || purchaseLoading}
              className={`w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all duration-300 text-lg ${
                isOutOfStock
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
                  : 'bg-primary-600 hover:bg-primary-500 text-white glow-primary border border-primary-500/20 active:scale-[0.98]'
              }`}
            >
              {purchaseLoading ? (
                <Spinner size="sm" />
              ) : (
                <>
                  <ShoppingBag className="w-5 h-5" />
                  <span>{isOutOfStock ? 'Out of Stock' : 'Aquire This Vehicle'}</span>
                </>
              )}
            </button>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};
