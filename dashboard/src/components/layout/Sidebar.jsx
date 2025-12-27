import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiHome, FiActivity, FiShield, FiTool, FiFileText, FiLogOut, FiDatabase, FiTerminal } from 'react-icons/fi';

const Sidebar = () => {
    const navItems = [
        { path: '/', icon: FiHome, label: 'Dashboard' },
        { path: '/pipelines', icon: FiActivity, label: 'Pipeline Runs' },
        { path: '/vulnerabilities', icon: FiShield, label: 'Vulnerabilities' },
        { path: '/fixes', icon: FiTool, label: 'Fix Suggestions' },
        { path: '/reports', icon: FiFileText, label: 'Reports' },
        { path: '/logs', icon: FiDatabase, label: 'Security Logs' },
        { path: '/log-parser', icon: FiTerminal, label: 'Log Parser' },
    ];

    return (
        <div className="h-screen w-64 glass-panel bg-white/80 flex flex-col fixed left-0 top-0 z-50 border-r border-border shadow-soft backdrop-blur-xl">
            <div className="p-6 flex items-center">
                <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center mr-3 shadow-glow-primary text-white">
                    <FiShield className="text-xl" />
                </div>
                <span className="text-2xl font-bold tracking-tight text-gray-900">SafeOps</span>
            </div>

            <nav className="flex-1 px-4 py-6 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center px-4 py-3.5 rounded-xl transition-all duration-300 group font-medium ${isActive
                                ? 'bg-primary/10 text-primary shadow-sm border border-primary/10'
                                : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900 hover:translate-x-1'
                            }`
                        }
                    >
                        {({ isActive }) => (
                            <>
                                <item.icon className={`text-xl mr-3 transition-colors ${isActive ? 'text-primary' : 'text-gray-400 group-hover:text-primary'}`} />
                                <span>{item.label}</span>
                                {isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary" />}
                            </>
                        )}
                    </NavLink>
                ))}
            </nav>

            <div className="p-4 border-t border-border/50">
                <button className="flex items-center w-full px-4 py-3 text-gray-500 hover:text-danger hover:bg-danger/5 transition-all rounded-xl group font-medium">
                    <FiLogOut className="text-xl mr-3 group-hover:-translate-x-1 transition-transform" />
                    <span>Sign Out</span>
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
