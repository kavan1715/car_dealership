import React from 'react';
import { Sparkles, ShoppingBag } from 'lucide-react';

export const VehicleCard = ({ vehicle, onPurchase }) => {
  const { id, make, model, category, price, quantity, image_src } = vehicle;
  const isOutOfStock = quantity === 0;

  // Formatter for currency
  const formatPrice = (value) => {
    const num = parseFloat(value);
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
    }).format(num);
  };

  // Curated premium images mapping based on category/make/model to look premium
  const getCarPlaceholderImage = () => {
    // Check if there is a database-stored image
    if (image_src) {
      return image_src;
    }
    // Generates a stylized backdrop image using Unsplash (reusable asset placeholders)
    if (category.toLowerCase() === 'suv') {
      return 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=600';
    }
    if (category.toLowerCase() === 'sedan') {
      return 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=600';
    }
    return 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=600';
  };

  return (
    <div className="glass-card flex flex-col h-full rounded-2xl overflow-hidden group">
      {/* Car Image Backdrop */}
      <div className="relative h-48 overflow-hidden bg-slate-900">
        <img 
          src={getCarPlaceholderImage()} 
          alt={`${make} ${model}`}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 opacity-80"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-90" />
        
        {/* Category Label */}
        <span className="absolute top-4 left-4 glass-panel px-3 py-1 text-xs font-semibold tracking-wider text-primary-300 uppercase rounded-full">
          {category}
        </span>
      </div>

      {/* Card Info */}
      <div className="p-6 flex flex-col flex-grow">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="text-xl font-bold font-display text-white group-hover:text-primary-400 transition-colors">
              {make}
            </h3>
            <p className="text-slate-400 text-sm">{model}</p>
          </div>
          <div className="text-right">
            <span className="text-lg font-black text-emerald-400 font-display">
              {formatPrice(price)}
            </span>
          </div>
        </div>

        <div className="mt-4 flex items-center justify-between text-xs border-t border-slate-800/80 pt-4">
          <div className="flex items-center gap-1.5 text-slate-400">
            <Sparkles className="w-3.5 h-3.5 text-primary-400" />
            <span>Condition: Excellent</span>
          </div>
          <div>
            {isOutOfStock ? (
              <span className="text-red-400 font-semibold px-2 py-0.5 bg-red-950/40 border border-red-900/50 rounded-md">
                Out of Stock
              </span>
            ) : (
              <span className="text-emerald-400 font-semibold px-2 py-0.5 bg-emerald-950/40 border border-emerald-900/50 rounded-md">
                {quantity} left
              </span>
            )}
          </div>
        </div>

        {/* Action Button */}
        <button
          onClick={() => !isOutOfStock && onPurchase(id)}
          disabled={isOutOfStock}
          className={`w-full mt-6 py-3 px-4 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all duration-300 ${
            isOutOfStock
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
              : 'bg-primary-600 hover:bg-primary-500 text-white glow-primary border border-primary-500/20 active:scale-[0.98]'
          }`}
        >
          <ShoppingBag className="w-4 h-4" />
          <span>{isOutOfStock ? 'Out of Stock' : 'Purchase'}</span>
        </button>
      </div>
    </div>
  );
};
