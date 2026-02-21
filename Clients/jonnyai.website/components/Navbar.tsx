"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Hammer, Users, Signal, Briefcase, ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";

const navLinks = [
  { name: "The Build", href: "#build", icon: Hammer },
  { name: "The Traffic", href: "#traffic", icon: Signal },
  { name: "The Workforce", href: "#workforce", icon: Users },
  { name: "Our Work", href: "#work", icon: Briefcase },
];

export default function Navbar() {
  return (
    <motion.nav 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 flex justify-center p-6"
    >
      <div className="glass-panel w-full max-w-6xl rounded-full px-8 py-3 flex items-center justify-between border-white/5">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center group-hover:rotate-12 transition-transform duration-300">
            <span className="text-black font-black text-xs">JAI</span>
          </div>
          <span className="font-mono text-xs uppercase tracking-[0.4em] font-bold">JonnyAI</span>
        </Link>

        {/* Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <Link 
              key={link.name} 
              href={link.href}
              className="text-[10px] uppercase tracking-widest text-white/60 hover:text-accent transition-colors duration-300 flex items-center gap-2"
            >
              <link.icon className="w-3 h-3" />
              {link.name}
            </Link>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4">
          <Link 
            href="/login" 
            className="hidden sm:block text-[10px] uppercase tracking-widest text-white/40 hover:text-white transition-colors duration-300"
          >
            Client Login
          </Link>
          <Link 
            href="/brief" 
            className="group relative flex items-center gap-2 bg-white text-black text-[10px] uppercase tracking-[0.2em] font-black px-6 py-2.5 rounded-full hover:bg-accent transition-all duration-500 overflow-hidden"
          >
            <span className="relative z-10 font-black">CHAT WITH MARCUS</span>
            <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    </motion.nav>
  );
}
