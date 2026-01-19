'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Modal from '@/components/Modal';
import DocumentUpload from '@/components/DocumentUpload';

interface QuickAction {
  id: number;
  title: string;
  description: string;
  icon: string;
  href?: string;
  gradient: string;
  borderColor: string;
  hoverBorderColor: string;
  accentColor: string;
}

const actions: QuickAction[] = [
  {
    id: 1,
    title: 'Upload Document',
    description: 'Upload a new PDF or document',
    icon: '📤',
    gradient: 'from-blue-500/20 to-cyan-500/20',
    borderColor: 'border-blue-500/30',
    hoverBorderColor: 'hover:border-blue-400/60',
    accentColor: 'text-blue-300'
  },
  {
    id: 2,
    title: 'Search Documents',
    description: 'Find information across your docs',
    icon: '🔍',
    href: '/new',
    gradient: 'from-cyan-500/20 to-indigo-500/20',
    borderColor: 'border-cyan-500/30',
    hoverBorderColor: 'hover:border-cyan-400/60',
    accentColor: 'text-cyan-300'
  },
  {
    id: 3,
    title: 'Ask Questions',
    description: 'Get AI-powered answers with citations',
    icon: '🤖',
    href: '/new',
    gradient: 'from-indigo-500/20 to-purple-500/20',
    borderColor: 'border-indigo-500/30',
    hoverBorderColor: 'hover:border-indigo-400/60',
    accentColor: 'text-indigo-300'
  },
];

export default function QuickActions() {
  const router = useRouter();
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

  const handleAction = (action: QuickAction) => {
    if (action.id === 1) {
      // Upload Document
      setIsUploadModalOpen(true);
    } else if (action.href) {
      router.push(action.href);
    }
  };

  const handleFileSelected = (file: File) => {
    console.log('File successfully uploaded:', file);
    // Close modal after successful upload
    setTimeout(() => {
      setIsUploadModalOpen(false);
    }, 500);
  };

  const handleUploadError = (error: any) => {
    console.error('Upload error:', error);
  };

  const handleUpload = async (file: File) => {
    // TODO: Implement actual file upload to backend API
    // Example:
    // const formData = new FormData();
    // formData.append('file', file);
    // const response = await axios.post('/api/documents/upload', formData);
    // return response.data;

    // For now, simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        console.log('File uploaded to backend:', file);
        resolve(undefined);
      }, 2000);
    });
  };

  return (
    <section className="relative w-full py-16 px-4 md:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div className="mb-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-4" style={{ fontFamily: 'var(--font-sora)' }}>
            Quick Actions
          </h2>
          <p className="text-gray-400 text-lg" style={{ fontFamily: 'var(--font-inter)' }}>
            Get started with your documents in a few clicks
          </p>
        </div>

        {/* Actions Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {actions.map((action) => (
            <button
              key={action.id}
              onClick={() => handleAction(action)}
              className={`relative group p-8 rounded-2xl ${action.gradient} backdrop-blur-sm border ${action.borderColor} ${action.hoverBorderColor} transition duration-300 text-left overflow-hidden cursor-pointer hover:shadow-lg hover:shadow-blue-500/20 transform hover:scale-105`}
            >
              {/* Animated Border */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-0 group-hover:opacity-10 group-hover:animate-pulse"></div>

              {/* Content */}
              <div className="relative z-10">
                <div className="text-5xl mb-4">{action.icon}</div>
                <h3 className={`text-2xl font-bold ${action.accentColor} mb-2`} style={{ fontFamily: 'var(--font-sora)' }}>
                  {action.title}
                </h3>
                <p className="text-gray-400" style={{ fontFamily: 'var(--font-inter)' }}>
                  {action.description}
                </p>
              </div>

              {/* Arrow Icon on Hover */}
              <div className="absolute top-6 right-6 text-2xl transform group-hover:translate-x-2 transition duration-300">
                →
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Upload Modal */}
      <Modal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        title="Upload Document"
      >
        <DocumentUpload
          onFileSelected={handleFileSelected}
          onError={handleUploadError}
          onUpload={handleUpload}
        />
      </Modal>
    </section>
  );
}
