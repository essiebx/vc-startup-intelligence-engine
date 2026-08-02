import React from 'react';
import { Startup } from '../lib/api';
import { RiskBadge } from './RiskBadge';
import { Building2, DollarSign, Flame, Calendar, Clock } from 'lucide-react';

interface StartupTableProps {
  startups: Startup[];
}

export const StartupTable: React.FC<StartupTableProps> = ({ startups }) => {
  const formatCurrency = (amount: number) => {
    if (amount >= 1_000_000) {
      return `$${(amount / 1_000_000).toFixed(1)}M`;
    }
    return `$${(amount / 1_000).toFixed(0)}K`;
  };

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-md shadow-xl">
      <table className="w-full text-left text-sm text-slate-300">
        <thead className="bg-slate-800/80 text-xs font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-800">
          <tr>
            <th scope="col" className="px-6 py-4">Company</th>
            <th scope="col" className="px-6 py-4">Industry</th>
            <th scope="col" className="px-6 py-4">Total Raised</th>
            <th scope="col" className="px-6 py-4">Monthly Burn</th>
            <th scope="col" className="px-6 py-4">Runway (Mo)</th>
            <th scope="col" className="px-6 py-4">Risk Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60">
          {startups.length === 0 ? (
            <tr>
              <td colSpan={6} className="px-6 py-12 text-center text-slate-500 font-medium">
                No startups found matching criteria.
              </td>
            </tr>
          ) : (
            startups.map((startup) => (
              <tr
                key={startup.startup_id}
                className="hover:bg-slate-800/40 transition-colors group cursor-pointer"
              >
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded-lg bg-slate-800 text-cyan-400 group-hover:bg-cyan-500/10 transition-colors">
                      <Building2 className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="font-bold text-white group-hover:text-cyan-400 transition-colors">
                        {startup.company_name}
                      </div>
                      <div className="text-xs text-slate-400">{startup.country}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 text-slate-300 font-medium">
                  {startup.industry}
                </td>
                <td className="px-6 py-4 font-semibold text-slate-200">
                  {formatCurrency(startup.total_capital_raised_usd)}
                </td>
                <td className="px-6 py-4 text-rose-400/90 font-medium">
                  {formatCurrency(startup.estimated_monthly_burn_usd)}/mo
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <span className="font-extrabold text-white text-base">
                      {startup.runway_months}
                    </span>
                    <span className="text-xs text-slate-400">months</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <RiskBadge level={startup.risk_level} />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};
