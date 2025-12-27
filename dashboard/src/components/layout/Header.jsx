import React from 'react';
import { FiBell, FiSearch, FiUser } from 'react-icons/fi';

const Header = () => {
    return (
        <header className="h-20 flex items-center justify-between px-8 sticky top-0 z-40 backdrop-blur-md bg-white/80 border-b border-border transition-all">
            <div className="flex items-center w-96">
                <div className="relative w-full group">
                    <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 group-focus-within:text-primary transition-colors" />
                    <input
                        type="text"
                        placeholder="Search pipelines, vulnerabilities..."
                        className="w-full pl-11 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-2xl text-sm text-gray-700 focus:ring-2 focus:ring-primary/20 focus:bg-white focus:border-primary/50 transition-all shadow-sm focus:shadow-md outline-none"
                    />
                </div>
            </div>

            <div className="flex items-center space-x-6">
                <button className="relative p-2.5 text-gray-500 hover:text-primary hover:bg-primary/5 transition-all rounded-full group">
                    <FiBell className="text-xl group-hover:scale-110 transition-transform" />
                    <span className="absolute top-2.5 right-2.5 w-2.5 h-2.5 bg-danger rounded-full border-2 border-white shadow-sm"></span>
                </button>

                <div className="w-px h-8 bg-gray-200 mx-2"></div>

                <div className="flex items-center space-x-3 cursor-pointer p-1.5 rounded-full hover:bg-gray-50 transition-colors pr-4 border border-transparent hover:border-gray-200/50">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white shadow-md text-sm font-bold ring-2 ring-white">
                        AU
                    </div>
                    <div className="hidden md:block text-sm text-left">
                        <div className="font-semibold text-gray-800">Admin User</div>
                        <div className="text-xs text-gray-500 font-medium">DevSecOps Engineer</div>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
