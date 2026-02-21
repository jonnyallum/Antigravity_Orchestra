import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "JonnyAI | Build at the Speed of Thought",
  description: "The AI Product Engine for Trillion-Dollar Startups. 48-hour builds. Real-time transparency. 50% Off Early Adopter Offer.",
  metadataBase: new URL("https://jonnyai.co.uk"),
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased relative min-h-screen`}
      >
        {/* Global Noise Overlay */}
        <div className="bg-noise absolute inset-0 fixed" />
        
        <main className="relative z-10">
          {children}
        </main>
      </body>
    </html>
  );
}
