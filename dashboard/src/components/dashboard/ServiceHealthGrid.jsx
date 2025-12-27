import React, { useEffect, useState } from 'react';
import { statusService } from '../../services/statusService';
import { FiServer, FiCpu, FiShield, FiFileText, FiActivity } from 'react-icons/fi';

const ServiceHealthGrid = () => {
    const [statuses, setStatuses] = useState([]);

    // Initial static list to prevent layout shift before load
    // Will update with real status
    const initialServices = [
        { id: 'logcollector', name: 'LogCollector', icon: FiServer, port: 3344 },
        { id: 'logparser', name: 'LogParser', icon: FiCpu, port: 8001 },
        { id: 'vulndetector', name: 'VulnDetector', icon: FiShield, port: 8004 },
        { id: 'fixsuggester', name: 'FixSuggester', icon: FiActivity, port: 8002 },
        { id: 'reportgenerator', name: 'ReportGenerator', icon: FiFileText, port: 8005 },
    ];

    useEffect(() => {
        const fetchStatus = async () => {
            const results = await statusService.checkAll();
            // Merge results with metadata
            const merged = initialServices.map(svc => {
                const res = results.find(r => r.id === svc.id);
                return { ...svc, status: res ? res.status : 'unknown' };
            });
            setStatuses(merged);
        };
        fetchStatus();
        const interval = setInterval(fetchStatus, 30000); // Poll every 30s
        return () => clearInterval(interval);
    }, []);

    // Use initial list if statuses empty (first render)
    const displayList = statuses.length > 0 ? statuses : initialServices.map(s => ({ ...s, status: 'loading' }));

    return (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
            {displayList.map((svc) => (
                <div key={svc.id} className="glass-panel p-5 flex flex-col items-center justify-center hover:scale-[1.02] transition-transform duration-300 group">
                    <div className={`p-3 rounded-2xl mb-3 shadow-sm transition-colors ${svc.status === 'online' ? 'bg-success/10 text-success' :
                        svc.status === 'loading' ? 'bg-gray-100 text-gray-400' :
                            'bg-danger/10 text-danger'
                        }`}>
                        <svc.icon className="text-2xl" />
                    </div>
                    <div className="text-sm font-bold text-gray-800 tracking-wide">{svc.name}</div>
                    <div className="text-xs text-gray-400 font-medium mt-1 uppercase tracking-wider">Port {svc.port}</div>
                    <div className="mt-3 flex items-center bg-gray-50 px-3 py-1 rounded-full border border-gray-100">
                        <span className={`w-2 h-2 rounded-full mr-2 shadow-sm ${svc.status === 'online' ? 'bg-success shadow-glow-success' :
                            svc.status === 'loading' ? 'bg-gray-300 animate-pulse' :
                                'bg-danger shadow-glow-danger'
                            }`}></span>
                        <span className={`text-[10px] font-bold uppercase tracking-widest ${svc.status === 'online' ? 'text-success' :
                            svc.status === 'loading' ? 'text-gray-400' :
                                'text-danger'
                            }`}>
                            {svc.status === 'loading' ? 'WAITING' : svc.status}
                        </span>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ServiceHealthGrid;
