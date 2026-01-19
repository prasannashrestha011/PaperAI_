import type { Metadata } from "next";
import { Sora, Outfit, Inter, Space_Mono } from "next/font/google";
import "./globals.css";
import AuthInitializer from "@/components/AuthInitializer";

const sora = Sora({
  variable: "--font-sora",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const spaceMono = Space_Mono({
  variable: "--font-space-mono",
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  title: "PaperAI - Intelligent Document Analysis",
  description: "RAG-powered document analysis and question answering platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${sora.variable} ${outfit.variable} ${inter.variable} ${spaceMono.variable} antialiased`}
        style={{ fontFamily: 'var(--font-inter)' }}
      >
        <AuthInitializer />
        {children}
      </body>
    </html>
  );
}
