import React from 'react';
import { AlertCircle, X } from 'lucide-react';
import { Button } from './Button';

export const ConfirmModal = ({ isOpen, title, message, onConfirm, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Dark overlay backdrop */}
      <div 
        className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm cursor-pointer"
        onClick={onClose} 
      />

      {/* Modal Dialog Content */}
      <div className="relative glass-panel rounded-2xl max-w-md w-full p-6 shadow-2xl animate-scaleUp z-10 border border-slate-800">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-red-950/40 border border-red-500/30 flex items-center justify-center shrink-0 text-red-400">
            <AlertCircle className="w-5 h-5" />
          </div>
          
          <div className="space-y-2 flex-grow">
            <h3 className="text-lg font-bold text-white uppercase font-display tracking-wide">
              {title}
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              {message}
            </p>
          </div>
        </div>

        <div className="mt-8 flex items-center justify-end gap-3">
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="danger" onClick={onConfirm}>
            Confirm
          </Button>
        </div>
      </div>
    </div>
  );
};
