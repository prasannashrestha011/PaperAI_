const features = [
  {
    id: 1,
    title: 'Document Upload',
    description: 'Easily upload PDFs and other documents for instant AI-powered analysis.',
    icon: '📄',
    gradient: 'from-blue-500/20 to-cyan-500/20',
    borderColor: 'border-blue-500/30',
    hoverBorderColor: 'hover:border-blue-400/60',
    accentColor: 'text-blue-300',
    stats: 'Lightning fast'
  },
  {
    id: 2,
    title: 'Semantic Search',
    description: 'Find relevant information across your documents using advanced retrieval.',
    icon: '🔍',
    gradient: 'from-cyan-500/20 to-indigo-500/20',
    borderColor: 'border-cyan-500/30',
    hoverBorderColor: 'hover:border-cyan-400/60',
    accentColor: 'text-cyan-300',
    stats: 'Intelligent search'
  },
  {
    id: 3,
    title: 'Question Answering',
    description: 'Ask questions and get accurate answers from your uploaded content.',
    icon: '🤖',
    gradient: 'from-indigo-500/20 to-purple-500/20',
    borderColor: 'border-indigo-500/30',
    hoverBorderColor: 'hover:border-indigo-400/60',
    accentColor: 'text-indigo-300',
    stats: 'AI Powered'
  },
  {
    id: 4,
    title: 'Citation & Highlighting',
    description: 'Get answers with direct citations and highlighted document snippets.',
    icon: '📑',
    gradient: 'from-purple-500/20 to-pink-500/20',
    borderColor: 'border-purple-500/30',
    hoverBorderColor: 'hover:border-purple-400/60',
    accentColor: 'text-purple-300',
    stats: 'Traceable results'
  },
  {
    id: 5,
    title: 'Graph RAG',
    description: 'Knowledge graphs automatically built from your documents for superior context understanding.',
    icon: '🕸️',
    gradient: 'from-pink-500/20 to-orange-500/20',
    borderColor: 'border-pink-500/30',
    hoverBorderColor: 'hover:border-pink-400/60',
    accentColor: 'text-pink-300',
    stats: 'Contextual retrieval'
  },
  {
    id: 6,
    title: 'Deep Agent Assistant',
    description: 'Multi-step reasoning agent that breaks down complex queries and provides comprehensive answers.',
    icon: '🧠',
    gradient: 'from-orange-500/20 to-red-500/20',
    borderColor: 'border-orange-500/30',
    hoverBorderColor: 'hover:border-orange-400/60',
    accentColor: 'text-orange-300',
    stats: 'Advanced reasoning'
  },
  {
    id: 7,
    title: 'Powered by Gemini',
    description: 'Leveraging Google\'s latest Gemini AI model for state-of-the-art language understanding.',
    icon: '✨',
    gradient: 'from-red-500/20 to-yellow-500/20',
    borderColor: 'border-red-500/30',
    hoverBorderColor: 'hover:border-red-400/60',
    accentColor: 'text-red-300',
    stats: 'Latest AI'
  },
  {
    id: 8,
    title: 'Neo4j Graph DB',
    description: 'Enterprise-grade graph database for efficient knowledge storage and relationship mapping.',
    icon: '🔗',
    gradient: 'from-yellow-500/20 to-green-500/20',
    borderColor: 'border-yellow-500/30',
    hoverBorderColor: 'hover:border-yellow-400/60',
    accentColor: 'text-yellow-300',
    stats: 'Graph-powered'
  },
];

export default function FeaturesSection() {
  return (
    <section id="feature" className="min-h-screen py-28 bg-linear-to-b from-slate-900 via-slate-950 to-slate-900 relative overflow-hidden flex items-center justify-center">
      {/* Decorative background elements */}
      <div className="absolute top-20 left-1/4 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-20 right-1/4 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-7xl mx-auto px-4 relative z-10">
        {/* Header */}
        <div className="text-center mb-20">
        <h2 className="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-linear-to-r from-blue-400 via-cyan-300 to-indigo-400 mb-6" style={{ fontFamily: 'var(--font-sora)' }}>
            Enterprise-Grade Features
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto" style={{ fontFamily: 'var(--font-inter)' }}>
            Advanced AI capabilities powered by Gemini and Neo4j Graph Database for intelligent document analysis
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, idx) => (
            <div
              key={feature.id}
              className={`group relative h-full rounded-2xl overflow-hidden transition-all duration-500 transform hover:scale-105 hover:-translate-y-2
                ${feature.borderColor} ${feature.hoverBorderColor} border backdrop-blur-xl
                bg-linear-to-br from-slate-800/40 to-slate-900/40 hover:shadow-2xl hover:shadow-cyan-500/10`}
            >
              {/* Gradient background */}
              <div className={`absolute inset-0 bg-linear-to-br ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-300`}></div>

              {/* Content */}
              <div className="relative p-8 h-full flex flex-col justify-between">
                {/* Top section with number and icon */}
                <div>
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex-1">
                      <div className="inline-block p-3 rounded-xl bg-slate-700/50 group-hover:bg-slate-600/70 transition-colors mb-4">
                        <span className="text-4xl">{feature.icon}</span>
                      </div>
                    </div>
                    <div className="text-4xl font-black text-slate-700 group-hover:text-slate-600 transition-colors">
                      {String(feature.id).padStart(2, '0')}
                    </div>
                  </div>

                  {/* Title and description */}
                  <h3 className={`text-xl font-bold ${feature.accentColor} mb-3 group-hover:text-white transition-colors`} style={{ fontFamily: 'var(--font-outfit)' }}>
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed group-hover:text-gray-300 transition-colors" style={{ fontFamily: 'var(--font-inter)' }}>
                    {feature.description}
                  </p>
                </div>

                {/* Bottom stat badge */}
                <div className="mt-6 pt-6 border-t border-slate-700/50">
                  <span className="inline-block text-xs font-semibold text-gray-400 group-hover:text-cyan-300 transition-colors" style={{ fontFamily: 'var(--font-outfit)' }}>
                    {feature.stats}
                  </span>
                </div>
              </div>

              {/* Animated border glow on hover */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                <div className="absolute top-0 left-1/2 w-1/3 h-px bg-linear-to-r from-transparent via-cyan-400 to-transparent transform -translate-x-1/2"></div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
