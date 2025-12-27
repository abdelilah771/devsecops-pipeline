import React, { useEffect, useState } from 'react';
import { vulnService } from '../services/vulnService';
import { useNavigate } from 'react-router-dom';

export default function Vulnerabilities() {
    const [vulns, setVulns] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadVulns();
    }, []);

    const loadVulns = async () => {
        try {
            setLoading(true);
            const data = await vulnService.getVulnerabilities();
            const rows = data.map((item, index) => ({ ...item, id: item._id || index }));
            setVulns(rows);
        } catch (error) {
            console.error("Error loading vulnerabilities", error);
        } finally {
            setLoading(false);
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity?.toUpperCase()) {
            case 'CRITICAL': return 'bg-danger-light dark:bg-danger-dark text-white';
            case 'HIGH': return 'bg-orange-500 text-white';
            case 'MEDIUM': return 'bg-yellow-400 text-gray-900';
            case 'LOW': return 'bg-success-light dark:bg-success-dark text-white';
            default: return 'bg-gray-200 text-gray-800';
        }
    };

    const [searchTerm, setSearchTerm] = useState('');

    const filteredVulns = vulns.filter(vuln =>
        (vuln.scanner_type?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
        (vuln.severity?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
        (vuln.run_id?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
        (vuln.status?.toLowerCase() || 'open').includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark p-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Vulnerabilities</h1>
                    <p className="mt-1 text-gray-600 dark:text-gray-400">Review and manage detected vulnerabilities in your CI/CD pipelines.</p>
                </div>

                <div className="mb-6 flex items-center justify-between">
                    <div className="relative w-full max-w-md">
                        <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500">search</span>
                        <input
                            className="w-full rounded-lg border border-border-light dark:border-border-dark bg-white dark:bg-white/5 py-2.5 pl-10 text-sm placeholder:text-gray-500 focus:border-primary focus:ring-primary focus:outline-none dark:text-white"
                            placeholder="Search vulnerabilities by type, pipeline, or status..."
                            type="search"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-4">
                        <button className="flex items-center gap-2 rounded-lg border border-border-light dark:border-border-dark bg-white dark:bg-white/5 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/10">
                            <span className="material-symbols-outlined text-base">filter_list</span>
                            Filter
                        </button>
                        <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90">
                            <span className="material-symbols-outlined text-base">add</span>
                            New Scan
                        </button>
                    </div>
                </div>

                <div className="overflow-hidden rounded-xl border border-border-light dark:border-border-dark bg-white dark:bg-background-dark/50 shadow-sm">
                    <table className="w-full text-left text-sm">
                        <thead className="bg-gray-50 dark:bg-black/10">
                            <tr className="text-xs uppercase text-gray-500 dark:text-gray-400">
                                <th className="px-4 py-3 font-medium">Type</th>
                                <th className="px-4 py-3 font-medium">Severity</th>
                                <th className="px-4 py-3 font-medium">Affected Pipeline/Run</th>
                                <th className="px-4 py-3 font-medium">Status</th>
                                <th className="px-4 py-3 font-medium">Detected At</th>
                                <th className="px-4 py-3 font-medium text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border-light dark:divide-border-dark">
                            {filteredVulns.map((vuln) => (
                                <tr key={vuln.id} className="hover:bg-primary/5 dark:hover:bg-primary/10 cursor-pointer transition-colors">
                                    <td className="px-4 py-3 font-medium text-gray-800 dark:text-gray-200">{vuln.scanner_type || 'Unknown'}</td>
                                    <td className="px-4 py-3">
                                        <span className={`inline-block rounded-full px-3 py-1 text-xs font-semibold ${getSeverityColor(vuln.severity)}`}>
                                            {vuln.severity || 'UNKNOWN'}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-gray-600 dark:text-gray-400">{vuln.run_id}</td>
                                    <td className="px-4 py-3">
                                        <span className="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300">
                                            <span className="size-1.5 rounded-full bg-current"></span>Open
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-gray-600 dark:text-gray-400">2024-01-15</td>
                                    <td className="px-4 py-3 text-right">
                                        <button
                                            onClick={() => navigate('/fixes', { state: { vulnId: vuln.vuln_id } })}
                                            className="text-primary hover:underline font-medium"
                                        >
                                            Details / Fix
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {vulns.length === 0 && !loading && (
                        <div className="p-6 text-center text-gray-500 dark:text-gray-400">No vulnerabilities found.</div>
                    )}
                    {loading && (
                        <div className="p-6 text-center text-gray-500 dark:text-gray-400">Loading vulnerabilities...</div>
                    )}
                </div>

                <div className="mt-6 flex items-center justify-between">
                    <p className="text-sm text-gray-500 dark:text-gray-400">Showing {vulns.length} results</p>
                    <div className="flex items-center gap-2">
                        <button className="rounded border border-border-light dark:border-border-dark bg-white dark:bg-white/5 px-3 py-1 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/10 disabled:opacity-50" disabled>Previous</button>
                        <button className="rounded border border-border-light dark:border-border-dark bg-white dark:bg-white/5 px-3 py-1 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/10">Next</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
