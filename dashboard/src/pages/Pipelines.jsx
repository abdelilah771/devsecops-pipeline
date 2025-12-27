import React, { useEffect, useState } from 'react';
import { pipelineService } from '../services/pipelineService';
import { logParserService } from '../services/logParserService';
import { FiPlay, FiCheck, FiAlertTriangle } from 'react-icons/fi';

export default function Pipelines() {
    const [pipelines, setPipelines] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadPipelines();
    }, []);

    const loadPipelines = async () => {
        try {
            setLoading(true);
            const data = await pipelineService.getAll();
            const rows = data.map((item, index) => ({ ...item, id: item._id || index, analyzing: false }));
            setPipelines(rows);
        } catch (error) {
            console.error("Error loading pipelines", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyze = async (runId) => {
        // Optimistic update
        setPipelines(prev => prev.map(p => p.run_id === runId ? { ...p, analyzing: true } : p));

        try {
            const result = await logParserService.analyzeRun(runId);
            if (result.mq_status === 'published') {
                alert(`Analysis queued for Run ${runId}`);
            }
        } catch (error) {
            alert(`Analysis failed: ${error.message}`);
        } finally {
            setPipelines(prev => prev.map(p => p.run_id === runId ? { ...p, analyzing: false } : p));
        }
    };

    return (
        <div className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark p-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Recent Runs</h2>
                    <p className="mt-1 text-gray-600 dark:text-gray-400">Monitor and analyze recent CI/CD pipeline runs for potential risks and issues.</p>
                </div>
                <div className="bg-white dark:bg-background-dark/50 shadow-sm rounded-lg overflow-hidden border border-border-light dark:border-border-dark">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-border-light dark:divide-border-dark">
                            <thead className="bg-gray-50 dark:bg-white/5">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Run ID</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Status</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Pipeline</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Start Time</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Duration</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Actions</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-light dark:text-muted-dark uppercase tracking-wider" scope="col">Health</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border-light dark:divide-border-dark">
                                {pipelines.map((run) => (
                                    <tr key={run.id} className="hover:bg-primary/5 dark:hover:bg-primary/10 transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary">{run.run_id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${run.status === 'Failed'
                                                ? 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'
                                                : 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300'
                                                }`}>
                                                <span className="material-symbols-outlined text-sm mr-1.5">
                                                    {run.status === 'Failed' ? 'cancel' : 'check_circle'}
                                                </span>
                                                {run.status || 'Completed'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-gray-200">{run.pipeline_name || run.repo_name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">{run.timestamp_received}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">--</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">--</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-gray-200">
                                            <button
                                                onClick={() => handleAnalyze(run.run_id)}
                                                disabled={run.analyzing}
                                                className={`flex items-center gap-2 px-3 py-1 rounded-md text-sm font-medium transition-colors ${run.analyzing
                                                        ? 'bg-gray-100 text-gray-400 dark:bg-gray-800'
                                                        : 'bg-primary/10 text-primary hover:bg-primary/20'
                                                    }`}
                                            >
                                                {run.analyzing ? (
                                                    <span className="animate-spin w-4 h-4 border-2 border-current border-t-transparent rounded-full"></span>
                                                ) : (
                                                    <FiPlay className="w-4 h-4" />
                                                )}
                                                {run.analyzing ? 'Analyzing...' : 'Analyze'}
                                            </button>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-2">
                                                <div className="w-24 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                                    <div className={`h-full ${run.status === 'Failed' ? 'bg-orange-500' : 'bg-green-500'}`} style={{ width: run.status === 'Failed' ? '60%' : '95%' }}></div>
                                                </div>
                                                <span className="text-sm font-medium text-gray-800 dark:text-gray-200">{run.status === 'Failed' ? '60' : '95'}</span>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {pipelines.length === 0 && !loading && (
                            <div className="p-6 text-center text-gray-500 dark:text-gray-400">No pipelines found.</div>
                        )}
                        {loading && (
                            <div className="p-6 text-center text-gray-500 dark:text-gray-400">Loading pipelines...</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
