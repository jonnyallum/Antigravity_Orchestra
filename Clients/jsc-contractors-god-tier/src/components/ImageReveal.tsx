"use client";

import { motion, useMotionValue, useSpring } from "framer-motion";
import Image from "next/image";
import { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";

interface ImageRevealProps {
  src: string;
  alt: string;
  className?: string;
}

export default function ImageReveal({ src, alt, className }: ImageRevealProps) {
  const [isHovered, setIsHovered] = useState(false);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springX = useSpring(mouseX, { stiffness: 300, damping: 30 });
  const springY = useSpring(mouseY, { stiffness: 300, damping: 30 });

  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!containerRef.current) return;
    const { left, top, width, height } = containerRef.current.getBoundingClientRect();
    const x = ((e.clientX - left) / width) * 100;
    const y = ((e.clientY - top) / height) * 100;
    mouseX.set(x);
    mouseY.set(y);
  };

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={cn(
        "relative overflow-hidden cursor-none group aspect-[3/2] w-full bg-neutral-200",
        className
      )}
    >
      {/* Greyscale Base Layer */}
      <Image
        src={src}
        alt={alt}
        fill
        className="object-cover transition-transform duration-700 group-hover:scale-105 grayscale"
        sizes="(max-width: 768px) 100vw, 50vw"
      />

      {/* Color Reveal Layer (Spotlight) */}
      <motion.div
        className="absolute inset-0 z-10 pointer-events-none"
        style={{
          clipPath: isHovered 
            ? `circle(150px at ${springX}% ${springY}%)` 
            : `circle(0px at 50% 50%)`,
          transition: "clip-path 0.1s ease-out"
        }}
      >
        <Image
          src={src}
          alt={alt}
          fill
          className="object-cover scale-105"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
      </motion.div>

      {/* Decorative Border / Frame */}
      <div className="absolute inset-0 border border-black/5 pointer-events-none group-hover:border-accent/20 transition-colors duration-500" />
      
      {/* Label (Visible on Hover) */}
      <div className="absolute bottom-4 left-4 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <span className="text-[10px] uppercase tracking-[0.2em] text-white bg-black/80 px-2 py-1 backdrop-blur-sm">
          Craftsmanship Revealed
        </span>
      </div>
    </div>
  );
}
