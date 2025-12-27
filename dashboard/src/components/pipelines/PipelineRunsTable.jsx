import React from 'react';
import { FiCheckCircle, FiXCircle, FiClock, FiActivity } from 'react-icons/fi';

const PipelineRunsTable = () => {
    const runs = [
        { id: '#1234', branch: 'main', commit: 'fe23a1', status: 'Success', duration: '4m 12s', time: '10 mins ago' },
        { id: '#1233', branch: 'feature/auth-fix', commit: '90a8c2', status: 'Failed', duration: '2m 15s', time: '1 hour ago' },
        { id: '#1232', branch: 'develop', commit: '33b1f9', status: 'Success', duration: '3m 45s', time: '2 hours ago' },
        { id: '#1231', branch: 'main', commit: '12c092', status: 'Success', duration: '4m 01s', time: '5 hours ago' },
    ];

    return (
        <div className="bg-surface-light rounded-xl border border-border-light shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead className="bg-background-light/50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Run ID</th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Branch/Commit</th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Duration</th>
                            <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Time</th>
                            <th className="px-6 py-3 text-right text-xs font-semibold text-muted-dark uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-border-light">
                        {runs.map((run) => (
                            <tr key={run.id} className="hover:bg-background-light/30 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <FiActivity className="text-muted-dark mr-2" />
                                        <span className="font-medium text-gray-900">{run.id}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex flex-col">
                                        <span className="text-sm font-medium text-gray-900">{run.branch}</span>
                                        <span className="text-xs text-muted-light font-mono">{run.commit}</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium w-fit ${run.status === 'Success' ? 'bg-success-light/10 text-success-light' : 'bg-danger-light/10 text-danger-light'
                                        }`}>
                                        {run.status === 'Success' ? <FiCheckCircle className="mr-1.5" /> : <FiXCircle className="mr-1.5" />}
                                        {run.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{run.duration}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-light flex items-center">
                                    <FiClock className="mr-1.5" />
                                    {run.time}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button className="text-primary hover:text-primary/80">View Logs</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PipelineRunsTable;
