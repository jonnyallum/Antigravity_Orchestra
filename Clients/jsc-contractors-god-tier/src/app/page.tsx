import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Projects from "@/components/Projects";
import Services from "@/components/Services";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen selection:bg-accent selection:text-black">
      <Navbar />
      <Hero />
      
      {/* Narrative Section */}
      <section className="py-32 px-6 bg-white flex items-center justify-center">
        <div className="max-w-3xl text-center space-y-12">
          <span className="text-accent text-[10px] uppercase tracking-[0.5em] font-bold block">
            Our Philosophy
          </span>
          <h2 className="text-4xl md:text-6xl font-serif text-black leading-[1.3]">
            We bridge the gap between <span className="italic">Heritage</span> soul and <span className="italic">Modern</span> structure.
          </h2>
          <p className="text-neutral-500 text-lg md:text-xl font-sans leading-relaxed">
            At JSC Contractors, we believe a building is more than just raw materials. It is a legacy. Our West Sussex heritage informs every detail—from the selection of the finest timber to the precision of a modern foundation. 
          </p>
          <div className="h-16 w-[1px] bg-neutral-100 mx-auto" />
        </div>
      </section>

      <Projects />
      <Services />
      
      {/* Final Call to Action */}
      <section className="py-32 px-6 bg-neutral-950 text-white overflow-hidden relative">
        <div className="absolute inset-0 bg-[url('/assets/background.png')] opacity-[0.02] pointer-events-none" />
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <h2 className="text-5xl md:text-8xl font-serif mb-12">
            Ready to <span className="italic text-neutral-500">Build</span> your Legacy?
          </h2>
          <button className="px-16 py-6 bg-accent text-black text-[12px] uppercase tracking-[0.4em] font-black hover:bg-white transition-all transform hover:scale-105 duration-500">
            Secure Your Consulate
          </button>
        </div>
      </section>

      <Footer />
    </main>
  );
}
