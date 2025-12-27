import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const data = [
    { name: 'Mon', critical: 4, high: 2, medium: 7 },
    { name: 'Tue', critical: 3, high: 5, medium: 5 },
    { name: 'Wed', critical: 2, high: 3, medium: 8 },
    { name: 'Thu', critical: 5, high: 4, medium: 6 },
    { name: 'Fri', critical: 1, high: 6, medium: 4 },
    { name: 'Sat', critical: 2, high: 3, medium: 3 },
    { name: 'Sun', critical: 1, high: 2, medium: 2 },
];

const TrendChart = () => {
    return (
        <div className="glass-panel p-6 rounded-2xl h-full flex flex-col">
            <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold text-lg text-slate-200 tracking-wide">Vulnerability Trends</h3>
                <select className="bg-surface-dark border border-white/10 rounded-lg text-sm px-3 py-1 text-muted-dark focus:ring-2 focus:ring-primary outline-none transition-all hover:border-white/20">
                    <option>Last 7 days</option>
                    <option>Last 30 days</option>
                    <option>Last 3 months</option>
                </select>
            </div>
            <div className="flex-1 w-full min-h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorCritical" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} dy={10} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', borderRadius: '12px', border: '1px solid #334155', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', color: '#f8fafc' }}
                            itemStyle={{ fontSize: '12px', fontWeight: 500 }}
                            labelStyle={{ color: '#94a3b8', marginBottom: '8px' }}
                        />
                        <Area type="monotone" dataKey="critical" stroke="#ef4444" strokeWidth={3} fillOpacity={1} fill="url(#colorCritical)" />
                        <Area type="monotone" dataKey="high" stroke="#f59e0b" strokeWidth={3} fillOpacity={1} fill="url(#colorHigh)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default TrendChart;
