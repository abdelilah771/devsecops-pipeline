import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { fixService } from '../services/fixService';

export default function Fixes() {
    const location = useLocation();
    const navigate = useNavigate();
    const { vulnId } = location.state || {};

    const [fixData, setFixData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!vulnId) return;

        const loadFix = async () => {
            try {
                setLoading(true);
                const data = await fixService.getFix(vulnId);
                setFixData(data);
            } catch (err) {
                console.error("Error loading fix:", err);
                setError("Failed to load fix suggestion.");
            } finally {
                setLoading(false);
            }
        };
        loadFix();
    }, [vulnId]);

    if (!vulnId) {
        return (
            <div className="flex-1 bg-background-light dark:bg-background-dark p-8 flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">No Vulnerability Selected</h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">Please select a vulnerability from the list to see fix suggestions.</p>
                    <button
                        onClick={() => navigate('/vulnerabilities')}
                        className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary/90"
                    >
                        Go to Vulnerabilities
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark p-8">
            <div className="max-w-5xl mx-auto">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Fix Suggestion</h2>
                    <p className="mt-2 text-gray-600 dark:text-gray-400">
                        Vulnerability ID: <span className="font-mono text-primary">{vulnId}</span>
                    </p>
                </div>

                {loading && (
                    <div className="text-center py-12">
                        <div className="animate-spin w-8 h-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
                        <p className="text-gray-500">Generating fix proposal...</p>
                    </div>
                )}

                {error && (
                    <div className="p-4 bg-danger-light/10 text-danger-light rounded-lg border border-danger-light/20">
                        {error}
                    </div>
                )}

                {!loading && !error && fixData && (
                    <div className="rounded-lg border border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark shadow-sm animate-fade-in">
                        <div className="flex items-center justify-between border-b border-border-light dark:border-border-dark px-6 py-4">
                            <h3 className="font-semibold text-lg text-gray-900 dark:text-white">Proposed Solution</h3>
                            <div className="flex items-center gap-3">
                                <button className="flex items-center gap-2 rounded-lg bg-primary/10 px-4 py-2 text-sm font-semibold text-primary transition-colors hover:bg-primary/20 dark:bg-primary/20 dark:hover:bg-primary/30">
                                    <span className="material-symbols-outlined text-base">download</span>
                                    Download Patch
                                </button>
                                <button className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-primary/90">
                                    <span className="material-symbols-outlined text-base">done</span>
                                    Apply Fix
                                </button>
                            </div>
                        </div>

                        <div className="p-6">
                            <h4 className="mb-3 font-medium text-gray-900 dark:text-white">Recommended Changes</h4>
                            <div className="overflow-x-auto rounded-md bg-gray-50 dark:bg-black/20 p-4 border border-border-light dark:border-border-dark">
                                <pre className="font-mono text-sm leading-relaxed text-gray-700 dark:text-gray-300">
                                    {fixData.fix}
                                </pre>
                            </div>
                        </div>

                        <div className="border-t border-border-light dark:border-border-dark p-6 bg-gray-50/50 dark:bg-white/5">
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                <strong>Explanation:</strong> {fixData.explanation}
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
