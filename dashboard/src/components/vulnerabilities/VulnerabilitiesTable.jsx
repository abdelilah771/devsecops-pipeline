import React from 'react';
import SeverityBadge from './SeverityBadge';
import { FiEye, FiMoreVertical } from 'react-icons/fi';

const VulnerabilitiesTable = () => {
    const vulns = [
        { id: 'VULN-001', name: 'SQL Injection in Login', severity: 'Critical', location: 'auth/login.php', status: 'Open', age: '2 days' },
        { id: 'VULN-002', name: 'Cross-Site Scripting (Reflected)', severity: 'High', location: 'views/search.js', status: 'In Progress', age: '5 days' },
        { id: 'VULN-003', name: 'Hardcoded API Key', severity: 'Medium', location: 'config/app.json', status: 'Open', age: '1 week' },
        { id: 'VULN-004', name: 'Insecure Direct Object Reference', severity: 'High', location: 'api/users.js', status: 'Verified', age: '3 hours' },
        { id: 'VULN-005', name: 'Outdated Dependency (Lodash)', severity: 'Low', location: 'package.json', status: 'Open', age: '1 month' },
    ];

    return (
        <div className="bg-surface-light rounded-xl border border-border-light shadow-sm overflow-hidden">
            <table className="w-full">
                <thead className="bg-background-light/50">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">ID</th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Vulnerability</th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Severity</th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Location</th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-left text-xs font-semibold text-muted-dark uppercase tracking-wider">Age</th>
                        <th className="px-6 py-3 text-right text-xs font-semibold text-muted-dark uppercase tracking-wider"></th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-border-light">
                    {vulns.map((vuln) => (
                        <tr key={vuln.id} className="hover:bg-background-light/30 transition-colors">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{vuln.id}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-medium">{vuln.name}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <SeverityBadge severity={vuln.severity} />
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-light font-mono">{vuln.location}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <span className={`text-xs font-medium px-2 py-1 rounded-md ${vuln.status === 'Open' ? 'bg-gray-100 text-gray-700' :
                                        vuln.status === 'In Progress' ? 'bg-blue-50 text-blue-700' :
                                            'bg-green-50 text-green-700'
                                    }`}>
                                    {vuln.status}
                                </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-light">{vuln.age}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button className="text-muted-dark hover:text-primary p-1">
                                    <FiEye />
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default VulnerabilitiesTable;
