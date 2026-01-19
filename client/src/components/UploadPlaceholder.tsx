export default function UploadPlaceholder() {
  return (
    <section className="py-20 bg-slate-950 relative">
      <div className="max-w-3xl mx-auto px-4">
        <div className="border border-cyan-500/30 rounded-2xl p-12 bg-linear-to-br from-slate-900 to-slate-800 shadow-2xl shadow-cyan-500/10 hover:shadow-cyan-500/20 transition-all duration-300 hover:border-cyan-500/50">
          <h2 className="text-3xl font-black text-transparent bg-clip-text bg-linear-to-r from-blue-400 to-cyan-300 mb-4" style={{ fontFamily: 'var(--font-sora)' }}>
            Upload Your Document
          </h2>
          <p className="text-gray-400 mb-8 text-lg" style={{ fontFamily: 'var(--font-inter)' }}>
            Drag and drop your PDF or click to select. (UI only, backend coming soon)
          </p>
          <div className="flex justify-center">
            <button className="px-8 py-4 rounded-lg bg-linear-to-r from-blue-500 to-cyan-400 text-slate-950 font-bold shadow-lg hover:shadow-cyan-500/50 transition hover:scale-105 transform duration-200 opacity-70 cursor-not-allowed" style={{ fontFamily: 'var(--font-sora)' }}>
              Choose File
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
