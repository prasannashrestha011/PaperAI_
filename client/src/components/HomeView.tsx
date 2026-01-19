
'use client';

import HomeHeader from '@/components/HomeHeader';
import HomeHero from '@/components/HomeHero';
import QuickActions from '@/components/QuickActions';
import RecentDocuments from '@/components/RecentDocuments';
import HomeStats from '@/components/HomeStats';
import CursorLight from '@/components/CursorLight';

export default function HomePage() {
  return (
    <div className="relative bg-slate-950 min-h-screen">
      <CursorLight />
      <HomeHeader />
      <main className="pt-16">
        <HomeHero />
        <QuickActions />
        <RecentDocuments />
        <HomeStats />
      </main>
      
      {/* Footer */}
      <footer className="border-t border-cyan-500/20 bg-slate-900/50 py-8 px-4">
        <div className="max-w-6xl mx-auto text-center text-gray-400 text-sm">
          <p>© 2024 PaperAI. Powered by Gemini AI & Neo4j Graph Technology</p>
        </div>
      </footer>
    </div>
  );
}
