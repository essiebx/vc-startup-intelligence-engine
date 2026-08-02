import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  variant?: 'cyan' | 'rose' | 'amber' | 'emerald' | 'slate';
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  variant = 'slate',
}) => {
  const variantStyles = {
    cyan: 'border-cyan-500/30 bg-cyan-950/20 text-cyan-400',
    rose: 'border-rose-500/30 bg-rose-950/20 text-rose-400',
    amber: 'border-amber-500/30 bg-amber-950/20 text-amber-400',
    emerald: 'border-emerald-500/30 bg-emerald-950/20 text-emerald-400',
    slate: 'border-slate-800 bg-slate-900/60 text-slate-400',
  };

  return (
    <div className={`p-5 rounded-2xl border ${variantStyles[variant]} backdrop-blur-sm shadow-lg`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
        <div className="p-2 rounded-xl bg-slate-800/80 border border-slate-700/50">
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">{value}</div>
      {subtitle && <p className="text-xs mt-1.5 text-slate-400">{subtitle}</p>}
    </div>
  );
};
