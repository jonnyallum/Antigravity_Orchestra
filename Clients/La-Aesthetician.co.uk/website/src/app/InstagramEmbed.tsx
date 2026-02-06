'use client';

import { useEffect, useState } from 'react';
import { Instagram } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface InstagramEmbedProps {
    url: string;
    caption?: string;
}

export default function InstagramEmbed({ url, caption }: InstagramEmbedProps) {
    const [isLoaded, setIsLoaded] = useState(false);
    const [loadError, setLoadError] = useState(false);
    const [showFallback, setShowFallback] = useState(false);

    // Extract ID from URL for link
    const reelId = url.split('/reel/')[1]?.split('/')[0] || url.split('/p/')[1]?.split('/')[0];

    useEffect(() => {
        // Set a timeout to show fallback if it takes too long to load
        // or if the iframe fails to communicate
        const timer = setTimeout(() => {
            if (!isLoaded) {
                setShowFallback(true);
            }
        }, 5000);

        return () => clearTimeout(timer);
    }, [isLoaded]);

    const handleLoad = () => {
        setIsLoaded(true);
        setShowFallback(false);
    };

    const handleError = () => {
        setLoadError(true);
        setShowFallback(true);
    };

    return (
        <div className="relative w-full h-full bg-white flex flex-col items-center justify-center overflow-hidden">
            <AnimatePresence>
                {!isLoaded && !loadError && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-cream"
                    >
                        <div className="w-12 h-12 border-2 border-coffee/20 border-t-coffee rounded-full animate-spin mb-4" />
                        <p className="text-xs text-coffee/60 font-medium uppercase tracking-widest">Loading Reel...</p>
                    </motion.div>
                )}
            </AnimatePresence>

            {!loadError ? (
                <iframe
                    src={`${url}embed/captioned/`}
                    className={`w-full h-full transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
                    frameBorder="0"
                    scrolling="no"
                    allowTransparency={true}
                    onLoad={handleLoad}
                    onError={handleError}
                />
            ) : null}

            {(loadError || showFallback) && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="absolute inset-0 flex flex-col items-center justify-center p-8 text-center bg-cream z-20"
                >
                    <div className="w-16 h-16 bg-coffee/10 rounded-full flex items-center justify-center mb-6">
                        <Instagram className="w-8 h-8 text-coffee" />
                    </div>
                    <h4 className="font-serif text-xl text-charcoal mb-2">View on Instagram</h4>
                    <p className="text-sm text-charcoal-light mb-8 max-w-[200px]">
                        {caption || "Check out this clinical result on our official page."}
                    </p>
                    <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-luxury py-3 px-8 text-[10px]"
                    >
                        <span>Open Post</span>
                    </a>

                    <p className="text-[10px] text-charcoal-light/40 mt-8 uppercase tracking-widest">
                        Privacy restrictions may block embeds in some browsers
                    </p>
                </motion.div>
            )}
        </div>
    );
}
