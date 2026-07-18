import React from 'react';
import { Routes, Route } from 'react-router-dom';

// Import Pages
import { LandingPage } from '../pages/LandingPage';
import { LoginPage } from '../pages/LoginPage';
import { RegisterPage } from '../pages/RegisterPage';
import { CustomerDashboard } from '../pages/CustomerDashboard';
import { VehicleDetailsPage } from '../pages/VehicleDetailsPage';
import { NotFoundPage } from '../pages/NotFoundPage';

// Import Admin Pages
import { AdminDashboard } from '../pages/AdminDashboard';
import { AdminVehiclePage } from '../pages/AdminVehiclePage';
import { AddVehiclePage } from '../pages/AddVehiclePage';
import { EditVehiclePage } from '../pages/EditVehiclePage';
import { ForbiddenPage } from '../pages/ForbiddenPage';

// Import Route Guards
import { ProtectedRoute } from '../components/ProtectedRoute';

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/403" element={<ForbiddenPage />} />
      
      {/* Customer Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <CustomerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/vehicles/:id"
        element={
          <ProtectedRoute>
            <VehicleDetailsPage />
          </ProtectedRoute>
        }
      />

      {/* Admin Protected Routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/vehicles"
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminVehiclePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/add-vehicle"
        element={
          <ProtectedRoute requiredRole="admin">
            <AddVehiclePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/edit-vehicle/:id"
        element={
          <ProtectedRoute requiredRole="admin">
            <EditVehiclePage />
          </ProtectedRoute>
        }
      />

      {/* Fallback 404 Route */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
