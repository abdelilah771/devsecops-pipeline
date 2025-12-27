import React, { useEffect, useState } from 'react';
import { logService } from '../../services/logService';
import { FiClock, FiDatabase, FiGitBranch, FiHash, FiEye } from 'react-icons/fi';

const LogList = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await logService.getLogs({ limit: 50 });
                setLogs(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400">
                Error loading logs: {error}
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-background-dark/50 shadow-sm rounded-xl border border-border-light dark:border-border-dark overflow-hidden">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-border-light dark:divide-border-dark">
                    <thead className="bg-gray-50 dark:bg-white/5">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider">Timestamp</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider">Provider</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider">Repo / Project</th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider">Run ID</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-transparent divide-y divide-border-light dark:divide-border-dark">
                        {logs.length === 0 ? (
                            <tr>
                                <td colSpan="4" className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                                    No logs found.
                                </td>
                            </tr>
                        ) : (
                            logs.map((log) => (
                                <tr key={log._id || log.id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200">
                                        <div className="flex items-center gap-2">
                                            <FiClock className="text-muted-light" />
                                            {new Date(log.timestamp_received).toLocaleString()}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${log.provider === 'GITHUB'
                                                ? 'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-700'
                                                : log.provider === 'GITLAB'
                                                    ? 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-900/20 dark:text-orange-300 dark:border-orange-800'
                                                    : 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800'
                                            }`}>
                                            <FiDatabase className="mr-1.5 w-3 h-3" />
                                            {log.provider}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white font-medium">
                                        <div className="flex items-center gap-2">
                                            <FiGitBranch className="text-muted-light" />
                                            {log.repo_name || 'N/A'}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 font-mono">
                                        <div className="flex items-center gap-2">
                                            <FiHash className="text-muted-light" />
                                            {log.run_id}
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default LogList;
