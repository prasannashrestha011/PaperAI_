'use client';

interface Stat {
  id: number;
  label: string;
  value: string;
  icon: string;
  gradient: string;
  accentColor: string;
}

const stats: Stat[] = [
  {
    id: 1,
    label: 'Documents',
    value: '12',
    icon: '📄',
    gradient: 'from-blue-500/20 to-cyan-500/20',
    accentColor: 'text-blue-300'
  },
  {
    id: 2,
    label: 'Questions Asked',
    value: '247',
    icon: '💬',
    gradient: 'from-cyan-500/20 to-indigo-500/20',
    accentColor: 'text-cyan-300'
  },
  {
    id: 3,
    label: 'Searches',
    value: '589',
    icon: '🔍',
    gradient: 'from-indigo-500/20 to-purple-500/20',
    accentColor: 'text-indigo-300'
  },
  {
    id: 4,
    label: 'Storage Used',
    value: '45.2 MB',
    icon: '💾',
    gradient: 'from-purple-500/20 to-pink-500/20',
    accentColor: 'text-purple-300'
  },
];

export default function HomeStats() {
  return (
    <section className="relative w-full py-16 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-4" style={{ fontFamily: 'var(--font-sora)' }}>
            Your Activity
          </h2>
          <p className="text-gray-400 text-lg" style={{ fontFamily: 'var(--font-inter)' }}>
            Track your usage and analytics
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => (
            <div
              key={stat.id}
              className={`relative group p-8 rounded-2xl ${stat.gradient} backdrop-blur-sm border border-cyan-500/20 hover:border-cyan-400/60 transition duration-300 overflow-hidden`}
            >
              {/* Animated Border */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 group-hover:animate-pulse"></div>

              {/* Content */}
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-gray-400 text-sm font-medium mb-2" style={{ fontFamily: 'var(--font-inter)' }}>
                      {stat.label}
                    </p>
                    <p className={`text-5xl font-black ${stat.accentColor}`} style={{ fontFamily: 'var(--font-sora)' }}>
                      {stat.value}
                    </p>
                  </div>
                  <div className="text-4xl">{stat.icon}</div>
                </div>

                {/* Progress Indicator */}
                <div className="mt-6 h-1 bg-gray-700 rounded-full overflow-hidden">
                  <div className={`h-full bg-gradient-to-r ${stat.gradient} w-3/4 rounded-full`}></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer Stats Note */}
        <div className="mt-12 text-center">
          <p className="text-gray-400" style={{ fontFamily: 'var(--font-inter)' }}>
            Updated in real-time • <span className="text-cyan-300">Last updated: Just now</span>
          </p>
        </div>
      </div>
    </section>
  );
}
