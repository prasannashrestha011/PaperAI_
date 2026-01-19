"use client"
import HeroSection from '@/components/HeroSection';
import FeaturesSection from '@/components/FeaturesSection';
import CursorLight from '@/components/CursorLight';

export default function Home() {
  return (
    <div className="relative bg-slate-950">
      <CursorLight/>
      <HeroSection />
      <FeaturesSection />
    </div>
  );
}
