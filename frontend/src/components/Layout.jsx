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
                {isActive && <div className="w-1.5 h-6 bg-brand-navy rounded-r-full absolute left-0" />}
                <Icon size={20} className={isActive ? "text-white" : "text-slate-400 group-hover:text-brand-navy transition-colors"} />
                <div className="absolute left-16 bg-brand-navy border border-slate-700 text-white text-[10px] font-bold tracking-widest uppercase px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50 shadow-xl">
                    {label}
                </div>
            </div>
        );
    };

    return (
        <div className={`app-container font-sans bg-transparent ${rightPanel ? 'has-right-panel' : ''}`}>
            {/* 1. Left Global Nav */}
            <aside className="main-nav">
                <div className="w-12 h-12 bg-gradient-to-br from-brand-navy to-brand-blue rounded-[1.25rem] flex items-center justify-center text-white shadow-lg shadow-brand-navy/40 mb-8 mt-2 cursor-pointer hover:scale-105 transition-transform" onClick={() => navigate('/dashboard')}>
                    <BrainCircuit size={24} />
                </div>

                <div className="flex-1 w-full flex flex-col items-center gap-3">
                    <NavItem icon={Inbox} path="/dashboard" label="Support Stream" />
                    <NavItem icon={BarChart2} path="/reporting" label="Intelligence" />
                    <NavItem icon={Database} path="/data" label="Data Grid" />
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
