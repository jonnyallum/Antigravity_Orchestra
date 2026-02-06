import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "L.A. Aesthetics | Premium Aesthetic Treatments | Registered Nurse",
  description: "Award-nominated aesthetic clinic offering dermal fillers, anti-wrinkle treatments, skin boosters & polynucleotides. Natural results by Libby, Registered Nurse with 10+ years experience.",
  keywords: ["aesthetics", "dermal fillers", "lip fillers", "anti-wrinkle", "skin boosters", "polynucleotides", "registered nurse", "aesthetic clinic", "UK"],
  authors: [{ name: "L.A. Aesthetics" }],
  openGraph: {
    title: "L.A. Aesthetics | Natural Beauty, Expert Care",
    description: "Premium aesthetic treatments by a Registered Nurse. UK Hair & Beauty Awards 2025 Finalist.",
    type: "website",
    locale: "en_GB",
    url: "https://la-aesthetician.co.uk",
    siteName: "L.A. Aesthetics",
  },
  twitter: {
    card: "summary_large_image",
    title: "L.A. Aesthetics | Premium Aesthetic Treatments",
    description: "Natural beauty, expert care. Book your consultation today.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="antialiased bg-noise">
        {children}
      </body>
    </html>
  );
}
