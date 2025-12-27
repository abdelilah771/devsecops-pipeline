import React from 'react';
import { FiAlertTriangle, FiGithub, FiCheckCircle } from 'react-icons/fi';

const alerts = [
    { id: 1, type: 'SQL Injection', target: 'Login Service', severity: 'High', time: '2 mins ago', status: 'Pending' },
    { id: 2, type: 'Hardcoded Secret', target: 'Payment API', severity: 'Critical', time: '15 mins ago', status: 'Fix Ready' },
    { id: 3, type: 'XSS Vulnerability', target: 'Frontend App', severity: 'Medium', time: '1 hour ago', status: 'Investigating' },
    { id: 4, type: 'Insecure Dep', target: 'Auth Module', severity: 'High', time: '3 hours ago', status: 'Pending' },
];

const AlertsTable = () => {
    return (
        <div className="glass-panel rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/5 backdrop-blur-sm">
                <div>
                    <h3 className="font-bold text-lg text-slate-200">Recent Security Alerts</h3>
                    <p className="text-xs text-muted-dark mt-1">Real-time threat detection stream</p>
                </div>
                <button className="text-primary text-sm font-medium hover:text-white transition-colors px-3 py-1 rounded-lg hover:bg-white/5">View All</button>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="border-b border-white/5 bg-surface-dark/30 text-left">
                            <th className="px-6 py-4 text-xs font-bold text-muted-dark uppercase tracking-wider">Type</th>
                            <th className="px-6 py-4 text-xs font-bold text-muted-dark uppercase tracking-wider">Target</th>
                            <th className="px-6 py-4 text-xs font-bold text-muted-dark uppercase tracking-wider">Severity</th>
                            <th className="px-6 py-4 text-xs font-bold text-muted-dark uppercase tracking-wider">Time</th>
                            <th className="px-6 py-4 text-xs font-bold text-muted-dark uppercase tracking-wider">Status</th>
                            <th className="px-6 py-4 text-right text-xs font-bold text-muted-dark uppercase tracking-wider">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {alerts.map((alert) => (
                            <tr key={alert.id} className="hover:bg-white/5 transition-colors group">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className={`p-2 rounded-lg mr-3 shadow-lg ${alert.severity === 'Critical' ? 'bg-danger-light/10 text-danger-light shadow-danger-light/10' :
                                                alert.severity === 'High' ? 'bg-warning-light/10 text-warning-light shadow-warning-light/10' :
                                                    'bg-info-light/10 text-info-light shadow-info-light/10'
                                            }`}>
                                            <FiAlertTriangle />
                                        </div>
                                        <span className="font-medium text-slate-200 group-hover:text-white transition-colors">{alert.type}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400 font-mono">{alert.target}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ring-1 ring-inset ${alert.severity === 'Critical' ? 'bg-danger-light/10 text-danger-light ring-danger-light/20' :
                                            alert.severity === 'High' ? 'bg-warning-light/10 text-warning-light ring-warning-light/20' :
                                                'bg-info-light/10 text-info-light ring-info-light/20'
                                        }`}>
                                        {alert.severity}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-dark">{alert.time}</td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`flex items-center text-sm font-medium ${alert.status === 'Fix Ready' ? 'text-success-light' : 'text-slate-400'
                                        }`}>
                                        {alert.status === 'Fix Ready' && <FiCheckCircle className="mr-1.5 text-lg" />}
                                        {alert.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    {alert.status === 'Fix Ready' ? (
                                        <button className="text-surface-darker bg-primary hover:bg-primary/90 px-4 py-1.5 rounded-lg text-xs font-bold transition-all hover:scale-105 shadow-glow-primary/30">
                                            Apply Fix
                                        </button>
                                    ) : (
                                        <button className="text-muted-dark hover:text-white transition-colors">Details</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AlertsTable;
