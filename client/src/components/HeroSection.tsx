export default function HeroSection() {
  return (
    <section className="relative w-full h-screen flex items-center justify-center overflow-hidden bg-slate-950">
      {/* Animated Gradient Mesh Background */}
      <div className="absolute inset-0 gradient-mesh-bg pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Grid Background Pattern */}
      <div className="absolute inset-0 pointer-events-none opacity-20" style={{
        backgroundImage: `
          linear-gradient(rgba(34, 211, 238, 0.5) 1px, transparent 1px),
          linear-gradient(90deg, rgba(34, 211, 238, 0.5) 1px, transparent 1px)
        `,
        backgroundSize: '70px 75px'
      }}></div>

      {/* Content */}
      <div className="relative z-10 w-full max-w-6xl px-4 md:px-8">

        {/* Main Heading */}
        <div className="mb-8 text-center">
          <h1 className="text-7xl sm:text-8xl md:text-9xl font-black text-transparent bg-clip-text bg-linear-to-r from-blue-400 via-cyan-300 to-indigo-400 mb-6 drop-shadow-2xl tracking-tight leading-tight" style={{ fontFamily: 'var(--font-sora)' }}>
            PaperAI
          </h1>
          <div className="h-1 w-32 mx-auto bg-linear-to-r from-blue-400 via-cyan-300 to-indigo-400 rounded-full mb-8"></div>
        </div>

        {/* Subheading - Larger and More Prominent */}
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6 text-center max-w-4xl mx-auto leading-tight" style={{ fontFamily: 'var(--font-outfit)' }}>
          Transform Your Documents into Knowledge with AI
        </h2>

        {/* Description - Enhanced */}
        <p className="text-lg md:text-xl text-gray-300 mb-8 text-center max-w-3xl mx-auto leading-relaxed" style={{ fontFamily: 'var(--font-inter)' }}>
          Powered by Gemini AI and Neo4j Graph Database. Upload documents, perform semantic searches, get intelligent answers with citations, and leverage graph RAG technology for superior context understanding.
        </p>

        {/* Feature Pills */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          <div className="px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            ✨ Graph RAG
          </div>
          <div className="px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            🧠 Deep Agent
          </div>
          <div className="px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            📊 Neo4j Powered
          </div>
          <div className="px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 text-sm font-semibold" style={{ fontFamily: 'var(--font-inter)' }}>
            🚀 Gemini AI
          </div>
        </div>

        {/* CTA Buttons - Enhanced */}
        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
          <a 
            href="/register" 
            className="px-10 py-4 rounded-lg bg-linear-to-r from-blue-500 to-cyan-400 text-slate-950 font-bold shadow-lg hover:shadow-cyan-500/50 transition hover:scale-105 transform duration-200 text-center text-lg"
            style={{ fontFamily: 'var(--font-sora)' }}
          >
            Get Started Free
          </a>
          <a 
            href="#feature" 
            className="px-10 py-4 rounded-lg bg-slate-800 text-cyan-300 font-bold border border-cyan-500/50 shadow-lg hover:bg-slate-700 transition hover:scale-105 transform duration-200 text-center text-lg"
            style={{ fontFamily: 'var(--font-sora)' }}
          >
            Explore Features
          </a>
        </div>

        {/* Stats Row */}
        <div className="flex flex-col sm:flex-row justify-center gap-8 sm:gap-12 pt-8 border-t border-cyan-500/10">
          <div className="text-center">
            <div className="text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-cyan-300" style={{ fontFamily: 'var(--font-sora)' }}>
              100%
            </div>
            <p className="text-gray-400 mt-2" style={{ fontFamily: 'var(--font-inter)' }}>Accurate Citations</p>
          </div>
          <div className="text-center">
            <div className="text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-linear-to-r from-cyan-300 to-indigo-400" style={{ fontFamily: 'var(--font-sora)' }}>
              Lightning
            </div>
            <p className="text-gray-400 mt-2" style={{ fontFamily: 'var(--font-inter)' }}>Fast Processing</p>
          </div>
          <div className="text-center">
            <div className="text-3xl md:text-4xl font-black text-transparent bg-clip-text bg-linear-to-r from-indigo-400 to-purple-400" style={{ fontFamily: 'var(--font-sora)' }}>
              Graph DB
            </div>
            <p className="text-gray-400 mt-2" style={{ fontFamily: 'var(--font-inter)' }}>Advanced Knowledge</p>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes blob {
          0%, 100% {
            transform: translate(0, 0) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </section>
  );
}
