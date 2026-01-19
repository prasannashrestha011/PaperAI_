'use client';

import { useRouter } from 'next/navigation';

interface Document {
  id: number;
  name: string;
  uploadDate: string;
  size: string;
  type: string;
  icon: string;
}

const recentDocuments: Document[] = [
  {
    id: 1,
    name: 'Machine Learning Basics.pdf',
    uploadDate: '2 days ago',
    size: '4.2 MB',
    type: 'PDF',
    icon: '📄'
  },
  {
    id: 2,
    name: 'Research Paper 2024.pdf',
    uploadDate: '1 week ago',
    size: '8.5 MB',
    type: 'PDF',
    icon: '📄'
  },
  {
    id: 3,
    name: 'Technical Documentation.pdf',
    uploadDate: '2 weeks ago',
    size: '2.1 MB',
    type: 'PDF',
    icon: '📄'
  },
  {
    id: 4,
    name: 'Annual Report 2024.pdf',
    uploadDate: '3 weeks ago',
    size: '5.8 MB',
    type: 'PDF',
    icon: '📄'
  },
];

export default function RecentDocuments() {
  const router = useRouter();

  const handleDocumentClick = (docId: number) => {
    router.push(`/foo?doc=${docId}`);
  };

  const handleUploadNew = () => {
    router.push('/new');
  };

  return (
    <section className="relative w-full py-16 px-4 md:px-8 bg-gradient-to-b from-transparent via-blue-500/5 to-transparent">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="flex justify-between items-center mb-12">
          <div>
            <h2 className="text-4xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-sora)' }}>
              Recent Documents
            </h2>
            <p className="text-gray-400 text-lg" style={{ fontFamily: 'var(--font-inter)' }}>
              Access your recently uploaded documents
            </p>
          </div>
          <button
            onClick={handleUploadNew}
            className="hidden sm:block px-6 py-2 text-sm font-semibold text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 rounded-lg transition duration-200 transform hover:scale-105 shadow-lg"
          >
            + Upload New
          </button>
        </div>

        {/* Documents Grid */}
        {recentDocuments.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {recentDocuments.map((doc) => (
              <button
                key={doc.id}
                onClick={() => handleDocumentClick(doc.id)}
                className="group relative p-6 rounded-xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 backdrop-blur-sm border border-cyan-500/20 hover:border-cyan-400/60 transition duration-300 overflow-hidden text-left hover:shadow-lg hover:shadow-cyan-500/20 transform hover:scale-105"
              >
                {/* Hover Gradient */}
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/5 to-cyan-500/0 opacity-0 group-hover:opacity-100 transition duration-300"></div>

                {/* Content */}
                <div className="relative z-10">
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-4xl">{doc.icon}</div>
                    <span className="px-2 py-1 text-xs font-semibold text-cyan-300 bg-cyan-500/20 rounded-full">
                      {doc.type}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white mb-3 line-clamp-2 group-hover:text-cyan-300 transition" style={{ fontFamily: 'var(--font-sora)' }}>
                    {doc.name}
                  </h3>

                  <div className="flex items-center justify-between text-sm text-gray-400">
                    <span>{doc.size}</span>
                    <span>{doc.uploadDate}</span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-16 px-8 rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-slate-900/40 to-slate-800/40 backdrop-blur-sm">
            <div className="text-6xl mb-4">📁</div>
            <h3 className="text-2xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-sora)' }}>
              No Documents Yet
            </h3>
            <p className="text-gray-400 mb-6" style={{ fontFamily: 'var(--font-inter)' }}>
              Upload your first document to get started
            </p>
            <button
              onClick={handleUploadNew}
              className="px-6 py-2 text-sm font-semibold text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 rounded-lg transition duration-200 transform hover:scale-105 shadow-lg"
            >
              Upload Document
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
