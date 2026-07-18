import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AdminSidebar } from '../components/AdminSidebar';
import { AdminNavbar } from '../components/AdminNavbar';
import { ConfirmModal } from '../components/ConfirmModal';
import { Pagination } from '../components/Pagination';
import { Spinner } from '../components/Spinner';
import { Button } from '../components/Button';
import api from '../services/api';
import { Edit, Trash2, ArrowUpCircle, Search, SlidersHorizontal, RefreshCw, AlertCircle, Plus } from 'lucide-react';
import toast from 'react-hot-toast';

export const AdminVehiclePage = () => {
  const [vehicles, setVehicles] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);

  // Search parameters
  const [searchText, setSearchText] = useState('');
  const [category, setCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [order, setOrder] = useState('desc');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal control states
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [vehicleToDelete, setVehicleToDelete] = useState(null);

  const [restockModalOpen, setRestockModalOpen] = useState(false);
  const [vehicleToRestock, setVehicleToRestock] = useState(null);
  const [restockQuantity, setRestockQuantity] = useState('');
  const [restockSubmitting, setRestockSubmitting] = useState(false);

  // Load vehicles
  const fetchVehicles = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        page: currentPage,
        limit: 10, // 10 rows per page looks professional
        sort_by: sortBy,
        order: order,
      };

      if (searchText.trim()) params.make = searchText.trim();
      if (category) params.category = category;
      if (minPrice) params.minimum_price = parseFloat(minPrice);
      if (maxPrice) params.maximum_price = parseFloat(maxPrice);

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

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchVehicles();
    }, 300);
    return () => clearTimeout(timeoutId);
  }, [searchText, category, minPrice, maxPrice, sortBy, order, currentPage]);

  // Handle Deletions
  const triggerDeletePrompt = (vehicle) => {
    setVehicleToDelete(vehicle);
    setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    setDeleteModalOpen(false);
    if (!vehicleToDelete) return;

    try {
      await api.delete(`/vehicles/${vehicleToDelete.id}`);
      toast.success(`${vehicleToDelete.make} deleted successfully.`);
      fetchVehicles();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete vehicle.');
    } finally {
      setVehicleToDelete(null);
    }
  };

  // Handle Restocking
  const triggerRestockPrompt = (vehicle) => {
    setVehicleToRestock(vehicle);
    setRestockQuantity('');
    setRestockModalOpen(true);
  };

  const submitRestock = async (e) => {
    e.preventDefault();
    if (!vehicleToRestock) return;

    const qty = parseInt(restockQuantity, 10);
    if (isNaN(qty) || qty <= 0) {
      toast.error('Restock quantity must be a positive integer.');
      return;
    }

    setRestockSubmitting(true);
    try {
      await api.post(`/vehicles/${vehicleToRestock.id}/restock`, { quantity: qty });
      toast.success(`Restocked ${qty} units of ${vehicleToRestock.make}.`);
      setRestockModalOpen(false);
      fetchVehicles();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to restock vehicle.');
    } finally {
      setRestockSubmitting(false);
      setVehicleToRestock(null);
    }
  };

  const resetFilters = () => {
    setSearchText('');
    setCategory('');
    setMinPrice('');
    setMaxPrice('');
    setSortBy('created_at');
    setOrder('desc');
    setCurrentPage(1);
    toast.success('Filters cleared');
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex">
      <AdminSidebar />

      <div className="flex-grow flex flex-col min-w-0">
        <AdminNavbar title="Inventory Control" />

        <main className="p-8 space-y-8 flex-grow">
          
          {/* Header Buttons */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-slate-400 text-sm">Add, remove, or modify catalog vehicles.</p>
            </div>
            <Link
              to="/admin/add-vehicle"
              className="bg-primary-600 hover:bg-primary-500 text-white text-sm font-bold px-5 py-3 rounded-xl flex items-center justify-center gap-2 border border-primary-500/20 glow-primary transition-all duration-300 active:scale-95 self-start sm:self-auto"
            >
              <Plus className="w-4 h-4" />
              <span>Add New Vehicle</span>
            </Link>
          </div>

          {/* Filtering Grid Row */}
          <div className="glass-panel p-6 rounded-2xl grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">Search</label>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Make/Model..."
                  value={searchText}
                  onChange={(e) => {
                    setSearchText(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="w-full bg-[#111625]/80 text-white rounded-xl pl-10 pr-4 py-2.5 border border-slate-800 focus:bg-[#111625] focus:border-primary-500 outline-none text-sm"
                />
                <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">Category</label>
              <select
                value={category}
                onChange={(e) => {
                  setCategory(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-2.5 border border-slate-800 outline-none text-sm cursor-pointer"
              >
                <option value="">All Categories</option>
                <option value="SUV">SUV</option>
                <option value="Sedan">Sedan</option>
                <option value="Coupe">Coupe</option>
                <option value="Sports">Sports</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">Sort Column</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-2.5 border border-slate-800 outline-none text-sm cursor-pointer"
              >
                <option value="created_at">Date Added</option>
                <option value="price">Price</option>
                <option value="make">Make</option>
              </select>
            </div>

            <button
              onClick={resetFilters}
              className="flex items-center justify-center gap-2 text-sm font-semibold text-slate-300 bg-[#131929] hover:bg-[#1a2136] border border-slate-800 rounded-xl py-3 transition-colors cursor-pointer"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Clear Filters</span>
            </button>
          </div>

          {/* Data Table */}
          <div className="glass-panel rounded-2xl overflow-hidden">
            {loading ? (
              <div className="p-24 flex justify-center">
                <Spinner size="lg" />
              </div>
            ) : error ? (
              <div className="p-16 flex flex-col items-center justify-center text-center">
                <AlertCircle className="w-12 h-12 text-red-400 mb-4" />
                <p className="text-slate-400">{error}</p>
              </div>
            ) : vehicles.length === 0 ? (
              <div className="p-24 text-center text-slate-500 font-medium">
                No vehicles found matching search criteria.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="bg-slate-900/60 border-b border-slate-850 text-slate-400 font-bold uppercase tracking-wider text-xs">
                      <th className="px-6 py-4">ID</th>
                      <th className="px-6 py-4">Make</th>
                      <th className="px-6 py-4">Model</th>
                      <th className="px-6 py-4">Category</th>
                      <th className="px-6 py-4">Price</th>
                      <th className="px-6 py-4">Stock</th>
                      <th className="px-6 py-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-850 text-slate-300 font-medium">
                    {vehicles.map((v) => (
                      <tr key={v.id} className="hover:bg-slate-900/30 transition-colors">
                        <td className="px-6 py-4 text-slate-500 font-bold">#{v.id}</td>
                        <td className="px-6 py-4 text-white font-bold">{v.make}</td>
                        <td className="px-6 py-4">{v.model}</td>
                        <td className="px-6 py-4">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-primary-950/40 border border-primary-500/20 text-primary-300">
                            {v.category}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-emerald-400 font-bold">
                          {new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(parseFloat(v.price))}
                        </td>
                        <td className="px-6 py-4">
                          {v.quantity === 0 ? (
                            <span className="text-red-400 font-bold px-2 py-0.5 bg-red-950/20 border border-red-900/40 rounded-md">
                              Out of Stock
                            </span>
                          ) : (
                            <span className="text-emerald-400 font-bold px-2 py-0.5 bg-emerald-950/20 border border-emerald-900/40 rounded-md">
                              {v.quantity} units
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4 text-right flex items-center justify-end gap-2.5">
                          <button
                            onClick={() => triggerRestockPrompt(v)}
                            title="Restock Inventory"
                            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-primary-400 hover:bg-[#1a2336] transition-colors"
                          >
                            <ArrowUpCircle className="w-4 h-4" />
                          </button>
                          <Link
                            to={`/admin/edit-vehicle/${v.id}`}
                            title="Edit specs"
                            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:bg-slate-850 transition-colors inline-block"
                          >
                            <Edit className="w-4 h-4" />
                          </Link>
                          <button
                            onClick={() => triggerDeletePrompt(v)}
                            title="Delete listing"
                            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-red-400 hover:bg-red-950/20 transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Table Pagination */}
            {!loading && !error && vehicles.length > 0 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={(page) => setCurrentPage(page)}
              />
            )}
          </div>
        </main>
      </div>

      {/* Confirmation Deletes Dialog */}
      <ConfirmModal
        isOpen={deleteModalOpen}
        title="Remove Catalog Listing"
        message={vehicleToDelete ? `Are you sure you want to permanently delete the ${vehicleToDelete.make} ${vehicleToDelete.model} from the active database catalog? This action is irreversible.` : ''}
        onConfirm={confirmDelete}
        onClose={() => setDeleteModalOpen(false)}
      />

      {/* Inline Restock Prompt Modal */}
      {restockModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm cursor-pointer" onClick={() => setRestockModalOpen(false)} />
          <form onSubmit={submitRestock} className="relative glass-panel rounded-2xl max-w-md w-full p-6 shadow-2xl z-10 border border-slate-800 space-y-6">
            <h3 className="text-lg font-bold text-white uppercase font-display tracking-wide border-b border-slate-800 pb-3">
              Restock {vehicleToRestock?.make} {vehicleToRestock?.model}
            </h3>
            
            <div className="flex flex-col gap-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Additional Units</label>
              <input
                type="number"
                required
                min="1"
                placeholder="5"
                value={restockQuantity}
                onChange={(e) => setRestockQuantity(e.target.value)}
                className="w-full bg-[#111625]/80 text-white rounded-xl px-4 py-3 border border-slate-800 outline-none text-sm"
              />
              <span className="text-[10px] text-slate-500 font-medium">Currently in stock: {vehicleToRestock?.quantity} units.</span>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <Button variant="secondary" onClick={() => setRestockModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" loading={restockSubmitting}>
                Restock Units
              </Button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
