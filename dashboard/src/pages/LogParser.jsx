import React, { useState } from 'react';
import { logParserService } from '../services/logParserService';

const LogParser = () => {
    const [inputYaml, setInputYaml] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleParse = async () => {
        if (!inputYaml.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await logParserService.parseLog(inputYaml);
            setResult(data);
        } catch (err) {
            setError(err.message || 'Failed to parse log');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8 animate-fade-in p-8">
            <div className="flex flex-col gap-4">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-slate-400">
                        Manual Log Parser
                    </h1>
                    <p className="text-muted-dark mt-1">Test the parser with raw YAML content.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="bg-white dark:bg-background-dark/50 p-6 rounded-lg shadow-sm border border-border-light dark:border-border-dark">
                    <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Input YAML</h3>
                    <textarea
                        className="w-full h-[500px] p-4 font-mono text-sm bg-gray-50 dark:bg-black/20 border border-border-light dark:border-border-dark rounded-md focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all resize-none text-gray-800 dark:text-gray-200"
                        placeholder="Paste your GitHub Actions YAML log here..."
                        value={inputYaml}
                        onChange={(e) => setInputYaml(e.target.value)}
                    />
                    <div className="mt-4 flex justify-end">
                        <button
                            onClick={handleParse}
                            disabled={loading || !inputYaml.trim()}
                            className={`px-6 py-2 rounded-lg font-bold text-white transition-all transform active:scale-95 ${loading || !inputYaml.trim()
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-primary hover:bg-primary/90 shadow-glow-primary hover:-translate-y-0.5'
                                }`}
                        >
                            {loading ? 'Parsing...' : 'Parse Log'}
                        </button>
                    </div>
                </div>

                {/* Results Section */}
                <div className="bg-white dark:bg-background-dark/50 p-6 rounded-lg shadow-sm border border-border-light dark:border-border-dark flex flex-col">
                    <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Parse Results</h3>

                    <div className="flex-1 bg-gray-50 dark:bg-black/20 border border-border-light dark:border-border-dark rounded-md overflow-hidden relative">
                        {error && (
                            <div className="p-4 bg-red-50 dark:bg-red-900/10 border-b border-red-100 dark:border-red-900/20 text-red-600 dark:text-red-400">
                                <strong>Error:</strong> {error}
                            </div>
                        )}

                        {result ? (
                            <div className="h-full overflow-auto p-4 custom-scrollbar">
                                <pre className="text-xs font-mono text-gray-800 dark:text-gray-300 whitespace-pre-wrap">
                                    {JSON.stringify(result, null, 2)}
                                </pre>
                            </div>
                        ) : (
                            !error && (
                                <div className="h-full flex items-center justify-center text-gray-400 dark:text-gray-500">
                                    <p>Results will appear here</p>
                                </div>
                            )
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LogParser;
