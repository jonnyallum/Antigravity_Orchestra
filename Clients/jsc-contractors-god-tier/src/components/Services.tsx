"use client";

import { motion } from "framer-motion";
import Image from "next/image";

const services = [
  {
    title: "Residential New Builds",
    description: "From concept to completion, we build high-performance homes that stand the test of time, utilizing heritage materials and modern engineering.",
    image: "/assets/IMG-20260219-WA0001.jpg",
  },
  {
    title: "Heritage Restoration",
    description: "Preserving the architectural soul of West Sussex. Expert masonry, timber framing, and sympathetic renovations.",
    image: "/assets/IMG-20260219-WA0002.jpg",
  },
  {
    title: "Bespoke Extensions",
    description: "Expanding your living space with seamless architectural integrations that elevate the value and aesthetic of your property.",
    image: "/assets/IMG-20260219-WA0003.jpg",
  },
];

export default function Services() {
  return (
    <section className="py-32 px-6 md:px-12 bg-neutral-50 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-accent/5 rounded-full blur-[120px] -z-10" />
      
      <div className="max-w-7xl mx-auto">
        <header className="mb-24 text-center">
          <span className="text-accent text-[10px] uppercase tracking-[0.5em] font-bold mb-4 block">
            Our Expertise
          </span>
          <h2 className="text-5xl md:text-7xl font-serif text-black leading-tight">
            Comprehensive <br /><span className="italic">Building</span> Services
          </h2>
        </header>

        <div className="grid grid-cols-1 gap-32">
          {services.map((service, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 1, ease: "easeOut" }}
              className={`flex flex-col ${idx % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"} items-center gap-12 md:gap-24`}
            >
              <div className="flex-1 space-y-8">
                <span className="text-sm font-sans text-neutral-400 block tracking-[0.2em]">0{idx + 1} —</span>
                <h3 className="text-3xl md:text-5xl font-serif text-black leading-tight italic">
                  {service.title}
                </h3>
                <p className="text-neutral-500 text-lg font-sans leading-relaxed max-w-lg">
                  {service.description}
                </p>
                <div className="pt-6">
                  <button className="text-[11px] uppercase tracking-[0.3em] font-bold text-black group flex items-center gap-4">
                    Explore Details
                    <div className="w-10 h-[1px] bg-black/20 group-hover:w-20 group-hover:bg-accent transition-all duration-500" />
                  </button>
                </div>
              </div>

              <div className="flex-1 w-full aspect-[4/5] relative overflow-hidden grayscale hover:grayscale-0 transition-all duration-1000 group">
                <Image
                  src={service.image}
                  alt={service.title}
                  fill
                  className="object-cover transition-transform duration-1000 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-black/10 group-hover:bg-transparent transition-colors duration-1000" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
