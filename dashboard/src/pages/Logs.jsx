import React from 'react';
import LogList from '../components/logs/LogList';

export default function Logs() {
    return (
        <div className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark p-8">
            <div className="max-w-6xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">Security Logs</h1>
                    <p className="mt-2 text-lg text-gray-600 dark:text-gray-400">
                        View raw security logs collected from various providers.
                    </p>
                </div>
                <LogList />
            </div>
        </div>
    );
}
