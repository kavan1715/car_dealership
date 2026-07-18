import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Import target components (which will fail initially - TDD RED phase)
// We will create mock pages or implement the features to satisfy these imports.
import { VehicleCard } from '../components/VehicleCard';
import { Pagination } from '../components/Pagination';

describe('Frontend Component Tests', () => {
  
  // ==========================================
  // 1. VEHICLE CARD COMPONENT
  // ==========================================
  test('VehicleCard renders detail fields correctly', () => {
    const mockVehicle = {
      id: 1,
      make: 'Tesla',
      model: 'Model S',
      category: 'Sedan',
      price: '90000.00',
      quantity: 5
    };
    const onPurchaseMock = vi.fn();
    
    render(<VehicleCard vehicle={mockVehicle} onPurchase={onPurchaseMock} />);
    
    expect(screen.getByText('Tesla')).toBeInTheDocument();
    expect(screen.getByText('Model S')).toBeInTheDocument();
    expect(screen.getByText('Sedan')).toBeInTheDocument();
    expect(screen.getByText('$90,000.00')).toBeInTheDocument();
    expect(screen.getByText('5 left')).toBeInTheDocument();
    
    const button = screen.getByRole('button', { name: /purchase/i });
    expect(button).not.toBeDisabled();
    fireEvent.click(button);
    expect(onPurchaseMock).toHaveBeenCalledWith(1);
  });

  test('VehicleCard disables purchase button when out of stock', () => {
    const mockVehicle = {
      id: 2,
      make: 'Audi',
      model: 'Q7',
      category: 'SUV',
      price: '70000.00',
      quantity: 0
    };
    const onPurchaseMock = vi.fn();
    
    render(<VehicleCard vehicle={mockVehicle} onPurchase={onPurchaseMock} />);
    
    const button = screen.getByRole('button', { name: /out of stock/i });
    expect(button).toBeDisabled();
  });

  // ==========================================
  // 2. PAGINATION COMPONENT
  // ==========================================
  test('Pagination rendering and page click actions', () => {
    const onPageChangeMock = vi.fn();
    
    render(
      <Pagination 
        currentPage={2} 
        totalPages={5} 
        onPageChange={onPageChangeMock} 
      />
    );
    
    // Test that the current page is rendered
    expect(screen.getAllByText('Page 2 of 5')[0]).toBeInTheDocument();
    
    // Click Next
    const nextButton = screen.getAllByRole('button', { name: /next/i })[0];
    fireEvent.click(nextButton);
    expect(onPageChangeMock).toHaveBeenCalledWith(3);
    
    // Click Prev
    const prevButton = screen.getAllByRole('button', { name: /previous/i })[0];
    fireEvent.click(prevButton);
    expect(onPageChangeMock).toHaveBeenCalledWith(1);
  });
});
