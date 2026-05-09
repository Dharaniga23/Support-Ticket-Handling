import React from 'react';
import { Inbox, BarChart2, Settings, Database, LogOut, BrainCircuit, User } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';

const Layout = ({ children, rightPanel }) => {
    const navigate = useNavigate();
    const location = useLocation();

    const NavItem = ({ icon: Icon, path, label }) => {
        const isActive = location.pathname === path || (path === '/dashboard' && location.pathname.startsWith('/ticket'));
        return (
            <div
                onClick={() => navigate(path)}
                className={`nav-item group relative ${isActive ? 'active' : ''}`}
                title={label}
            >
                <Icon size={20} />
                <div className="absolute left-16 bg-slate-800 border border-slate-700 text-white text-[10px] font-bold tracking-widest uppercase px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50 shadow-xl">
                    {label}
                </div>
            </div>
        );
    };

    return (
        <div className="app-container font-sans bg-transparent">
            {/* 1. Left Global Nav */}
            <aside className="main-nav">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-[1.25rem] flex items-center justify-center text-white shadow-lg shadow-indigo-500/40 mb-8 mt-2 cursor-pointer hover:scale-105 transition-transform" onClick={() => navigate('/dashboard')}>
                    <BrainCircuit size={24} />
                </div>

                <div className="flex-1 w-full flex flex-col items-center gap-3">
                    <NavItem icon={Inbox} path="/dashboard" label="Support Stream" />
                    <NavItem icon={BarChart2} path="/reporting" label="Intelligence" />
                    <NavItem icon={Database} path="/data" label="Data Grid" />
                </div>

                <div className="flex flex-col items-center gap-3 mb-6 w-full px-4">
                    <div className="w-full border-t border-slate-800 mb-2"></div>
                    <NavItem icon={Settings} path="#" label="Settings" />
                    
                    {/* User Profile */}
                    <div className="mt-2 w-10 h-10 rounded-full bg-slate-800 border-2 border-slate-700 flex items-center justify-center text-slate-400 cursor-pointer hover:border-indigo-500 hover:text-indigo-400 transition-all shadow-lg" title="Profile">
                        <User size={18} />
                    </div>

                    <button
                        onClick={() => navigate('/login')}
                        className="mt-2 w-10 h-10 bg-slate-800/50 rounded-2xl flex items-center justify-center text-rose-400 hover:bg-rose-500 hover:text-white transition-all shadow-lg border border-slate-700/50"
                        title="Disconnect"
                    >
                        <LogOut size={16} />
                    </button>
                </div>
            </aside>

            {/* 2. Main Content */}
            <main className="flex flex-col overflow-hidden relative backdrop-blur-3xl bg-white/40">
                <div className="h-full overflow-y-auto">
                    {children}
                </div>
            </main>

            {/* 3. Agency Panel */}
            {rightPanel && (
                <aside className="prediction-panel">
                    {rightPanel}
                </aside>
            )}
        </div>
    );
};

export default Layout;
