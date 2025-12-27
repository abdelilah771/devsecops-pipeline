import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // Verify credentials logic here
        navigate('/');
    };

    return (
        <div className="flex min-h-screen flex-col bg-background-light dark:bg-background-dark text-gray-800 dark:text-gray-200 antialiased">
            <header className="border-b border-gray-200/10 dark:border-gray-700/50">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex h-16 items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/20 text-primary">
                                <span className="material-symbols-outlined">shield</span>
                            </div>
                            <span className="text-lg font-bold text-gray-900 dark:text-white">SafeOps-LogMiner</span>
                        </div>
                    </div>
                </div>
            </header>
            <main className="flex flex-1 items-center justify-center py-12 sm:px-6 lg:px-8">
                <div className="w-full max-w-md space-y-8">
                    <div>
                        <h1 className="text-center text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Sign in to your account</h1>
                    </div>
                    <div className="mt-8 space-y-6 rounded-xl bg-white dark:bg-gray-800/20 p-8 shadow-sm border border-border-light dark:border-border-dark">
                        <form onSubmit={handleLogin} className="space-y-6">
                            <div>
                                <label className="sr-only" htmlFor="email-address">Username or Email</label>
                                <div className="relative">
                                    <span className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500"> person </span>
                                    <input autoComplete="email" className="block w-full rounded-lg border border-border-light dark:border-gray-700 bg-background-light dark:bg-background-dark py-3 pl-10 pr-3 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm" id="email-address" name="email" placeholder="Username or Email" required type="text" defaultValue="admin" />
                                </div>
                            </div>
                            <div>
                                <label className="sr-only" htmlFor="password">Password</label>
                                <div className="relative">
                                    <span className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500"> lock </span>
                                    <input autoComplete="current-password" className="block w-full rounded-lg border border-border-light dark:border-gray-700 bg-background-light dark:bg-background-dark py-3 pl-10 pr-3 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm" id="password" name="password" placeholder="Password" required type="password" defaultValue="admin" />
                                </div>
                            </div>
                            <div className="flex items-center justify-end">
                                <div className="text-sm">
                                    <a className="font-medium text-primary hover:text-primary/80" href="#"> Forgot your password? </a>
                                </div>
                            </div>
                            <div>
                                <button className="flex w-full justify-center rounded-lg border border-transparent bg-primary px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background-light dark:focus:ring-offset-background-dark" type="submit">
                                    Sign In
                                </button>
                            </div>
                        </form>
                        <div className="relative">
                            <div aria-hidden="true" className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-300 dark:border-gray-700"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="bg-white dark:bg-gray-800/20 px-2 text-gray-500 dark:text-gray-400">Or continue with</span>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                            <a className="flex w-full items-center justify-center rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-background-dark px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 shadow-sm hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors" href="#">
                                <span className="sr-only">Sign in with SSO</span>
                                SSO
                            </a>
                            <a className="flex w-full items-center justify-center rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-background-dark px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 shadow-sm hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors" href="#">
                                <span>GitHub</span>
                            </a>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
