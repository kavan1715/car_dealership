import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { VehicleCard } from '../components/VehicleCard';
import { Pagination } from '../components/Pagination';
import { Spinner } from '../components/Spinner';
import api from '../services/api';
import { Search, SlidersHorizontal, Sliders, RefreshCw, AlertCircle, ShoppingBag } from 'lucide-react';
import toast from 'react-hot-toast';

export const CustomerDashboard = () => {
  const [vehicles, setVehicles] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  
  // Search state query params
  const [searchText, setSearchText] = useState('');
  const [category, setCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [availability, setAvailability] = useState('all'); // all, available, out_of_stock
  const [sortBy, setSortBy] = useState('created_at'); // price, created_at, make
  const [order, setOrder] = useState('desc'); // asc, desc

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Debounced search query fetching
  useEffect(() => {
    const fetchVehicles = async () => {
      setLoading(true);
      setError(null);
      try {
        // Construct query parameters
        const params = {
          page: currentPage,
          limit: 6, // 6 items per page fits grid nicely
          sort_by: sortBy,
          order: order,
        };

        // Text search make/model
        if (searchText.trim()) {
          params.make = searchText.trim();
        }
        if (category) {
          params.category = category;
        }
        if (minPrice) {
          params.minimum_price = parseFloat(minPrice);
        }
        if (maxPrice) {
          params.maximum_price = parseFloat(maxPrice);
        }

        // Availability filtering
        if (availability === 'available') {
          params.availability = true;
        } else if (availability === 'out_of_stock') {
          params.availability = false;
        }

        const response = await api.get('/vehicles/search', { params });
        const { results, total_records, total_pages, current_page } = response.data;
        
        setVehicles(results);
        setTotalRecords(total_records);
        setTotalPages(total_pages);
        setCurrentPage(current_page);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to fetch inventory.');
      } finally {
        setLoading(false);
      }
    };

    // Debounce the call if user is typing search text
    const timeoutId = setTimeout(() => {
      fetchVehicles();
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchText, category, minPrice, maxPrice, availability, sortBy, order, currentPage]);

  // Handle purchasing operations
  const handlePurchase = async (id) => {
    try {
      const response = await api.post(`/vehicles/${id}/purchase`);
      toast.success('Vehicle purchased successfully!');
      
      // Update local state directly so UI matches inventory instantly
      setVehicles((prev) =>
        prev.map((v) => (v.id === id ? { ...v, quantity: response.data.quantity } : v))
      );
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to complete purchase.');
    }
  };

  // Reset filters
  const resetFilters = () => {
    setSearchText('');
    setCategory('');
    setMinPrice('');
    setMaxPrice('');
    setAvailability('all');
    setSortBy('created_at');
    setOrder('desc');
    setCurrentPage(1);
    toast.success('Filters cleared');
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-12 flex-grow w-full">
        
        {/* Header Title */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-12">
          <div>
            <h1 className="text-3xl font-black font-display text-white uppercase tracking-wide">
              Vehicle <span className="text-primary-500">Showroom</span>
            </h1>
            <p className="text-slate-400 text-sm mt-1">Browse, filter, and acquire elite automobiles.</p>
          </div>
          <button
            onClick={resetFilters}
            className="self-start md:self-auto flex items-center gap-2 text-sm font-semibold text-slate-300 bg-[#131929] hover:bg-[#1a2136] border border-slate-800 rounded-xl px-5 py-3 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reset Filters</span>
          </button>
        </div>

        {/* Layout Grid: Left Filters, Right Items */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* Filters Sidebar */}
          <aside className="glass-panel p-6 rounded-2xl h-fit space-y-6">
            <div className="flex items-center gap-2 pb-4 border-b border-slate-800/80">
              <SlidersHorizontal className="w-5 h-5 text-primary-400" />
              <h2 className="text-lg font-bold text-white uppercase font-display tracking-wider">
                Filters
              </h2>
            </div>

            {/* Keyword Search */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Search</label>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Make or Model..."
                  value={searchText}
                  onChange={(e) => {
                    setSearchText(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="w-full bg-[#111625]/80 text-white rounded-xl pl-10 pr-4 py-3 border border-slate-800 focus:bg-[#111625] focus:border-primary-500 outline-none placeholder-slate-600 transition-all text-sm"
                />
                <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              </div>
            </div>

            {/* Category Select */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Category</label>
              <select
                value={category}
                onChange={(e) => {
                  setCategory(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-3 border border-slate-800 focus:border-primary-500 outline-none transition-all text-sm cursor-pointer"
              >
                <option value="">All Categories</option>
                <option value="SUV">SUV</option>
                <option value="Sedan">Sedan</option>
                <option value="Coupe">Coupe</option>
                <option value="Sports">Sports</option>
              </select>
            </div>

            {/* Price Boundaries */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Price Range ($)</label>
              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={minPrice}
                  onChange={(e) => {
                    setMinPrice(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="w-full bg-[#111625]/80 text-white rounded-xl px-3 py-2.5 border border-slate-800 focus:border-primary-500 outline-none placeholder-slate-600 text-sm"
                />
                <input
                  type="number"
                  placeholder="Max"
                  value={maxPrice}
                  onChange={(e) => {
                    setMaxPrice(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="w-full bg-[#111625]/80 text-white rounded-xl px-3 py-2.5 border border-slate-800 focus:border-primary-500 outline-none placeholder-slate-600 text-sm"
                />
              </div>
            </div>

            {/* Stock Availability */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Availability</label>
              <div className="flex flex-col gap-2">
                {['all', 'available', 'out_of_stock'].map((option) => (
                  <label key={option} className="flex items-center gap-2 text-sm text-slate-400 cursor-pointer hover:text-white transition-colors capitalize">
                    <input
                      type="radio"
                      name="availability"
                      value={option}
                      checked={availability === option}
                      onChange={(e) => {
                        setAvailability(e.target.value);
                        setCurrentPage(1);
                      }}
                      className="accent-primary-500 cursor-pointer h-4 w-4"
                    />
                    <span>{option.replace('_', ' ')}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Sorting Columns */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-3 border border-slate-800 focus:border-primary-500 outline-none transition-all text-sm cursor-pointer"
              >
                <option value="created_at">Date Added</option>
                <option value="price">Price</option>
                <option value="make">Make</option>
              </select>
            </div>

            {/* Sorting Directions */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Sort Order</label>
              <select
                value={order}
                onChange={(e) => setOrder(e.target.value)}
                className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-3 border border-slate-800 focus:border-primary-500 outline-none transition-all text-sm cursor-pointer"
              >
                <option value="desc">Descending / Newest</option>
                <option value="asc">Ascending / Oldest</option>
              </select>
            </div>
          </aside>

          {/* Showroom Grid Content */}
          <main className="lg:col-span-3 space-y-8 flex flex-col justify-between">
            
            {loading ? (
              // Loading Skeleton Loader Grid
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[1, 2, 4].map((n) => (
                  <div key={n} className="glass-card h-96 rounded-2xl animate-pulse flex flex-col p-6 space-y-4">
                    <div className="h-44 bg-slate-800 rounded-xl w-full" />
                    <div className="h-6 bg-slate-800 rounded-md w-3/4" />
                    <div className="h-4 bg-slate-800 rounded-md w-1/2" />
                    <div className="h-12 bg-slate-800 rounded-xl w-full mt-auto" />
                  </div>
                ))}
              </div>
            ) : error ? (
              // Error State UI
              <div className="glass-panel p-12 rounded-2xl flex flex-col items-center justify-center text-center">
                <AlertCircle className="w-12 h-12 text-red-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Something went wrong</h3>
                <p className="text-slate-400 max-w-sm">{error}</p>
              </div>
            ) : vehicles.length === 0 ? (
              // Empty State UI
              <div className="glass-panel p-16 rounded-2xl flex flex-col items-center justify-center text-center">
                <ShoppingBag className="w-16 h-16 text-slate-700 mb-6" />
                <h3 className="text-xl font-bold text-white mb-2">No masterworks match your query</h3>
                <p className="text-slate-500 max-w-xs text-sm">
                  Try adjusting your search criteria, widening the price range, or checking categories.
                </p>
              </div>
            ) : (
              // Main Grid
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fadeIn">
                {vehicles.map((vehicle) => (
                  <VehicleCard
                    key={vehicle.id}
                    vehicle={vehicle}
                    onPurchase={handlePurchase}
                  />
                ))}
              </div>
            )}

            {/* Pagination Component */}
            {!loading && !error && vehicles.length > 0 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={(page) => setCurrentPage(page)}
              />
            )}
          </main>
        </div>
      </div>

      <Footer />
    </div>
  );
};
