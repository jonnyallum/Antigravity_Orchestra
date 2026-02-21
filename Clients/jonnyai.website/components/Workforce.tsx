"use client";

import { motion } from "framer-motion";
import { User, Shield, Zap, Lock, Palette, Database } from "lucide-react";

const agents = [
  {
    handle: "@Marcus",
    name: "Marcus Cole",
    role: "The Conductor",
    quote: "Strategy is the orchestrator; tools are the instruments.",
    icon: Shield,
    color: "#00ff88",
  },
  {
    handle: "@Priya",
    name: "Priya Sharma",
    role: "The Perfectionist",
    quote: "God is in the details. If it's not perfect, it's not finished.",
    icon: Palette,
    color: "#ff0088",
  },
  {
    handle: "@Sebastian",
    name: "Sebastian Cross",
    role: "The Architect",
    quote: "Type-safe infrastructure is the only cure for technical debt.",
    icon: Database,
    color: "#0088ff",
  },
  {
    handle: "@Victor",
    name: "Victor Reyes",
    role: "The Locksmith",
    quote: "Security isn't a feature; it's a fundamental baseline.",
    icon: Lock,
    color: "#ffbb00",
  },
  {
    handle: "@Rowan",
    name: "Rowan",
    role: "The Beast",
    quote: "Truth is heavy. I'm here to make sure you never drop it.",
    icon: Zap,
    color: "#ffffff",
  },
];

export default function Workforce() {
  return (
    <section id="workforce" className="py-24 px-6 bg-black">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-20">
          <motion.span 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-accent text-[11px] uppercase tracking-[0.4em] font-black mb-6 block"
          >
            Section 04: The Core Orchestra
          </motion.span>
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-7xl font-bold mb-8"
          >
            Elite Intellect. <br />
            <span className="text-white/40 italic">Assembled for the Mission.</span>
          </motion.h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          {agents.map((agent, i) => (
            <motion.div
              key={agent.handle}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="glass-card rounded-2xl p-8 group hover:border-accent/30 transition-all duration-500 flex flex-col items-center text-center"
            >
              <div className="relative mb-6">
                <div className="w-20 h-20 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center transition-all duration-500 group-hover:scale-110 group-hover:bg-accent/10">
                  <agent.icon className="w-8 h-8 text-white group-hover:text-accent transition-colors" />
                </div>
                {/* Status Indicator */}
                <div className="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-black border border-white/10 flex items-center justify-center">
                  <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                </div>
              </div>

              <span className="text-accent text-[10px] uppercase tracking-widest font-black mb-2">{agent.handle}</span>
              <h4 className="text-white font-bold text-lg mb-1">{agent.name}</h4>
              <p className="text-white/40 text-[10px] uppercase tracking-tighter font-bold mb-6">{agent.role}</p>
              
              <div className="w-10 h-px bg-white/10 mb-6 group-hover:w-full transition-all duration-700" />
              
              <p className="text-white/60 text-xs leading-relaxed italic font-serif group-hover:text-white transition-colors">
                "{agent.quote}"
              </p>
            </motion.div>
          ))}
        </div>

        <div className="mt-20 text-center">
           <motion.p 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-white/20 text-xs uppercase tracking-[0.2em] font-mono leading-loose max-w-2xl mx-auto"
           >
            + 35 more specialized agents in recruitment, growth, legality, and infrastructure. Total Workforce Uptime: <span className="text-accent font-black">99.98%</span>.
           </motion.p>
        </div>
      </div>
    </section>
  );
}
