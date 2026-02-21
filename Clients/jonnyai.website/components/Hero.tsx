"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import Link from "next/link";
import { ChevronRight, Play, Info } from "lucide-react";
import { useRef } from "react";

export default function Hero() {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section 
      ref={containerRef}
      className="relative min-h-screen w-full flex flex-col items-center justify-center overflow-hidden pt-32 pb-20 px-6"
    >
      {/* Background Animated Grid */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-background" />
        <div className="absolute inset-0 opacity-[0.15]" 
             style={{ backgroundImage: "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)", backgroundSize: "60px 60px" }} 
        />
        <motion.div 
          animate={{ opacity: [0.1, 0.3, 0.1] }}
          transition={{ duration: 5, repeat: Infinity }}
          className="absolute inset-0 bg-[radial-gradient(circle_500px_at_50%_40%,rgba(0,255,136,0.08),transparent)]" 
        />
      </div>

      {/* Hero Content */}
      <motion.div 
        style={{ y, opacity }}
        className="relative z-10 text-center max-w-5xl"
      >
        <motion.div
           initial={{ opacity: 0, scale: 0.9 }}
           animate={{ opacity: 1, scale: 1 }}
           transition={{ duration: 0.8 }}
           className="mb-8 inline-flex items-center gap-2 px-4 py-1.5 glass-panel rounded-full border-accent/20"
        >
          <span className="flex h-2 w-2 rounded-full bg-accent animate-pulse" />
          <span className="text-[10px] uppercase tracking-[0.3em] font-black text-accent">March 2026: 50% Off Early Adopter Phase</span>
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 1 }}
          className="text-6xl md:text-9xl font-bold tracking-tight mb-8 leading-[0.95] md:leading-[1.1]"
        >
          Stop Waiting Months.<br />
          <span className="text-white">Build at the </span>
          <span className="text-accent italic">Speed of Thought.</span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 1 }}
          className="text-white/60 text-lg md:text-2xl font-sans max-w-3xl mx-auto leading-relaxed mb-12"
        >
          The <span className="text-white font-bold">AI Product Engine</span> that ships enterprise-grade MVPs in 48 hours. No project managers. No decision fatigue. Just an elite orchestra of 40 agents shipping code.
        </motion.p>

        {/* CTAs */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 1 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-6"
        >
          <Link 
            href="/brief" 
            className="group w-full sm:w-auto px-12 py-5 bg-white text-black text-[12px] uppercase tracking-[0.2em] font-black hover:bg-accent hover:scale-105 transition-all duration-500 rounded-full flex items-center justify-center gap-2 shadow-[0_0_50px_rgba(0,255,136,0.2)]"
          >
            CHAT NOW
            <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link 
            href="/menu" 
            className="group w-full sm:w-auto px-12 py-5 glass-panel border-white/10 text-white text-[12px] uppercase tracking-[0.2em] font-black hover:bg-white/5 transition-all duration-500 rounded-full flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4 fill-white" />
            View Service Menu
          </Link>
        </motion.div>

        {/* Trust Signals / Footer context */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 2 }}
          className="mt-20 flex flex-wrap justify-center gap-x-12 gap-y-6 opacity-30 grayscale hover:grayscale-0 transition-all duration-1000"
        >
          {['NEXT.JS 15', 'SUPABASE REALTIME', 'FRAMER MOTION', 'AgOS 4.0'].map((tech) => (
            <span key={tech} className="text-[10px] font-mono tracking-[0.3em] font-black">{tech}</span>
          ))}
        </motion.div>
      </motion.div>

      {/* Side Intelligence Context (Dr. Elias Thorne Injected) */}
      <div className="hidden xl:block absolute left-10 top-1/2 -translate-y-1/2 max-w-[140px] opacity-20 hover:opacity-100 transition-opacity duration-500 cursor-default">
         <div className="flex flex-col gap-8 border-l border-white/10 pl-4 py-8">
            <div className="flex flex-col gap-2">
               <Info className="w-4 h-4 text-accent" />
               <p className="text-[9px] leading-relaxed font-mono uppercase tracking-wider">
                  "Speed is the only defensible moat for startups in 2026."
               </p>
               <span className="text-[8px] text-accent/60 font-black">— Dr. Elias Thorne</span>
            </div>
         </div>
      </div>
    </section>
  );
}
