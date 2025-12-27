import React from 'react';
import { FiShield, FiFileText } from 'react-icons/fi';

const ComplianceCard = ({ title, status, score }) => {
    return (
        <div className="bg-surface-light p-5 rounded-xl border border-border-light shadow-sm">
            <div className="flex justify-between items-start mb-4">
                <div className="p-2.5 bg-background-light rounded-lg text-muted-dark">
                    <FiShield className="text-xl" />
                </div>
                <div className={`px-2 py-1 rounded text-xs font-bold uppercase tracking-wide ${status === 'Compliant' ? 'bg-success-light/10 text-success-light' : 'bg-orange-100 text-orange-600'
                    }`}>
                    {status}
                </div>
            </div>
            <h3 className="font-bold text-gray-900 mb-1">{title}</h3>
            <p className="text-sm text-muted-light mb-4">Last audit conducted 2 days ago</p>

            <div className="w-full bg-background-light rounded-full h-2 mb-2">
                <div
                    className="bg-primary h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${score}%` }}
                ></div>
            </div>
            <div className="flex justify-between text-xs font-medium">
                <span className="text-muted-dark">Compliance Score</span>
                <span className="text-gray-900">{score}%</span>
            </div>
        </div>
    );
};

export default ComplianceCard;
