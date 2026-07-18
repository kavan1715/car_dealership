import React, { useState, useEffect } from 'react';
import { AdminSidebar } from '../components/AdminSidebar';
import { AdminNavbar } from '../components/AdminNavbar';
import { StatsCard } from '../components/StatsCard';
import { Spinner } from '../components/Spinner';
import api from '../services/api';
import { Car, Hash, EyeOff, Tag, AlertCircle } from 'lucide-react';

export const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalVehicles: 0,
    totalQuantity: 0,
    outOfStock: 0,
    totalCategories: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Query search with high limit to capture all items
        const response = await api.get('/vehicles/search?page=1&limit=1000');
        const items = response.data.results;

        // Perform client-side aggregations
        const totalVehicles = items.length;
        const totalQuantity = items.reduce((acc, curr) => acc + (curr.quantity || 0), 0);
        const outOfStock = items.filter((item) => (item.quantity || 0) === 0).length;
        const uniqueCategories = new Set(items.map((item) => item.category.trim())).size;

        setStats({
          totalVehicles,
          totalQuantity,
          outOfStock,
          totalCategories: uniqueCategories,
        });
      } catch (err) {
        setError('Could not aggregate metrics. Verify database connections.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="min-h-screen bg-[#0b0f19] flex">
      <AdminSidebar />

      <div className="flex-grow flex flex-col min-w-0">
        <AdminNavbar title="System Overview" />

        <main className="p-8 space-y-8 flex-grow">
          {loading ? (
            <div className="h-96 flex items-center justify-center">
              <Spinner size="lg" />
            </div>
          ) : error ? (
            <div className="glass-panel p-12 rounded-2xl flex flex-col items-center justify-center text-center">
              <AlertCircle className="w-12 h-12 text-red-400 mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Metrics Offline</h3>
              <p className="text-slate-400 max-w-sm">{error}</p>
            </div>
          ) : (
            <>
              {/* Stats Widgets Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fadeIn">
                <StatsCard
                  title="Total Vehicles"
                  value={stats.totalVehicles}
                  label="Registered listings"
                  icon={Car}
                />
                <StatsCard
                  title="Total Inventory"
                  value={stats.totalQuantity}
                  label="In-stock units"
                  icon={Hash}
                />
                <StatsCard
                  title="Out of Stock"
                  value={stats.outOfStock}
                  label="Requires replenishment"
                  icon={EyeOff}
                />
                <StatsCard
                  title="Categories"
                  value={stats.totalCategories}
                  label="Distinct segments"
                  icon={Tag}
                />
              </div>

              {/* Information Board Card */}
              <div className="glass-panel p-8 rounded-2xl">
                <h3 className="text-lg font-bold text-white uppercase font-display tracking-wider mb-4">
                  Admin Console Guidelines
                </h3>
                <p className="text-slate-400 text-sm leading-relaxed max-w-3xl">
                  Welcome to the GarageOne Administrative Console. Here you can configure catalog entries, review stock levels, adjust prices, and record vehicle restocking acquisitions. Ensure you double-check values before committing database additions or deletions.
                </p>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
};
