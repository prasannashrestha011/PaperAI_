export default function QAPlaceholder() {
  return (
    <section className="py-20 bg-slate-900 relative">
      <div className="max-w-3xl mx-auto px-4">
        <div className="rounded-2xl p-12 bg-linear-to-br from-slate-800 to-slate-900 border border-cyan-500/30 shadow-2xl shadow-cyan-500/10 hover:shadow-cyan-500/20 transition-all duration-300 hover:border-cyan-500/50">
          <h2 className="text-3xl font-black text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-cyan-300 mb-4" style={{ fontFamily: 'var(--font-sora)' }}>
            Ask Your Questions
          </h2>
          <p className="text-gray-400 mb-8 text-lg" style={{ fontFamily: 'var(--font-inter)' }}>
            Get intelligent answers from your documents. (UI only, backend coming soon)
          </p>
          <div className="space-y-4">
            <input
              type="text"
              className="w-full px-4 py-3 rounded-lg bg-slate-700 border border-cyan-500/30 text-gray-300 placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/50 transition"
              style={{ fontFamily: 'var(--font-inter)' }}
              placeholder="E.g. What is the main finding?"
              disabled
            />
            <button className="w-full px-6 py-4 rounded-lg bg-linear-to-r from-blue-500 to-cyan-400 text-slate-950 font-bold shadow-lg opacity-50 cursor-not-allowed transition" style={{ fontFamily: 'var(--font-sora)' }}>
              Ask Question
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
