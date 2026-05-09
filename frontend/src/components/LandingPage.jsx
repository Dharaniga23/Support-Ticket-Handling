import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BrainCircuit, ShieldCheck, Zap, ArrowRight, ChevronRight, Activity, Globe } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 overflow-hidden relative selection:bg-indigo-500/30">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-500/10 rounded-full blur-[120px] animate-pulse-glow" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/10 rounded-full blur-[120px] animate-pulse-glow" style={{ animationDelay: '1s' }} />

      {/* Navigation */}
      <nav className="relative z-10 max-w-7xl mx-auto px-6 py-6 flex items-center justify-between animate-fade-in-up">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
            <BrainCircuit size={20} />
          </div>
          <span className="text-xl font-black tracking-tight text-slate-900">Semantic AI<span className="text-indigo-600">.</span></span>
        </div>
        <div className="flex items-center gap-6">
          <a href="#features" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors hidden md:block">Platform</a>
          <a href="#security" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors hidden md:block">Security</a>
          <button onClick={() => navigate('/login')} className="btn-primary text-sm px-5 py-2.5">
            Client Portal <ChevronRight size={16} />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-32 text-center flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-bold uppercase tracking-widest mb-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
          </span>
          System Online v2.4.0
        </div>
        
        <h1 className="text-6xl md:text-8xl font-black text-slate-900 tracking-tighter mb-8 leading-[1.1] animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          Autonomous <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Ticket Resolution.</span>
        </h1>
        
        <p className="text-lg md:text-xl text-slate-500 font-medium max-w-2xl mb-12 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          Empower your enterprise with an end-to-end neural network pipeline that understands, classifies, and resolves customer issues in real-time.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center gap-4 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
          <button onClick={() => navigate('/login')} className="btn-accent w-full sm:w-auto">
            Deploy Now <Zap size={18} />
          </button>
          <button onClick={() => navigate('/login')} className="btn-outline w-full sm:w-auto bg-white/50 backdrop-blur-md">
            View Live Demo <ArrowRight size={18} />
          </button>
        </div>
      </main>

      {/* Feature Grid */}
      <section id="features" className="relative z-10 max-w-7xl mx-auto px-6 pb-32">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: BrainCircuit,
              title: "Semantic Analysis",
              desc: "Deep learning models understand context, sentiment, and urgency beyond simple keywords.",
              delay: '0.5s'
            },
            {
              icon: Activity,
              title: "Real-time Processing",
              desc: "Zero-latency inference engine processes thousands of incoming tickets per minute.",
              delay: '0.6s'
            },
            {
              icon: Globe,
              title: "Global Distribution",
              desc: "Automatically routes highly complex issues to the correct specialized human agents worldwide.",
              delay: '0.7s'
            }
          ].map((feature, idx) => (
            <div key={idx} className="glass-panel p-8 rounded-[2rem] hover:-translate-y-2 transition-transform duration-500 animate-fade-in-up" style={{ animationDelay: feature.delay }}>
              <div className="w-12 h-12 bg-indigo-50 rounded-2xl flex items-center justify-center text-indigo-600 mb-6">
                <feature.icon size={24} />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">{feature.title}</h3>
              <p className="text-slate-500 leading-relaxed font-medium">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200/50 bg-white/30 backdrop-blur-md relative z-10">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-slate-400 font-semibold text-sm">
            <ShieldCheck size={16} /> Enterprise Grade Security
          </div>
          <div className="text-slate-400 text-sm font-medium">
            &copy; 2026 Semantic AI Systems. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
