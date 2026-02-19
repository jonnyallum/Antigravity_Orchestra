"use client";

import { motion } from "framer-motion";
import ImageReveal from "./ImageReveal";
import { cn } from "@/lib/utils";

const projects = [
  {
    title: "New Build Excellence",
    category: "Residential",
    image: "/projects/new-build/IMG_3582.JPG",
    span: "md:col-span-2 md:row-span-2",
  },
  {
    title: "Architectural Roofing",
    category: "Restoration",
    image: "/projects/roofing/IMG_3546.JPG",
    span: "md:col-span-1 md:row-span-1",
  },
  {
    title: "Bespoke Loft Space",
    category: "Renovation",
    image: "/projects/loft-conversion/IMG_3575.JPG",
    span: "md:col-span-1 md:row-span-1",
  },
  {
    title: "Luxury Garden Retreat",
    category: "Specialized",
    image: "/projects/garden-room/686A0484-E359-4473-9FED-E434802B8268.JPG",
    span: "md:col-span-1 md:row-span-2",
  },
  {
    title: "Modern Container Living",
    category: "Innovation",
    image: "/projects/container-conversion/4084c0d5-3547-4167-9bb8-bf2ec6d4ccae.jpeg",
    span: "md:col-span-1 md:row-span-1",
  },
];

export default function Projects() {
  return (
    <section className="py-24 px-6 md:px-12 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-end justify-between mb-16 gap-8">
          <div className="max-w-2xl">
            <span className="text-accent text-[10px] uppercase tracking-[0.4em] font-bold mb-4 block">
              Our Portfolio
            </span>
            <h2 className="text-4xl md:text-6xl font-serif text-black leading-tight">
              Selected Works of <span className="italic text-neutral-400 underline decoration-accent/30 underline-offset-8">Distinction</span>
            </h2>
          </div>
          <p className="text-neutral-500 font-sans max-w-sm text-sm leading-relaxed">
            A testament to precision and heritage standards. Hover to reveal the true finish of our craftsmanship.
          </p>
        </div>

        {/* Masonry-ish Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[300px]">
          {projects.map((project, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.1, duration: 0.8 }}
              className={cn("relative group", project.span)}
            >
              <ImageReveal 
                src={project.image} 
                alt={project.title} 
                className="h-full"
              />
              <div className="mt-4 flex items-center justify-between">
                <div>
                  <h3 className="text-[12px] uppercase tracking-[0.2em] font-bold text-black">
                    {project.title}
                  </h3>
                  <span className="text-[10px] text-neutral-400 uppercase tracking-widest">
                    {project.category}
                  </span>
                </div>
                <div className="w-8 h-[1px] bg-neutral-200 group-hover:w-16 group-hover:bg-accent transition-all duration-500" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
