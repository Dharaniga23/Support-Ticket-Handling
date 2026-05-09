import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, ArrowRight, BrainCircuit, ShieldCheck, Loader2 } from 'lucide-react';

const Login = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate network delay for effect
    setTimeout(() => {
      setIsLoading(false);
      navigate('/dashboard');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Dark Mode Background Effects */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] animate-pulse-glow" />
      <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] animate-pulse-glow" style={{ animationDelay: '1s' }} />

      <div className="w-full max-w-5xl grid md:grid-cols-2 gap-0 bg-slate-900/50 backdrop-blur-xl border border-white/10 rounded-[2rem] shadow-2xl overflow-hidden animate-fade-in-up z-10">
        
        {/* Left Side - Info Panel */}
        <div className="p-12 md:p-16 flex flex-col justify-between bg-gradient-to-br from-indigo-900/40 to-slate-900/40 relative">
          <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm -z-10" />
          
          <div>
            <div className="w-12 h-12 bg-indigo-500/20 rounded-2xl flex items-center justify-center text-indigo-400 mb-8 border border-indigo-500/30">
              <BrainCircuit size={24} />
            </div>
            <h2 className="text-3xl md:text-4xl font-black text-white tracking-tight mb-4">
              Neural <br /> Command Center.
            </h2>
            <p className="text-slate-400 font-medium leading-relaxed max-w-sm">
              Secure authentication layer for enterprise AI administration. Access real-time analytics, neural routing configurations, and live support streams.
            </p>
          </div>

          <div className="mt-16 flex items-center gap-3 text-slate-500 text-sm font-semibold">
            <ShieldCheck size={18} className="text-emerald-500" /> AES-256 Encrypted Connection
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="p-12 md:p-16 bg-slate-800/50 backdrop-blur-md flex flex-col justify-center">
          <div className="mb-10">
            <h3 className="text-2xl font-bold text-white mb-2">Agent Login</h3>
            <p className="text-slate-400 font-medium text-sm">Enter your credentials to access the workspace.</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label className="text-[11px] font-black uppercase tracking-widest text-slate-400">Corporate Email</label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                <input 
                  type="email" 
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-12 pr-4 py-3.5 bg-slate-900/50 border border-slate-700/50 rounded-xl text-white focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-600"
                  placeholder="agent@enterprise.com"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-[11px] font-black uppercase tracking-widest text-slate-400">Access Key</label>
                <a href="#" className="text-xs font-semibold text-indigo-400 hover:text-indigo-300">Forgot key?</a>
              </div>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
                <input 
                  type="password" 
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-12 pr-4 py-3.5 bg-slate-900/50 border border-slate-700/50 rounded-xl text-white focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-600"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button 
              type="submit" 
              disabled={isLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed mt-4 shadow-lg shadow-indigo-500/20"
            >
              {isLoading ? (
                <><Loader2 className="animate-spin" size={20} /> Authenticating...</>
              ) : (
                <>Establish Uplink <ArrowRight size={20} /></>
              )}
            </button>
          </form>

          <div className="mt-8 text-center text-xs text-slate-500 font-medium">
            Protected by Enterprise SSO Integration
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
