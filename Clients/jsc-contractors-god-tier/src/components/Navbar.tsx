"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Case Studies", href: "/projects" },
    { name: "Services", href: "/services" },
    { name: "About", href: "/about" },
    { name: "Contact", href: "/contact" },
  ];

  return (
    <nav
      className={cn(
        "fixed top-0 left-0 w-full z-50 transition-all duration-500 px-6 md:px-12",
        scrolled 
          ? "py-4 bg-white/70 backdrop-blur-md border-b border-black/5" 
          : "py-8 bg-transparent"
      )}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* God-Tier Logo */}
        <Link href="/" className="relative group">
          <div className="relative h-12 w-32 md:h-16 md:w-40 transition-transform duration-500 group-hover:scale-105">
            <Image
              src="/assets/jsc-logo.png"
              alt="JSC Contractors"
              fill
              className="object-contain"
              priority
            />
          </div>
          {/* Subtle gold shimmer line on hover */}
          <motion.div 
            className="absolute -bottom-1 left-0 h-[1px] bg-accent w-0 group-hover:w-full transition-all duration-500"
          />
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center space-x-10">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className="text-[11px] uppercase tracking-[0.3em] text-black font-semibold hover:text-accent transition-colors duration-300"
            >
              {link.name}
            </Link>
          ))}
          
          {/* Action Button */}
          <Link
            href="/contact"
            className="px-6 py-2 bg-black text-white text-[10px] uppercase tracking-[0.2em] font-bold hover:bg-accent transition-all duration-300"
          >
            Start Build
          </Link>
        </div>

        {/* Mobile Menu Icon (Placeholder) */}
        <div className="md:hidden">
          <div className="w-6 h-[2px] bg-black mb-1.5" />
          <div className="w-6 h-[2px] bg-black" />
        </div>
      </div>
    </nav>
  );
}
