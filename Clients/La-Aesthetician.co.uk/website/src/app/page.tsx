'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import Image from 'next/image';
import {
  Phone,
  Instagram,
  Award,
  Clock,
  Shield,
  Sparkles,
  Star,
  ChevronDown,
  MapPin,
  Calendar,
  Heart,
  Syringe,
  Droplets,
  Zap,
  MessageCircle
} from 'lucide-react';

// ═══════════════════════════════════════════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════════════════════════════════════════

const services = [
  {
    icon: Heart,
    title: 'Dermal Fillers',
    description: 'Restore volume and enhance natural contours with premium hyaluronic acid fillers.',
    areas: ['Lips', 'Cheeks', 'Chin', 'Jawline', 'Tear Trough', 'Non-Surgical Rhinoplasty'],
    price: 'From £100',
  },
  {
    icon: Droplets,
    title: 'Skin Boosters',
    description: 'Deep hydration and collagen stimulation for radiant, youthful skin.',
    areas: ['Face', 'Neck', 'Décolletage', 'Hands'],
    price: 'From £50',
  },
  {
    icon: Zap,
    title: 'Anti-Wrinkle',
    description: 'Smooth expression lines and prevent future wrinkles with precise treatment.',
    areas: ['Forehead', 'Frown Lines', 'Crow\'s Feet', 'Advanced Areas'],
    price: 'From £150',
  },
  {
    icon: Syringe,
    title: 'Polynucleotides',
    description: 'Regenerative DNA therapy for deep skin renewal and repair.',
    areas: ['Under Eyes', 'Face', 'Neck', 'Scalp'],
    price: 'From £110',
  },
];

const stats = [
  { value: '10+', label: 'Years Experience' },
  { value: '200+', label: 'Happy Clients' },
  { value: '5★', label: 'Client Rating' },
  { value: '100%', label: 'Clinical Standards' },
];

const testimonials = [
  {
    text: "Libby made me feel so comfortable during my first filler appointment. The results are so natural - exactly what I wanted!",
    author: "Sophie M.",
    treatment: "Lip Fillers",
  },
  {
    text: "As a registered nurse herself, I knew I was in safe hands. The attention to detail and aftercare is exceptional.",
    author: "Emma T.",
    treatment: "Anti-Wrinkle",
  },
  {
    text: "Finally found someone who understands 'less is more'. My skin has never looked better after the polynucleotides treatment.",
    author: "Rachel K.",
    treatment: "Polynucleotides",
  },
];

const processSteps = [
  {
    step: '01',
    title: 'Consultation',
    description: 'A thorough assessment of your goals, medical history, and facial anatomy.',
  },
  {
    step: '02',
    title: 'Personalised Plan',
    description: 'Bespoke treatment recommendations tailored to achieve your desired results.',
  },
  {
    step: '03',
    title: 'Treatment',
    description: 'Expert application using premium products in a comfortable, clinical setting.',
  },
  {
    step: '04',
    title: 'Aftercare',
    description: 'Comprehensive guidance and follow-up support for optimal results.',
  },
];

// ═══════════════════════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════════

function Navigation() {
  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.4, 0, 0.2, 1] }}
      className="fixed top-0 left-0 right-0 z-50 bg-cream/80 backdrop-blur-lg border-b border-coffee/10"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="#" className="font-serif text-2xl text-charcoal tracking-wide">
          L.A. <span className="text-coffee">Aesthetics</span>
        </a>

        <div className="hidden md:flex items-center gap-8">
          {['Services', 'About', 'Process', 'Testimonials', 'Contact'].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="text-sm font-sans font-medium text-charcoal-light hover:text-coffee transition-colors tracking-wide"
            >
              {item}
            </a>
          ))}
        </div>

        <a
          href="https://squareup.com/appointments/book/la-aesthetics"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-luxury text-xs py-3 px-6"
        >
          <span>Book Now</span>
        </a>
      </div>
    </motion.nav>
  );
}

function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [0, 200]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center overflow-hidden bg-taupe-light">
      {/* Background Pattern & Hero Image */}
      <div className="absolute inset-0">
        <Image
          src="/images/hero-bg-new.jpg"
          alt="L.A. Aesthetics Atmosphere"
          fill
          className="object-cover opacity-20 blur-[10px] scale-110"
          unoptimized
        />
        <div className="absolute inset-0 bg-gradient-to-b from-taupe-light/90 via-taupe-light/70 to-taupe-light/90 mix-blend-soft-light" />
        <div className="absolute inset-0 bg-gradient-to-t from-taupe-light via-transparent to-taupe-light opacity-80" />
      </div>

      {/* Floating Elements */}
      <motion.div
        style={{ y }}
        className="absolute top-20 right-20 w-72 h-72 bg-coffee/10 rounded-full blur-3xl"
      />
      <motion.div
        style={{ y: useTransform(scrollYProgress, [0, 1], [0, 100]) }}
        className="absolute bottom-20 left-20 w-96 h-96 bg-cloud/20 rounded-full blur-3xl"
      />

      <motion.div
        style={{ opacity }}
        className="relative z-10 max-w-5xl mx-auto px-6 text-center"
      >
        {/* Award Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="inline-flex items-center gap-2 px-4 py-2 bg-white/60 backdrop-blur-sm rounded-full border border-coffee/20 mb-8"
        >
          <Award className="w-4 h-4 text-gold" />
          <span className="text-xs font-sans font-medium text-charcoal tracking-wide">
            UK Hair & Beauty Awards 2025 Finalist
          </span>
        </motion.div>

        {/* Main Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.2 }}
          className="font-serif text-5xl md:text-7xl lg:text-8xl text-charcoal mb-6 leading-[1.1]"
        >
          Natural Beauty,
          <br />
          <span className="text-coffee italic">Expert Care</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.4 }}
          className="font-sans text-lg md:text-xl text-charcoal-light max-w-2xl mx-auto mb-12 leading-relaxed"
        >
          Premium aesthetic treatments by Libby, Registered Nurse with over 10 years
          in the beauty industry. Enhancing your natural beauty with clinical precision.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href="https://squareup.com/appointments/book/la-aesthetics"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-luxury"
          >
            <span>Book Consultation</span>
          </a>
          <a href="#services" className="btn-luxury btn-luxury-outline">
            <span>View Treatments</span>
          </a>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.8 }}
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8"
        >
          {stats.map((stat, i) => (
            <div key={stat.label} className="text-center">
              <div className="font-serif text-4xl md:text-5xl text-coffee mb-2">{stat.value}</div>
              <div className="font-sans text-xs uppercase tracking-widest text-charcoal-light">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="flex flex-col items-center gap-2 text-charcoal-light"
        >
          <span className="text-xs font-sans uppercase tracking-widest">Discover</span>
          <ChevronDown className="w-5 h-5" />
        </motion.div>
      </motion.div>
    </section>
  );
}

function About() {
  return (
    <section id="about" className="py-32 bg-cream relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Image Side */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="aspect-[4/5] rounded-[2rem] overflow-hidden relative group shadow-2xl">
              <Image
                src="/images/libby.jpg"
                alt="Libby - Registered Nurse & Founder"
                fill
                className="object-cover transition-transform duration-700 group-hover:scale-105"
                unoptimized
              />

              {/* Overlay Badge */}
              <div className="absolute bottom-6 left-6 right-6">
                <div className="bg-white/90 backdrop-blur md:p-6 p-4 rounded-xl border border-coffee/10 shadow-lg">
                  <p className="font-serif text-xl text-coffee mb-1">Libby</p>
                  <div className="flex items-center gap-2 text-xs text-charcoal-light uppercase tracking-widest">
                    <Award className="w-3 h-3 text-gold" />
                    <span>RN Qualified</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Overlay gradient */}
            <div className="absolute inset-0 bg-gradient-to-t from-charcoal/20 to-transparent" />

            {/* Decorative border */}
            <div className="absolute -inset-4 border-2 border-coffee/20 rounded-[2.5rem] -z-10" />


            {/* Floating Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="absolute -bottom-8 -right-8 bg-white p-6 rounded-2xl shadow-xl border border-coffee/10"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-coffee/10 rounded-full flex items-center justify-center">
                  <Shield className="w-6 h-6 text-coffee" />
                </div>
                <div>
                  <p className="font-serif text-lg text-charcoal">RN Qualified</p>
                  <p className="text-xs text-muted">Fully Insured</p>
                </div>
              </div>
            </motion.div>
          </motion.div>

          {/* Content Side */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <span className="section-subtitle">Meet Your Practitioner</span>
            <h2 className="section-title mb-6">
              A Passion for<br />
              <span className="text-coffee italic">Natural Enhancement</span>
            </h2>

            <div className="space-y-6 text-charcoal-light leading-relaxed">
              <p>
                Hello, I&apos;m Libby – the owner of LA Aesthetics. I&apos;m a Nurse-Led aesthetics clinic owner in Havant, specialising in a range of injectable treatments.
              </p>
              <p>
                My aim is to make every woman feel their absolute best, by enhancing their natural beauty through precision &quot;tweakments&quot;.
              </p>
              <p>
                You can relax knowing you&apos;re in the safe and well trained hands of a perfectionist. My philosophy is simple: enhance your natural beauty, never mask it. I believe in subtle, refined results that leave you looking refreshed.
              </p>
            </div>

            {/* Credentials */}
            <div className="mt-10 grid grid-cols-2 gap-6">
              {[
                { icon: Award, text: 'Best New Talent Finalist 2025' },
                { icon: Shield, text: 'Fully Insured & Registered' },
                { icon: Clock, text: '10+ Years Industry Experience' },
                { icon: Star, text: '5-Star Client Reviews' },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-coffee/10 rounded-full flex items-center justify-center">
                    <item.icon className="w-5 h-5 text-coffee" />
                  </div>
                  <span className="text-sm text-charcoal font-medium">{item.text}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div >
    </section >
  );
}

function Services() {
  return (
    <section id="services" className="py-32 bg-taupe-light relative">
      {/* Background Decoration */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-coffee/5 to-transparent" />

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <span className="section-subtitle">Treatment Menu</span>
          <h2 className="section-title">
            Premium <span className="text-coffee italic">Treatments</span>
          </h2>
          <p className="mt-6 text-charcoal-light max-w-2xl mx-auto">
            Each treatment includes a personalized consultation and comprehensive aftercare guidance.
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {services.map((service, i) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="service-card p-8 rounded-2xl group"
            >
              {/* Icon */}
              <div className="w-14 h-14 bg-coffee/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-coffee/20 transition-colors">
                <service.icon className="w-7 h-7 text-coffee" />
              </div>

              {/* Title & Price */}
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-serif text-2xl text-charcoal">{service.title}</h3>
                <span className="font-sans text-sm font-medium text-coffee bg-coffee/10 px-3 py-1 rounded-full">
                  {service.price}
                </span>
              </div>

              {/* Description */}
              <p className="text-charcoal-light mb-6">{service.description}</p>

              {/* Treatment Areas */}
              <div className="flex flex-wrap gap-2">
                {service.areas.map((area) => (
                  <span
                    key={area}
                    className="text-xs font-medium text-charcoal-light bg-taupe px-3 py-1 rounded-full"
                  >
                    {area}
                  </span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <a
            href="https://squareup.com/appointments/book/la-aesthetics"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-luxury"
          >
            <span>Book Your Treatment</span>
          </a>
        </motion.div>
      </div>
    </section>
  );
}

function Process() {
  return (
    <section id="process" className="py-32 bg-cream">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <span className="section-subtitle">Your Journey</span>
          <h2 className="section-title">
            The <span className="text-coffee italic">Experience</span>
          </h2>
        </motion.div>

        {/* Process Steps */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {processSteps.map((step, i) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="relative"
            >
              {/* Connector Line */}
              {i < processSteps.length - 1 && (
                <div className="hidden lg:block absolute top-8 left-full w-full h-[1px] bg-gradient-to-r from-coffee/40 to-transparent z-0" />
              )}

              <div className="relative z-10 text-center lg:text-left">
                {/* Step Number */}
                <div className="inline-flex items-center justify-center w-16 h-16 bg-coffee text-white font-serif text-2xl rounded-full mb-6">
                  {step.step}
                </div>

                <h3 className="font-serif text-xl text-charcoal mb-3">{step.title}</h3>
                <p className="text-charcoal-light text-sm leading-relaxed">{step.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Testimonials() {
  return (
    <section id="testimonials" className="py-32 bg-charcoal relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, var(--coffee) 1px, transparent 0)`,
          backgroundSize: '60px 60px'
        }} />
      </div>

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <span className="text-coffee-light text-xs font-sans font-medium tracking-[0.25em] uppercase">
            Client Stories
          </span>
          <h2 className="font-serif text-4xl md:text-5xl text-white mt-4">
            Words from <span className="text-coffee italic">Happy Clients</span>
          </h2>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="bg-white/5 backdrop-blur-sm border border-white/10 p-8 rounded-2xl"
            >
              {/* Stars */}
              <div className="flex gap-1 mb-6">
                {[...Array(5)].map((_, j) => (
                  <Star key={j} className="w-4 h-4 text-gold fill-gold" />
                ))}
              </div>

              {/* Quote */}
              <p className="text-white/80 leading-relaxed mb-6 italic">
                &quot;{testimonial.text}&quot;
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-coffee/20 rounded-full flex items-center justify-center">
                  <span className="font-serif text-coffee">{testimonial.author[0]}</span>
                </div>
                <div>
                  <p className="text-white font-medium">{testimonial.author}</p>
                  <p className="text-white/50 text-xs">{testimonial.treatment}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

import InstagramGallery from './components/InstagramGallery';

function Socials() {
  return (
    <section id="socials" className="py-32 bg-taupe-light">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <span className="section-subtitle">Follow the Results</span>
          <h2 className="section-title">
            Latest from <span className="text-coffee italic">Instagram</span>
          </h2>
        </div>

        <InstagramGallery />

        <div className="text-center mt-12">
          <a
            href="https://instagram.com/la.aesthetics_rn"
            target="_blank"
            rel="noopener noreferrer"
            className="text-charcoal-light font-sans text-sm tracking-widest uppercase hover:text-coffee transition-colors"
          >
            View More on Instagram @la.aesthetics_rn
          </a>
        </div>
      </div>
    </section>
  );
}

function Contact() {
  return (
    <section id="contact" className="py-32 bg-cream">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
          {/* Info Side */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <span className="section-subtitle">Get in Touch</span>
            <h2 className="section-title mb-6">
              Ready to Begin Your<br />
              <span className="text-coffee italic">Transformation?</span>
            </h2>

            <p className="text-charcoal-light mb-10 max-w-md">
              Book your consultation today and take the first step towards enhancing your natural beauty.
            </p>

            {/* Contact Info */}
            <div className="space-y-6">
              <a
                href="tel:07702320230"
                className="flex items-center gap-4 p-4 bg-white rounded-xl border border-coffee/10 hover:border-coffee/30 transition-colors group"
              >
                <div className="w-12 h-12 bg-coffee/10 rounded-full flex items-center justify-center group-hover:bg-coffee/20 transition-colors">
                  <Phone className="w-5 h-5 text-coffee" />
                </div>
                <div>
                  <p className="text-xs text-muted uppercase tracking-wider">Call or WhatsApp</p>
                  <p className="font-serif text-xl text-charcoal">0770 232 0230</p>
                </div>
              </a>

              <a
                href="https://instagram.com/la.aesthetics_rn"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 p-4 bg-white rounded-xl border border-coffee/10 hover:border-coffee/30 transition-colors group"
              >
                <div className="w-12 h-12 bg-coffee/10 rounded-full flex items-center justify-center group-hover:bg-coffee/20 transition-colors">
                  <Instagram className="w-5 h-5 text-coffee" />
                </div>
                <div>
                  <p className="text-xs text-muted uppercase tracking-wider">Follow on Instagram</p>
                  <p className="font-serif text-xl text-charcoal">@la.aesthetics_rn</p>
                </div>
              </a>

              <div className="flex items-center gap-4 p-4 bg-white rounded-xl border border-coffee/10">
                <div className="w-12 h-12 bg-coffee/10 rounded-full flex items-center justify-center">
                  <MapPin className="w-5 h-5 text-coffee" />
                </div>
                <div>
                  <p className="text-xs text-muted uppercase tracking-wider">Location</p>
                  <p className="font-serif text-xl text-charcoal">United Kingdom</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Booking CTA Side */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-coffee to-coffee-dark p-10 md:p-16 rounded-3xl text-white relative overflow-hidden"
          >
            {/* Decorative */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

            <div className="relative z-10">
              <Calendar className="w-12 h-12 mb-6 text-white/80" />

              <h3 className="font-serif text-3xl md:text-4xl mb-4">
                Book Your<br />Consultation
              </h3>

              <p className="text-white/80 mb-8">
                Schedule your appointment online and receive a confirmation within 24 hours.
              </p>

              <a
                href="https://squareup.com/appointments/book/la-aesthetics"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center w-full py-4 px-8 bg-white text-coffee font-sans text-sm font-medium uppercase tracking-widest hover:bg-taupe transition-colors"
              >
                Book Online Now
              </a>

              <p className="text-white/60 text-xs mt-6 text-center">
                Or message via WhatsApp for availability
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="bg-charcoal py-16">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          {/* Logo */}
          <div className="text-center md:text-left">
            <a href="#" className="font-serif text-2xl text-white tracking-wide">
              L.A. <span className="text-coffee">Aesthetics</span>
            </a>
            <p className="text-white/40 text-sm mt-2">Natural Beauty, Expert Care</p>
          </div>

          {/* Social */}
          <div className="flex items-center gap-4">
            <a
              href="https://instagram.com/la.aesthetics_rn"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-white/60 hover:bg-coffee/20 hover:text-coffee transition-colors"
            >
              <Instagram className="w-5 h-5" />
            </a>
            <a
              href="https://wa.me/447702320230"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-white/60 hover:bg-coffee/20 hover:text-coffee transition-colors"
            >
              <MessageCircle className="w-5 h-5" />
            </a>
          </div>

          {/* Copyright */}
          <div className="text-center md:text-right">
            <p className="text-white/40 text-xs">
              © {new Date().getFullYear()} L.A. Aesthetics. All rights reserved.
            </p>
            <a
              href="https://www.jonnyai.co.uk"
              target="_blank"
              rel="noopener noreferrer"
              className="text-white/30 text-[10px] hover:text-coffee transition-colors mt-1 inline-block"
            >
              Crafted by JonnyAi | Jai.OS 4.0
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ═══════════════════════════════════════════════════════════════════════════════

export default function Home() {
  return (
    <main>
      <Navigation />
      <Hero />
      <About />
      <Services />
      <Process />
      <Testimonials />
      <Socials />
      <Contact />
      <Footer />
    </main>
  );
}
