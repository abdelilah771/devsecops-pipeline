import React from 'react';
import { FiDownloadCloud } from 'react-icons/fi';

const AuditLogExport = () => {
    return (
        <div className="bg-surface-light p-6 rounded-xl border border-border-light shadow-sm flex items-center justify-between">
            <div>
                <h3 className="font-bold text-gray-900">Audit Logs</h3>
                <p className="text-sm text-muted-light mt-1">Export system activity logs for compliance review.</p>
            </div>
            <button className="flex items-center px-4 py-2 bg-white border border-border-light rounded-lg text-muted-dark hover:text-primary hover:border-primary transition-colors">
                <FiDownloadCloud className="mr-2" />
                Export CSV
            </button>
        </div>
    );
};

export default AuditLogExport;
