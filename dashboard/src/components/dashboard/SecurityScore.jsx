import React from 'react';

const SecurityScore = () => {
    const score = 85;
    const grade = 'A';

    // Calculate stroke dasharray for the circle
    const radius = 58;
    const circumference = 2 * Math.PI * radius;
    const progress = score / 100;
    const dashoffset = circumference - progress * circumference;

    return (
        <div className="relative h-full overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-indigo-900/40 to-blue-900/40 backdrop-blur-xl border border-white/10 shadow-glass group">
            {/* Animated Glow Background */}
            <div className="absolute top-0 right-0 w-48 h-48 bg-primary/20 rounded-full blur-3xl -mr-12 -mt-12 animate-pulse-slow"></div>
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-secondary/20 rounded-full blur-3xl -ml-8 -mb-8 animate-pulse-slow animation-delay-2000"></div>

            <div className="relative z-10 flex flex-col h-full">
                <h3 className="font-semibold text-lg text-slate-200 mb-6 tracking-wide">Security Score</h3>

                <div className="flex items-center justify-center relative py-4 flex-1">
                    {/* Background Circle */}
                    <svg className="transform -rotate-90 w-48 h-48 drop-shadow-xl">
                        <circle
                            cx="96"
                            cy="96"
                            r={radius}
                            stroke="#1e293b"
                            strokeWidth="12"
                            fill="transparent"
                            className="text-surface-dark"
                        />
                        {/* Progress Circle with Glow */}
                        <circle
                            cx="96"
                            cy="96"
                            r={radius}
                            stroke="url(#gradientScore)"
                            strokeWidth="12"
                            fill="transparent"
                            strokeDasharray={circumference}
                            strokeDashoffset={dashoffset}
                            strokeLinecap="round"
                            className="transition-all duration-1000 ease-out drop-shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                        />
                        <defs>
                            <linearGradient id="gradientScore" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#10b981" />
                                <stop offset="100%" stopColor="#3b82f6" />
                            </linearGradient>
                        </defs>
                    </svg>

                    <div className="absolute flex flex-col items-center justify-center">
                        <span className="text-5xl font-bold tracking-tighter text-white drop-shadow-lg">{score}</span>
                        <span className="text-sm font-bold text-success-light uppercase tracking-widest mt-1">Grade {grade}</span>
                    </div>
                </div>

                <div className="mt-8 space-y-4">
                    <div>
                        <div className="flex justify-between text-sm mb-1.5">
                            <span className="text-slate-400">Code Quality</span>
                            <span className="font-medium text-slate-200">92/100</span>
                        </div>
                        <div className="w-full bg-surface-dark/50 rounded-full h-2 overflow-hidden border border-white/5">
                            <div className="bg-gradient-to-r from-success-dark to-success-light h-full rounded-full shadow-[0_0_10px_rgba(16,185,129,0.3)]" style={{ width: '92%' }}></div>
                        </div>
                    </div>

                    <div>
                        <div className="flex justify-between text-sm mb-1.5">
                            <span className="text-slate-400">Dependency Risk</span>
                            <span className="font-medium text-success-light">Low</span>
                        </div>
                        <div className="w-full bg-surface-dark/50 rounded-full h-2 overflow-hidden border border-white/5">
                            <div className="bg-gradient-to-r from-success-dark to-success-light h-full rounded-full shadow-[0_0_10px_rgba(16,185,129,0.3)]" style={{ width: '85%' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SecurityScore;
