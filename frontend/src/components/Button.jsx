import React from 'react';
import { Spinner } from './Spinner';

export const Button = ({
  children,
  type = 'button',
  variant = 'primary',
  loading = false,
  disabled = false,
  className = '',
  ...props
}) => {
  const baseClasses =
    'relative inline-flex items-center justify-center font-bold px-6 py-3 rounded-xl border transition-all duration-300 active:scale-98 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary:
      'bg-primary-600 hover:bg-primary-500 text-white border-primary-500/20 glow-primary',
    secondary:
      'bg-[#131929] hover:bg-[#1a2136] text-slate-200 border-slate-800',
    danger:
      'bg-red-650 hover:bg-red-600 text-white border-red-500/20',
  };

  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`${baseClasses} ${variants[variant]} ${className}`}
      {...props}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <Spinner size="sm" />
          <span>Processing...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};
