'use client';

export default function HomeHero() {
  return (
    <section className="relative w-full min-h-[500px] flex items-center justify-center pt-24 pb-12 overflow-hidden">
      {/* Animated Gradient Mesh Background */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob"></div>
        <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-blob animation-delay-4000"></div>
      </div>

      {/* Grid Background Pattern */}
      <div className="absolute inset-0 pointer-events-none opacity-10" style={{
        backgroundImage: `
          linear-gradient(rgba(34, 211, 238, 0.5) 1px, transparent 1px),
          linear-gradient(90deg, rgba(34, 211, 238, 0.5) 1px, transparent 1px)
        `,
        backgroundSize: '70px 75px'
      }}></div>

      {/* Content */}
      <div className="relative z-10 w-full max-w-4xl px-4 md:px-8 text-center">
        {/* Greeting Badge */}
        <div className="inline-block mb-6 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
          👋 Welcome to Your Dashboard
        </div>

        {/* Main Heading */}
        <h1 className="text-5xl sm:text-6xl md:text-7xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 mb-6 drop-shadow-2xl tracking-tight leading-tight" style={{ fontFamily: 'var(--font-sora)' }}>
          Manage Your Documents
        </h1>

        {/* Subheading */}
        <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed" style={{ fontFamily: 'var(--font-inter)' }}>
          Upload documents, perform intelligent searches, ask questions with citations, and leverage AI-powered insights powered by Gemini and Graph RAG technology.
        </p>

        {/* Feature Pills */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          <div className="px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            🚀 Fast Upload
          </div>
          <div className="px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            🔍 Smart Search
          </div>
          <div className="px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            💬 Ask Questions
          </div>
        </div>
      </div>
    </section>
  );
}
