import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Import components to test (will fail initially - TDD RED)
import { StatsCard } from '../components/StatsCard';
import { ConfirmModal } from '../components/ConfirmModal';

describe('Admin Component Tests', () => {

  // ==========================================
  // 1. STATS CARD TEST
  // ==========================================
  test('StatsCard renders numeric values and labels correctly', () => {
    render(<StatsCard title="Total Vehicles" value={42} label="Listed cars" />);
    
    expect(screen.getByText('Total Vehicles')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
    expect(screen.getByText('Listed cars')).toBeInTheDocument();
  });

  // ==========================================
  // 2. CONFIRMATION DELETE MODAL TEST
  // ==========================================
  test('ConfirmModal displays description and handles callbacks', () => {
    const onConfirmMock = vi.fn();
    const onCloseMock = vi.fn();
    
    render(
      <ConfirmModal 
        isOpen={true}
        title="Delete Vehicle"
        message="Are you sure you want to delete this vehicle permanently?"
        onConfirm={onConfirmMock}
        onClose={onCloseMock}
      />
    );
    
    expect(screen.getByText('Delete Vehicle')).toBeInTheDocument();
    expect(screen.getByText('Are you sure you want to delete this vehicle permanently?')).toBeInTheDocument();
    
    // Test cancel trigger
    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);
    expect(onCloseMock).toHaveBeenCalled();
    
    // Test confirm trigger
    const confirmButton = screen.getByRole('button', { name: /confirm/i });
    fireEvent.click(confirmButton);
    expect(onConfirmMock).toHaveBeenCalled();
  });

  test('ConfirmModal hides if isOpen is false', () => {
    render(
      <ConfirmModal 
        isOpen={false}
        title="Delete Vehicle"
        message="Are you sure?"
        onConfirm={vi.fn()}
        onClose={vi.fn()}
      />
    );
    
    expect(screen.queryByText('Delete Vehicle')).not.toBeInTheDocument();
  });
});
