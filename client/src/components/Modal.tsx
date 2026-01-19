'use client';

import { ReactNode } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
}

export default function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal Content */}
      <div className="relative z-10 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        <div className="bg-slate-900 rounded-2xl border border-cyan-500/30 shadow-2xl shadow-cyan-500/20">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-cyan-500/20">
            {title && (
              <h2 className="text-2xl font-bold text-white" style={{ fontFamily: 'var(--font-sora)' }}>
                {title}
              </h2>
            )}
            <button
              onClick={onClose}
              className="ml-auto text-gray-400 hover:text-white transition duration-200 text-2xl font-bold"
            >
              ✕
            </button>
          </div>

          {/* Content */}
          <div className="p-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
