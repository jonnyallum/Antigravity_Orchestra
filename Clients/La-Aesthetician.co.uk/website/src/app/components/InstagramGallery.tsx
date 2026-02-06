'use client';

import Image from 'next/image';
import { motion } from 'framer-motion';
import { Instagram } from 'lucide-react';

// Using REAL images extracted from client's saved Instagram content
const galleryImages = [
    {
        src: '/images/gallery/photo-1.jpg',
        alt: 'L.A. Aesthetics Treatment',
        caption: 'Natural enhancement'
    },
    {
        src: '/images/gallery/photo-2.jpg',
        alt: 'L.A. Aesthetics Clinic',
        caption: 'Clinic expertise'
    },
    {
        src: '/images/gallery/photo-3.jpg',
        alt: 'Treatment Detail',
        caption: 'Precision & care'
    },
    {
        src: '/images/gallery/photo-4.jpg',
        alt: 'Client Results',
        caption: 'Beautiful results'
    },
    {
        src: '/images/gallery/photo-5.jpg',
        alt: 'Aesthetic Treatment',
        caption: 'Enhancing beauty'
    },
    {
        src: '/images/gallery/photo-6.jpg',
        alt: 'L.A. Aesthetics Result',
        caption: 'Radiant confidence'
    },
    {
        src: '/images/gallery/photo-7.jpg',
        alt: 'L.A. Aesthetics Result',
        caption: 'Radiant confidence'
    },
    {
        src: '/images/gallery/photo-8.jpg',
        alt: 'L.A. Aesthetics Result',
        caption: 'Radiant confidence'
    }
];

export default function InstagramGallery() {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
            {galleryImages.map((image, index) => (
                <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="group relative aspect-square rounded-2xl overflow-hidden bg-taupe/20 border border-gold/20 shadow-sm hover:shadow-xl transition-all duration-500"
                >
                    <Image
                        src={image.src}
                        alt={image.alt}
                        fill
                        className="object-cover transition-transform duration-700 group-hover:scale-110"
                        unoptimized
                    />

                    {/* Gold Overlay Effect */}
                    <div className="absolute inset-0 bg-coffee/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 mix-blend-overlay" />

                    {/* Caption Overlay */}
                    <div className="absolute inset-x-0 bottom-0 p-6 bg-gradient-to-t from-coffee-dark/90 via-coffee-dark/50 to-transparent translate-y-full group-hover:translate-y-0 transition-transform duration-500">
                        <div className="flex items-center gap-2 mb-1">
                            <Instagram className="w-3 h-3 text-gold" />
                            <span className="text-[10px] text-gold uppercase tracking-widest font-medium">L.A. Aesthetics</span>
                        </div>
                        <p className="text-white text-sm font-serif italic">{image.caption}</p>
                    </div>
                </motion.div>
            ))}
        </div>
    );
}
