"use client";

import { motion } from "framer-motion";
import { Terminal, Shield, Activity, Code2, CheckCircle2, AlertCircle } from "lucide-react";

const mockTasks = [
  { id: 1, time: "10:42 AM", agent: "Sebastian", action: "Initialized Next.js 15 App Router", status: "success" },
  { id: 2, time: "10:45 AM", agent: "Priya", action: "Pushed 'God-Tier' Design Tokens", status: "success" },
  { id: 3, time: "10:51 AM", agent: "Victor", action: "RLS Policy: Secure Tenant Isolation", status: "checking" },
  { id: 4, time: "10:54 AM", agent: "Jonny AI", action: "Subscribing to WebSocket...", status: "active" },
];

export default function GlassBoxPreview() {
  return (
    <section className="py-24 px-6 bg-black relative overflow-hidden">
      {/* Glow Effect */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-accent/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          className="relative z-10"
        >
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 glass-panel rounded-xl flex items-center justify-center border-accent/20">
              <Shield className="w-5 h-5 text-accent" />
            </div>
            <span className="text-accent text-[11px] uppercase tracking-[0.4em] font-black">Section 03: The Showstopper</span>
          </div>
          
          <h2 className="text-5xl md:text-7xl font-bold mb-8 leading-tight">
            See Your Code<br />
            <span className="italic text-accent">Come to Life.</span>
          </h2>
          
          <p className="text-white/60 text-lg md:text-xl font-sans max-w-xl leading-relaxed mb-10">
            Traditional agencies hide behind "Weekly Updates." We give you the <span className="text-white font-bold">Glass Box</span>. Watch Marcus, Priya, and Jonny AI commit code, resolve alerts, and push milestones in real-time. 
          </p>

          <div className="flex flex-col gap-6">
            <div className="flex items-start gap-4">
               <div className="mt-1 bg-accent/20 p-2 rounded-lg">
                  <Activity className="w-4 h-4 text-accent" />
               </div>
               <div>
                  <h4 className="text-white font-bold text-sm uppercase tracking-wider mb-1">Zero Blind Spots</h4>
                  <p className="text-white/40 text-[11px]">Every task, alert, and commit is visualized via Supabase Realtime.</p>
               </div>
            </div>
            <div className="flex items-start gap-4">
               <div className="mt-1 bg-white/5 p-2 rounded-lg">
                  <Shield className="w-4 h-4 text-white/40" />
               </div>
               <div>
                  <h4 className="text-white/40 font-bold text-sm uppercase tracking-wider mb-1">Military-Grade Isolation</h4>
                  <p className="text-white/40 text-[11px]">RLS policies ensure you see only your build. Truth-lock verified by @Victor.</p>
               </div>
            </div>
          </div>
        </motion.div>

        {/* The Mock Dashboard */}
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          className="relative group"
        >
          <div className="glass-card rounded-3xl p-6 border-white/10 relative z-10 overflow-hidden">
            {/* Dashboard Header */}
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
              <div className="flex items-center gap-3">
                <div className="h-3 w-3 rounded-full bg-red-500/20 flex items-center justify-center">
                  <div className="h-1 w-1 rounded-full bg-red-500 animate-pulse" />
                </div>
                <span className="text-[10px] uppercase tracking-widest font-mono text-white/40">Glass Box Feed // Project: Alpha_MVP</span>
              </div>
              <div className="flex gap-2">
                <div className="w-2 h-2 rounded-full bg-white/10" />
                <div className="w-2 h-2 rounded-full bg-white/10" />
              </div>
            </div>

            {/* Live Feed Container */}
            <div className="space-y-4 mb-8">
              {mockTasks.map((task, i) => (
                <motion.div 
                  key={task.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.2 }}
                  className="flex items-start gap-4 p-3 rounded-xl hover:bg-white/5 transition-colors group/task"
                >
                  <span className="text-[10px] font-mono text-white/20 mt-1">{task.time}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-black text-accent uppercase tracking-tighter">@{task.agent}</span>
                      {task.status === "success" ? (
                        <CheckCircle2 className="w-3 h-3 text-accent" />
                      ) : (
                        <div className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
                      )}
                    </div>
                    <p className="text-[12px] text-white/80 font-mono tracking-tight">{task.action}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Terminal Input Mock */}
            <div className="bg-black/40 rounded-xl p-4 border border-white/5 flex items-center gap-3">
              <Terminal className="w-4 h-4 text-white/20" />
              <span className="text-white/20 text-xs font-mono">Awaiting mission update from @Conductor...</span>
            </div>

            {/* Workforce Overlay */}
            <div className="absolute top-20 right-6 flex flex-col gap-3">
               {[1,2,3].map((v) => (
                 <div key={v} className="w-8 h-8 rounded-full border border-accent/30 bg-black flex items-center justify-center shadow-[0_0_15px_rgba(0,255,136,0.1)]">
                   <div className="w-6 h-6 rounded-full bg-white/10 overflow-hidden" />
                 </div>
               ))}
            </div>
          </div>
          
          {/* Decorative Background Elements */}
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-accent/20 blur-[60px] rounded-full" />
          <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-accent/10 blur-[60px] rounded-full" />
        </motion.div>
      </div>
    </section>
  );
}
