import Image from "next/image";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-black text-white py-24 px-6 md:px-12">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-16 mb-24">
          <div className="md:col-span-2">
            <div className="h-10 w-32 relative mb-12">
              <Image
                src="/assets/jsc-logo-white.png"
                alt="JSC Contractors"
                fill
                className="object-contain"
              />
            </div>
            <p className="text-white/40 text-lg font-sans max-w-sm mb-12 italic leading-relaxed">
              "Building the future of West Sussex through the lens of heritage and craftsmanship."
            </p>
            <div className="flex gap-8">
              {['Instagram', 'LinkedIn', 'Houzz'].map(social => (
                <Link key={social} href="#" className="text-[10px] uppercase tracking-widest text-white/60 hover:text-accent transition-colors">
                  {social}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-[10px] uppercase tracking-[0.4em] font-bold mb-8 text-neutral-500">Contact</h4>
            <div className="space-y-4 text-sm font-sans text-white/60">
              <p>West Sussex, United Kingdom</p>
              <p>info@jsccontractors.co.uk</p>
              <p>+44 (0) 1243 000 000</p>
            </div>
          </div>

          <div>
            <h4 className="text-[10px] uppercase tracking-[0.4em] font-bold mb-8 text-neutral-500">Navigation</h4>
            <div className="flex flex-col space-y-4 text-sm font-sans text-white/60">
              {['Home', 'Projects', 'Services', 'About', 'Contact'].map(link => (
                <Link key={link} href="#" className="hover:text-white transition-colors">{link}</Link>
              ))}
            </div>
          </div>
        </div>

        <div className="border-t border-white/5 pt-12 flex flex-col md:flex-row items-center justify-between gap-8">
          <span className="text-[10px] uppercase tracking-widest text-neutral-600">
            © 2026 JSC Contractors Ltd.
          </span>
          <span className="text-[9px] uppercase tracking-widest text-neutral-800">
            Designed with Jai.OS 4.0 Collective Velocity
          </span>
        </div>
      </div>
    </footer>
  );
}
