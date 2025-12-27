import React from 'react';
import { FiTrendingUp, FiTrendingDown, FiMinus } from 'react-icons/fi';

const MetricCard = ({ title, value, change, changeType, icon: Icon, color }) => {
    const getChangeColor = () => {
        switch (changeType) {
            case 'increase':
                return 'text-danger-light';
            case 'decrease':
                return 'text-success-light';
            default:
                return 'text-muted-light';
        }
    };

    const getChangeIcon = () => {
        switch (changeType) {
            case 'increase':
                return <FiTrendingUp className="mr-1" />;
            case 'decrease':
                return <FiTrendingDown className="mr-1" />;
            default:
                return <FiMinus className="mr-1" />;
        }
    };

    return (
        <div className="glass-panel glass-panel-hover p-6 rounded-2xl relative overflow-hidden group">
            {/* Decorative Glow */}
            <div className={`absolute -right-6 -top-6 w-24 h-24 bg-${color}/20 rounded-full blur-2xl group-hover:bg-${color}/30 transition-all duration-500`}></div>

            <div className="flex items-start justify-between mb-4 relative z-10">
                <div className={`p-3.5 rounded-xl bg-gradient-to-br from-${color}/20 to-${color}/5 text-${color} shadow-lg shadow-${color}/10 ring-1 ring-${color}/20 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="text-xl" />
                </div>
                {change && (
                    <div className={`flex items-center text-sm font-bold ${getChangeColor()} bg-surface-darker/50 px-2 py-1 rounded-lg backdrop-blur-sm border border-white/5`}>
                        {getChangeIcon()}
                        <span>{change}</span>
                    </div>
                )}
            </div>
            <h3 className="text-muted-light text-sm font-medium mb-1 tracking-wide">{title}</h3>
            <div className="text-3xl font-bold text-white tracking-tight">{value}</div>
        </div>
    );
};

export default MetricCard;
