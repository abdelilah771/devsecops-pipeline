import React from 'react';
import ReportGenerator from '../components/reports/ReportGenerator';

export default function Reports() {
    return (
        <div className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark p-8">
            <div className="max-w-6xl mx-auto">
                <div className="mb-12">
                    <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">Reports</h1>
                    <p className="mt-2 text-lg text-gray-600 dark:text-gray-400">
                        Generate and download security reports in PDF, HTML, or SARIF formats. View compliance status against industry standards and export audit logs for regulatory use.
                    </p>
                </div>
                <div className="space-y-10">
                    <section>
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Compliance Overview</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                            <div className="bg-white dark:bg-background-dark/50 border border-gray-200 dark:border-gray-700/50 rounded-lg p-6 flex flex-col justify-between shadow-sm">
                                <div>
                                    <p className="text-base font-medium text-gray-600 dark:text-gray-300">OWASP Compliance</p>
                                    <p className="text-5xl font-bold text-gray-900 dark:text-white mt-2">95%</p>
                                </div>
                                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-4">
                                    <div className="bg-success-light dark:bg-success-dark h-2.5 rounded-full" style={{ width: '95%' }}></div>
                                </div>
                            </div>
                            <div className="bg-white dark:bg-background-dark/50 border border-gray-200 dark:border-gray-700/50 rounded-lg p-6 flex flex-col justify-between shadow-sm">
                                <div>
                                    <p className="text-base font-medium text-gray-600 dark:text-gray-300">SLSA Compliance</p>
                                    <p className="text-5xl font-bold text-gray-900 dark:text-white mt-2">88%</p>
                                </div>
                                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-4">
                                    <div className="bg-yellow-500 h-2.5 rounded-full" style={{ width: '88%' }}></div>
                                </div>
                            </div>
                            <div className="bg-white dark:bg-background-dark/50 border border-gray-200 dark:border-gray-700/50 rounded-lg p-6 flex flex-col justify-between shadow-sm">
                                <div>
                                    <p className="text-base font-medium text-gray-600 dark:text-gray-300">CIS Compliance</p>
                                    <p className="text-5xl font-bold text-gray-900 dark:text-white mt-2">92%</p>
                                </div>
                                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-4">
                                    <div className="bg-success-light dark:bg-success-dark h-2.5 rounded-full" style={{ width: '92%' }}></div>
                                </div>
                            </div>
                        </div>
                    </section>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                        <section>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Report Generation</h2>
                            <ReportGenerator />
                        </section>
                        <section>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Audit Log Export</h2>
                            <div className="space-y-6 bg-white dark:bg-background-dark/50 border border-gray-200 dark:border-gray-700/50 rounded-lg p-6 shadow-sm">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300" htmlFor="date-range">Date Range</label>
                                    <select className="form-select block w-full rounded-md border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:border-primary focus:ring-primary sm:text-sm" id="date-range" name="date-range">
                                        <option>Last 7 days</option>
                                        <option>Last 30 days</option>
                                        <option>Last 90 days</option>
                                        <option>Custom range</option>
                                    </select>
                                </div>
                                <div className="h-[76px]"></div>
                                <button className="w-full flex items-center justify-center gap-2 rounded-md bg-gray-200 dark:bg-gray-700 px-4 py-2.5 text-sm font-semibold text-gray-800 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-400 transition-colors" type="button">
                                    <span className="material-symbols-outlined text-xl">history</span>
                                    Export Audit Logs
                                </button>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
}
