import React from 'react';

export const StatsCard = ({ title, value, label, icon: Icon }) => {
  return (
    <div className="glass-card p-6 rounded-2xl flex items-center justify-between">
      <div className="space-y-2">
        <p className="text-sm font-bold text-slate-400 uppercase tracking-wider">
          {title}
        </p>
        <p className="text-3xl font-black font-display text-white">
          {value}
        </p>
        {label && (
          <p className="text-xs text-slate-500 font-medium">
            {label}
          </p>
        )}
      </div>

      {Icon && (
        <div className="w-12 h-12 rounded-xl bg-primary-950/40 border border-primary-500/30 flex items-center justify-center text-primary-400 shrink-0">
          <Icon className="w-6 h-6" />
        </div>
      )}
    </div>
  );
};
