'use client';

import React, { useEffect, useState } from 'react';
import { Header } from '../components/Header';
import { KpiCard } from '../components/KpiCard';
import { StartupTable } from '../components/StartupTable';
import { fetchRunwaySummary, fetchStartups, RiskSummaryKPI, Startup } from '../lib/api';
import { ShieldAlert, AlertCircle, CheckCircle2, TrendingUp, Search, Filter, RefreshCw } from 'lucide-react';

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<RiskSummaryKPI | null>(null);
  const [startups, setStartups] = useState<Startup[]>([]);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('All');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    const [m, s] = await Promise.all([
      fetchRunwaySummary(),
      fetchStartups(search, riskFilter),
    ]);
    setMetrics(m);
    setStartups(s);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, [riskFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 space-y-8">
        {/* KPI Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <KpiCard
            title="High Risk Startups"
            value={metrics ? metrics.high_risk_count : '-'}
            subtitle="< 6 months runway remaining"
            icon={ShieldAlert}
            variant="rose"
          />
          <KpiCard
            title="Medium Risk Watch"
            value={metrics ? metrics.medium_risk_count : '-'}
            subtitle="6 - 12 months runway"
            icon={AlertCircle}
            variant="amber"
          />
          <KpiCard
            title="Low Risk Buffer"
            value={metrics ? metrics.low_risk_count : '-'}
            subtitle="> 12 months runway"
            icon={CheckCircle2}
            variant="emerald"
          />
          <KpiCard
            title="Avg Portfolio Runway"
            value={metrics ? `${metrics.avg_runway_months} Mo` : '-'}
            subtitle={`Across ${metrics?.total_portfolio_startups || 0} tracked companies`}
            icon={TrendingUp}
            variant="cyan"
          />
        </div>

        {/* Filters & Control Bar */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 p-4 rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-md">
          <form onSubmit={handleSearchSubmit} className="flex items-center gap-2 w-full md:w-96">
            <div className="relative w-full">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search company or industry..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-950/80 border border-slate-800 rounded-xl text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-sm font-semibold transition-colors shadow-lg shadow-cyan-500/20"
            >
              Search
            </button>
          </form>

          <div className="flex items-center gap-3 w-full md:w-auto justify-end">
            <div className="flex items-center gap-2 text-xs text-slate-400 font-semibold uppercase">
              <Filter className="w-3.5 h-3.5" />
              Risk Level:
            </div>
            {['All', 'High', 'Medium', 'Low'].map((level) => (
              <button
                key={level}
                onClick={() => setRiskFilter(level)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  riskFilter === level
                    ? 'bg-slate-700 text-white border border-slate-600 shadow'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                {level}
              </button>
            ))}
            <button
              onClick={loadData}
              className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors ml-2"
              title="Refresh Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {/* Portfolio Runway Table Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              Portfolio Runway Radar
              <span className="text-xs font-normal px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                {startups.length} Companies
              </span>
            </h2>
          </div>

          <StartupTable startups={startups} />
        </section>
      </main>
    </div>
  );
}
