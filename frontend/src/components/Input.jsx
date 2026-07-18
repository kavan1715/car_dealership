import React, { forwardRef } from 'react';

export const Input = forwardRef(({ label, error, type = 'text', ...props }, ref) => {
  return (
    <div className="flex flex-col gap-2 w-full">
      {label && (
        <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
          {label}
        </label>
      )}
      <input
        ref={ref}
        type={type}
        className={`w-full bg-[#111625]/80 text-white rounded-xl px-4 py-3 border transition-all duration-300 outline-none placeholder-slate-600 focus:bg-[#111625] focus:border-primary-500 ${
          error
            ? 'border-red-500/55 focus:border-red-500'
            : 'border-slate-800 focus:border-primary-500'
        }`}
        {...props}
      />
      {error && (
        <span className="text-xs font-semibold text-red-400 transition-all">
          {error.message}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';
