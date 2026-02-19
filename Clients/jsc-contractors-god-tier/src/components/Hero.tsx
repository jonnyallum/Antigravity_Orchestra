"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import Image from "next/image";
import { useRef } from "react";

export default function Hero() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], ["0%", "30%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 1], [1, 1.1]);
  const blur = useTransform(scrollYProgress, [0, 0.5], ["0px", "10px"]);

  return (
    <section 
      ref={containerRef}
      className="relative h-screen w-full flex items-center justify-center overflow-hidden bg-black"
    >
      {/* Background Image (Color Revealed via Interaction or Scroll) */}
      <motion.div 
        style={{ y, scale, filter: `grayscale(20%)` }}
        className="absolute inset-0 z-0"
      >
        <Image
          src="/assets/IMG-20260219-WA0007.jpg"
          alt="JSC Construction Excellence"
          fill
          className="object-cover opacity-60"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/80" />
      </motion.div>

      {/* Hero Content */}
      <div className="relative z-10 text-center px-6 max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          style={{ opacity }}
        >
          <span className="text-accent text-[12px] uppercase tracking-[0.4em] font-semibold mb-6 block">
            Heritage West Sussex
          </span>
          <h1 className="text-5xl md:text-8xl text-white font-serif leading-none mb-8">
            Building with purpose.<br />
            <span className="italic">Crafted</span> with care.
          </h1>
          <p className="text-white/60 text-lg md:text-xl font-sans max-w-2xl mx-auto leading-relaxed">
            Premium residential construction and renovations. We transform bare foundations into timeless masterpieces of craftsmanship.
          </p>
          
          <div className="mt-12 flex flex-col md:flex-row items-center justify-center gap-6">
            <button className="px-10 py-4 bg-white text-black text-[11px] uppercase tracking-[0.2em] font-bold hover:bg-accent transition-colors duration-500">
              View Our Work
            </button>
            <button className="px-10 py-4 border border-white/20 text-white text-[11px] uppercase tracking-[0.2em] font-bold hover:bg-white/10 transition-colors duration-500 backdrop-blur-sm">
              Our Heritage
            </button>
          </div>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2, duration: 1 }}
        className="absolute bottom-12 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center"
      >
        <span className="text-[9px] uppercase tracking-[0.3em] text-white/40 mb-4">Scroll to Explore</span>
        <div className="w-[1px] h-12 bg-gradient-to-b from-accent to-transparent" />
      </motion.div>

      {/* Grain Overlay for Tactility */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.03] z-50 bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
    </section>
  );
}
