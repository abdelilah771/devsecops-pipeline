import React, { useEffect, useState } from 'react';
import { rabbitService } from '../../services/rabbitService';
import { FiLayers, FiActivity, FiMessageSquare } from 'react-icons/fi';
import { Line } from 'react-chartjs-2';
// Note: We might need to install chart.js if not present, but for now let's make a simple metric view
// assuming chart.js might be heavy to install right now. Let's start with a clean stat card view.

const RabbitMQMonitor = () => {
    const [stats, setStats] = useState(null);
    const [queues, setQueues] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [overview, queueData] = await Promise.all([
                    rabbitService.getOverview(),
                    rabbitService.getQueues()
                ]);
                setStats(overview);
                setQueues(queueData);
            } catch (err) {
                console.error("RabbitMQ load error", err);
                setError("Could not load RabbitMQ stats (Ensure Management Plugin enabled on 15672)");
            }
        };
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, []);

    if (error) return (
        <div className="bg-orange-50 border border-orange-200 text-orange-700 p-4 rounded-lg text-sm mb-8">
            <strong>RabbitMQ Monitor:</strong> {error}
        </div>
    );

    if (!stats) return <div className="text-gray-400 text-sm mb-8">Loading RabbitMQ Stats...</div>;

    // Filter interesting queues
    const activeQueues = queues.filter(q => q.name.includes('queue'));

    return (
        <div className="glass-panel p-8 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                <span className="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center text-orange-500 mr-4 shadow-sm border border-orange-100">
                    <FiLayers className="text-xl" />
                </span>
                RabbitMQ Overview
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-gray-50/50 border border-gray-100 rounded-2xl p-5 hover:bg-white transition-colors">
                    <div className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 flex items-center"><FiMessageSquare className="mr-2" /> Total Messages</div>
                    <div className="text-3xl font-display font-bold text-gray-800">{stats.queue_totals?.messages || 0}</div>
                    <div className="text-xs text-success font-medium mt-1 bg-success/5 inline-block px-2 py-0.5 rounded-full">Ready: {stats.queue_totals?.messages_ready || 0}</div>
                </div>
                <div className="bg-gray-50/50 border border-gray-100 rounded-2xl p-5 hover:bg-white transition-colors">
                    <div className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 flex items-center"><FiActivity className="mr-2" /> Throughput</div>
                    <div className="text-3xl font-display font-bold text-gray-800">{stats.message_stats?.publish_details?.rate?.toFixed(2) || 0} <span className="text-sm text-gray-400 font-normal">/s</span></div>
                    <div className="text-xs text-gray-400 mt-1">Publish Rate</div>
                </div>
                <div className="bg-gray-50/50 border border-gray-100 rounded-2xl p-5 hover:bg-white transition-colors">
                    <div className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 flex items-center"><FiLayers className="mr-2" /> Queues</div>
                    <div className="text-3xl font-display font-bold text-gray-800">{activeQueues.length}</div>
                    <div className="text-xs text-primary font-medium mt-1">Active Consumers</div>
                </div>
            </div>

            <div className="overflow-hidden rounded-2xl border border-gray-100">
                <table className="min-w-full text-sm">
                    <thead>
                        <tr className="bg-gray-50/80 text-left border-b border-gray-100">
                            <th className="p-4 text-gray-400 font-bold uppercase text-xs tracking-wider">Queue Name</th>
                            <th className="p-4 text-gray-400 font-bold uppercase text-xs tracking-wider">Ready</th>
                            <th className="p-4 text-gray-400 font-bold uppercase text-xs tracking-wider">Unacked</th>
                            <th className="p-4 text-gray-400 font-bold uppercase text-xs tracking-wider">State</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white">
                        {activeQueues.map(q => (
                            <tr key={q.name} className="border-b border-gray-50 hover:bg-gray-50/50 transition-colors last:border-0">
                                <td className="p-4 font-medium text-gray-700">{q.name}</td>
                                <td className="p-4 text-gray-600 font-mono">{q.messages_ready}</td>
                                <td className="p-4 text-gray-600 font-mono">{q.messages_unacknowledged}</td>
                                <td className="p-4">
                                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${q.state === 'running'
                                        ? 'bg-success/5 text-success border-success/20'
                                        : 'bg-gray-100 text-gray-500 border-gray-200'
                                        }`}>
                                        {q.state}
                                    </span>
                                </td>
                            </tr>
                        ))}
                        {activeQueues.length === 0 && (
                            <tr><td colSpan="4" className="p-8 text-center text-gray-400">No active queues found.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default RabbitMQMonitor;
