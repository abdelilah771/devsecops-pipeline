import React, { useState, useEffect } from 'react';
import { FiDownload, FiCalendar, FiFileText, FiLoader, FiCheckCircle, FiAlertTriangle } from 'react-icons/fi';
import { reportService } from '../../services/reportService';
import { pipelineService } from '../../services/pipelineService';

const ReportGenerator = () => {
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState('IDLE'); // IDLE, PROCESSING, SUCCESS, FAILURE
    const [taskId, setTaskId] = useState(null);
    const [downloadUrl, setDownloadUrl] = useState(null);
    const [error, setError] = useState(null);

    // Form State
    const [reportType, setReportType] = useState('technical');
    const [format, setFormat] = useState('html');
    const [runId, setRunId] = useState('');
    const [runs, setRuns] = useState([]);

    // Load recent runs to populate Run ID dropdown
    useEffect(() => {
        const loadRuns = async () => {
            try {
                const data = await pipelineService.getAll();
                if (data && data.length > 0) {
                    setRuns(data);
                    setRunId(data[0].run_id || ''); // Default to latest
                }
            } catch (err) {
                console.error("Failed to load runs", err);
            }
        };
        loadRuns();
    }, []);

    // Polling Logic
    useEffect(() => {
        let interval;
        if (status === 'PROCESSING' && taskId) {
            interval = setInterval(async () => {
                try {
                    const data = await reportService.getStatus(taskId);
                    console.log("Polling status:", data);

                    if (data.status === 'SUCCESS') {
                        setStatus('SUCCESS');
                        clearInterval(interval);
                        if (data.result && data.result.report_id) {
                            // Construct reliable URL using proxy
                            // If backend returns file URI, we might need to adjust logic. 
                            // Assuming getDownloadUrl proxy works:
                            setDownloadUrl(`/api/reports/download/${data.result.report_id}`);
                        }
                    } else if (data.status === 'FAILURE') {
                        setStatus('FAILURE');
                        setError('Generation failed on server.');
                        clearInterval(interval);
                    }
                } catch (err) {
                    console.error("Polling error", err);
                    setStatus('FAILURE');
                    setError(err.message);
                    clearInterval(interval);
                }
            }, 2000);
        }
        return () => clearInterval(interval);
    }, [status, taskId]);

    const handleGenerate = async () => {
        setLoading(true);
        setStatus('PROCESSING');
        setError(null);
        setDownloadUrl(null);

        try {
            const payload = {
                run_id: runId || 'latest',
                project_name: "SafeOps Dashboard",
                triggered_by: "Dashboard User",
                report_type: reportType,
                format: format,
                // explicit empty array and default metrics to avoid 422
                vulnerabilities: [],
                metrics: {
                    total_vulnerabilities: 0,
                    critical_count: 0,
                    high_count: 0,
                    medium_count: 0,
                    low_count: 0,
                    security_score: 0.0
                }
            };

            const data = await reportService.generate(payload);
            if (data.task_id) {
                setTaskId(data.task_id);
            } else {
                throw new Error("No task ID returned");
            }
        } catch (err) {
            setStatus('FAILURE');
            setError(err.message);
        } finally {
            setLoading(false);
            // Note: loading false just means HTTP POST done, but status stays PROCESSING
        }
    };

    return (
        <div className="bg-white dark:bg-background-dark/50 p-6 rounded-xl border border-border-light dark:border-border-dark shadow-sm">
            <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <FiFileText /> Generate Report
            </h3>

            <div className="space-y-4">
                {/* Run Selection */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Select Pipeline Run</label>
                    <select
                        value={runId}
                        onChange={(e) => setRunId(e.target.value)}
                        className="w-full bg-gray-50 dark:bg-black/20 border border-border-light dark:border-border-dark rounded-lg text-sm text-gray-900 dark:text-white px-3 py-2 outline-none focus:ring-2 focus:ring-primary"
                    >
                        {runs.length === 0 && <option value="">Loading runs...</option>}
                        {runs.map(r => (
                            <option key={r.run_id} value={r.run_id}>
                                {r.pipeline_name || r.repo_name} ({r.run_id}) - {r.status}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Report Type */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Report Type</label>
                    <select
                        value={reportType}
                        onChange={(e) => setReportType(e.target.value)}
                        className="w-full bg-gray-50 dark:bg-black/20 border border-border-light dark:border-border-dark rounded-lg text-sm text-gray-900 dark:text-white px-3 py-2 outline-none focus:ring-2 focus:ring-primary"
                    >
                        <option value="technical">Technical Report</option>
                        <option value="executive">Executive Summary</option>
                        <option value="compliance">Compliance Audit</option>
                    </select>
                </div>

                {/* Format */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Format</label>
                    <select
                        value={format}
                        onChange={(e) => setFormat(e.target.value)}
                        className="w-full bg-gray-50 dark:bg-black/20 border border-border-light dark:border-border-dark rounded-lg text-sm text-gray-900 dark:text-white px-3 py-2 outline-none focus:ring-2 focus:ring-primary"
                    >
                        <option value="html">HTML</option>
                        <option value="pdf">PDF</option>
                        <option value="json">JSON</option>
                    </select>
                </div>

                {/* Action Button & Status */}
                <div className="mt-6">
                    {status === 'IDLE' && (
                        <button
                            onClick={handleGenerate}
                            disabled={loading || !runId}
                            className={`w-full bg-primary hover:bg-primary/90 text-white font-medium py-2.5 rounded-lg flex items-center justify-center transition-all shadow-glow-primary ${(!runId) ? 'opacity-50 cursor-not-allowed' : ''
                                }`}
                        >
                            <FiDownload className="mr-2" />
                            Generate Report
                        </button>
                    )}

                    {status === 'PROCESSING' && (
                        <div className="w-full bg-primary/10 text-primary font-medium py-2.5 rounded-lg flex items-center justify-center border border-primary/20">
                            <FiLoader className="animate-spin mr-2" />
                            Generating...
                        </div>
                    )}

                    {status === 'SUCCESS' && downloadUrl && (
                        <a
                            href={downloadUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="w-full bg-success-light hover:bg-success-dark text-white font-medium py-2.5 rounded-lg flex items-center justify-center transition-all shadow-md cursor-pointer"
                        >
                            <FiCheckCircle className="mr-2" />
                            Download Ready
                        </a>
                    )}

                    {status === 'SUCCESS' && !downloadUrl && (
                        <div className="text-sm text-gray-500 text-center mt-2">
                            Report ready but URL missing.
                        </div>
                    )}

                    {status === 'FAILURE' && (
                        <div className="w-full bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 font-medium py-2.5 rounded-lg flex items-center justify-center border border-red-200 dark:border-red-900/30">
                            <FiAlertTriangle className="mr-2" />
                            {error || 'Generation Failed'}
                        </div>
                    )}

                    {(status === 'SUCCESS' || status === 'FAILURE') && (
                        <button
                            onClick={() => setStatus('IDLE')}
                            className="w-full mt-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 underline"
                        >
                            Reset
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ReportGenerator;
