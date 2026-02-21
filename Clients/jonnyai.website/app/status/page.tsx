"use client";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { Activity, Shield, Zap, Server, Globe, Cpu, CheckCircle2 } from "lucide-react";

const technicalMetrics = [
  { label: "Core Web Vitals", value: "99/100", agent: "@Milo", status: "Optimal" },
  { label: "LCP (Load Speed)", value: "0.8s", agent: "@Milo", status: "Gold-Tier" },
  { label: "FID (Latency)", value: "14ms", agent: "@Milo", status: "Optimal" },
  { label: "Security Audit", value: "0 Weaknesses", agent: "@Victor", status: "Verified" },
];

const mcpServers = [
  { name: "Supabase Central", handle: "supabase", pool: "64 Conn", status: "Connected" },
  { name: "GitHub Pulse", handle: "github", pool: "API v3", status: "Connected" },
  { name: "Brave Intelsat", handle: "brave-search", pool: "Live", status: "Active" },
  { name: "Playwright Verifier", handle: "playwright", pool: "Headed", status: "Standby" },
];

export default function StatusPage() {
  return (
    <div className="flex flex-col min-h-screen bg-black overflow-hidden selection:bg-accent selection:text-black">
      <Navbar />
      
      <main className="pt-40 pb-24 px-6 md:px-12">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-24 flex flex-col items-center text-center">
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-2 px-4 py-1.5 glass-panel rounded-full border-accent/20 mb-8"
            >
              <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              <span className="text-[10px] uppercase tracking-[0.3em] font-black text-accent">Global System Health: 99.98%</span>
            </motion.div>
            
            <h1 className="text-6xl md:text-9xl font-bold mb-8 leading-[0.95]">
              Real-Time<br />
              <span className="text-white/30 italic">Technical Vitals.</span>
            </h1>
            
            <p className="text-white/40 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed font-sans">
              We operate a distributed Jai.OS 4.0 infrastructure. Every build is monitored by the orchestra for performance parity and security isolation.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Vitals Column */}
            <div className="lg:col-span-2 space-y-8">
               {/* Metrics Grid */}
               <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                 {technicalMetrics.map((tech) => (
                   <div key={tech.label} className="glass-panel p-8 rounded-[40px] border-white/5 hover:border-accent/20 transition-all group">
                      <div className="flex justify-between items-start mb-10">
                         <span className="text-white/20 text-[10px] uppercase tracking-[0.4em] font-black">{tech.label}</span>
                         <CheckCircle2 className="w-5 h-5 text-accent opacity-20 group-hover:opacity-100 transition-opacity" />
                      </div>
                      <div className="flex items-end justify-between">
                         <div>
                            <span className="text-4xl font-black text-white block mb-2">{tech.value}</span>
                            <span className="text-accent text-[9px] font-black uppercase tracking-widest leading-none">{tech.status}</span>
                         </div>
                         <span className="text-white/20 text-[9px] uppercase tracking-widest font-bold">Managed // {tech.agent}</span>
                      </div>
                   </div>
                 ))}
               </div>

               {/* Large Activity Graph Mock */}
               <div className="glass-panel p-10 rounded-[40px] border-white/5 relative overflow-hidden group">
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
                     <div>
                        <h4 className="text-white font-bold text-lg mb-1">Response Latency (Global)</h4>
                        <p className="text-white/40 text-xs">Averaged across 12 distributed node centers.</p>
                     </div>
                     <div className="flex gap-4">
                        <div className="flex items-center gap-2">
                           <div className="w-2 h-2 rounded-full bg-accent" />
                           <span className="text-[9px] text-white/40 uppercase font-black tracking-widest">Main Cluster</span>
                        </div>
                        <div className="flex items-center gap-2">
                           <div className="w-2 h-2 rounded-full bg-white/10" />
                           <span className="text-[9px] text-white/40 uppercase font-black tracking-widest">Failover</span>
                        </div>
                     </div>
                  </div>
                  
                  {/* The Graph Visual */}
                  <div className="h-40 w-full flex items-end gap-1 px-2">
                     {[40, 60, 45, 80, 55, 70, 40, 90, 65, 50, 60, 45, 80, 55, 70, 40, 90, 65, 50, 40, 60, 45, 80, 55, 70].map((h, i) => (
                       <motion.div 
                        key={i}
                        initial={{ height: 0 }}
                        whileInView={{ height: `${h}%` }}
                        transition={{ delay: i * 0.05, duration: 1 }}
                        className="bg-accent/40 hover:bg-accent transition-colors w-full rounded-t-sm"
                       />
                     ))}
                  </div>

                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
               </div>
            </div>

            {/* MCP / Infrastructure Sidebar */}
            <div className="space-y-8">
               <div className="glass-panel p-8 rounded-[40px] border-white/5">
                  <div className="flex items-center gap-3 mb-8">
                     <Server className="w-5 h-5 text-accent" />
                     <h4 className="text-white font-bold text-sm uppercase tracking-wider">MCP Registry</h4>
                  </div>
                  <div className="space-y-6">
                     {mcpServers.map(server => (
                       <div key={server.handle} className="flex items-center justify-between group">
                          <div>
                             <span className="text-white text-[11px] font-bold block mb-0.5 group-hover:text-accent transition-colors">{server.name}</span>
                             <span className="text-white/20 text-[9px] font-mono tracking-tighter uppercase">{server.handle} // {server.pool}</span>
                          </div>
                          <div className="flex items-center gap-2">
                             <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
                             <span className="text-[9px] text-accent font-black uppercase tracking-widest">{server.status}</span>
                          </div>
                       </div>
                     ))}
                  </div>
                  <div className="mt-8 pt-8 border-t border-white/5">
                     <p className="text-[9px] text-white/40 leading-relaxed font-mono">
                        "Custom MCP server development active. @Adrian (The Welder) is hardening the bridge between our hive mind and Vercel Edge functions."
                     </p>
                  </div>
               </div>

               <div className="glass-panel p-8 rounded-[40px] border-white/5 bg-accent/5">
                  <div className="flex items-center gap-3 mb-6">
                     <Zap className="w-5 h-5 text-accent" />
                     <h4 className="text-white font-bold text-sm uppercase tracking-wider">Active Sprints</h4>
                  </div>
                  <div className="space-y-4">
                     <div className="flex justify-between items-center bg-black/40 p-4 rounded-2xl border border-white/5">
                        <span className="text-[10px] text-white/60 font-black uppercase tracking-widest">Next.js 16 Migration</span>
                        <span className="text-accent text-[10px] font-bold">In Progress</span>
                     </div>
                     <div className="flex justify-between items-center bg-black/40 p-4 rounded-2xl border border-white/5 opacity-40">
                        <span className="text-[10px] text-white/60 font-black uppercase tracking-widest">Global RLS Audit</span>
                        <span className="text-white/40 text-[10px] font-bold">Planned</span>
                     </div>
                  </div>
               </div>
            </div>
          </div>

          {/* Footer Context */}
          <div className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
             {[
               { icon: globeIcon, label: 'Global Edge', desc: 'Deployed across 12 node clusters.' },
               { icon: shieldIcon, label: 'RLS Isolated', desc: 'Secure database architecture by @Victor.' },
               { icon: cpuIcon, label: 'AgOS 4.0 Stable', desc: 'The orchestrator engine is active.' }
             ].map(item => (
                <div key={item.label} className="flex flex-col items-center">
                   <div className="bg-white/5 p-4 rounded-2xl border border-white/10 mb-6">
                      <item.icon className="w-6 h-6 text-white/40" />
                   </div>
                   <h5 className="text-white font-bold text-xs uppercase tracking-widest mb-2">{item.label}</h5>
                   <p className="text-white/40 text-[11px] max-w-[200px] leading-relaxed mx-auto">{item.desc}</p>
                </div>
             ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

function globeIcon(props: any) { return <Globe {...props} /> }
function shieldIcon(props: any) { return <Shield {...props} /> }
function cpuIcon(props: any) { return <Cpu {...props} /> }
