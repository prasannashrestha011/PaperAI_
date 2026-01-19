'use client';

import { useState, useRef, useCallback } from 'react';

interface FileValidationError {
  type: 'size' | 'format' | 'unknown';
  message: string;
}

interface DocumentUploadProps {
  onFileSelected?: (file: File) => void;
  onError?: (error: FileValidationError) => void;
  onUpload?: (file: File) => Promise<void>;
}

const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50 MB
const ACCEPTED_TYPES = ['application/pdf'];
const ACCEPTED_EXTENSIONS = ['.pdf'];

export default function DocumentUpload({ onFileSelected, onError, onUpload }: DocumentUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<FileValidationError | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Validate file
  const validateFile = useCallback((file: File): FileValidationError | null => {
    // Check file type
    if (!ACCEPTED_TYPES.includes(file.type)) {
      const hasValidExtension = ACCEPTED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext));
      if (!hasValidExtension) {
        const error: FileValidationError = {
          type: 'format',
          message: 'Only PDF and DOC files are allowed',
        };
        return error;
      }
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      const error: FileValidationError = {
        type: 'size',
        message: `File size exceeds 50 MB limit. Your file is ${(file.size / (1024 * 1024)).toFixed(2)} MB`,
      };
      return error;
    }

    return null;
  }, []);

  const handleFileSelect = useCallback((file: File) => {
    const error = validateFile(file);

    if (error) {
      setValidationError(error);
      setSelectedFile(null);
      onError?.(error);
    } else {
      setValidationError(null);
      setSelectedFile(file);
      // Don't call onFileSelected immediately - wait for upload button click
    }
  }, [validateFile, onError]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleClear = () => {
    setSelectedFile(null);
    setValidationError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsLoading(true);

    try {
      if (onUpload) {
        await onUpload(selectedFile);
        // Call onFileSelected after successful upload
        onFileSelected?.(selectedFile);
        // Clear after success
        setTimeout(() => {
          handleClear();
        }, 500);
      }
    } catch (error) {
      console.error('Upload error:', error);
      onError?.({
        type: 'unknown',
        message: 'Failed to upload file. Please try again.',
      });
      setIsLoading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const getFileIcon = (fileName: string): string => {
    if (fileName.toLowerCase().endsWith('.pdf')) return '📄';
    if (fileName.toLowerCase().endsWith('.doc') || fileName.toLowerCase().endsWith('.docx')) return '📝';
    return '📎';
  };

  return (
    <div className="w-full">
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={handleInputChange}
        className="hidden"
      />

      {!selectedFile ? (
        // Upload Area
        <div
          onClick={handleClick}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`relative p-8 rounded-2xl border-2 border-dashed cursor-pointer transition-all duration-300 ${
            isDragging
              ? 'border-cyan-400 bg-cyan-500/10 shadow-lg shadow-cyan-500/20'
              : 'border-cyan-500/30 bg-gradient-to-br from-slate-800/40 to-slate-900/40 hover:border-cyan-400/60 hover:bg-cyan-500/5'
          }`}
        >
          {/* Animated background on drag */}
          <div className={`absolute inset-0 rounded-2xl transition-opacity duration-300 pointer-events-none ${
            isDragging ? 'bg-gradient-to-r from-transparent via-cyan-500/10 to-transparent opacity-100' : 'opacity-0'
          }`}></div>

          {/* Content */}
          <div className="relative z-10 flex flex-col items-center justify-center">
            <div className="text-5xl mb-4">📁</div>
            <h3 className="text-xl font-bold text-white mb-2" style={{ fontFamily: 'var(--font-sora)' }}>
              {isDragging ? 'Drop your file here' : 'Drag and drop your document'}
            </h3>
            <p className="text-gray-400 mb-4 text-center" style={{ fontFamily: 'var(--font-inter)' }}>
              or click to browse your files
            </p>
            <div className="flex gap-2">
              <span className="px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-blue-300 text-sm font-semibold">
                PDF
              </span>
            <span className="px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-sm font-semibold">
                Max 50MB
              </span>
            </div>
          </div>
        </div>
      ) : (
        // Selected File Display
        <div className="space-y-4">
          <div className="p-6 rounded-2xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/30">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <div className="text-4xl mt-1">{getFileIcon(selectedFile.name)}</div>
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-white break-all" style={{ fontFamily: 'var(--font-sora)' }}>
                    {selectedFile.name}
                  </h3>
                  <div className="flex gap-4 mt-2 text-sm text-gray-400">
                    <span>📦 {formatFileSize(selectedFile.size)}</span>
                    <span className={isLoading ? 'text-yellow-300 font-semibold' : 'text-green-300 font-semibold'}>
                      {isLoading ? '⏳ Uploading...' : '✓ Ready to upload'}
                    </span>
                  </div>
                </div>
              </div>
              <button
                onClick={handleClear}
                disabled={isLoading}
                className="px-4 py-2 text-sm font-medium text-red-300 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Clear
              </button>
            </div>
          </div>

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={isLoading}
            className="w-full py-3 px-4 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white font-bold shadow-lg hover:shadow-cyan-500/50 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '⏳ Uploading...' : 'Upload Document'}
          </button>
        </div>
      )}

      {/* Error Message */}
      {validationError && (
        <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <h4 className="text-sm font-semibold text-red-300 mb-1">
                {validationError.type === 'size' ? 'File Too Large' : 'Invalid File Type'}
              </h4>
              <p className="text-sm text-red-200" style={{ fontFamily: 'var(--font-inter)' }}>
                {validationError.message}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Validation Info */}
      <div className="mt-4 p-4 rounded-lg bg-blue-500/5 border border-blue-500/20">
        <p className="text-xs text-blue-300" style={{ fontFamily: 'var(--font-inter)' }}>
          <strong>Supported formats:</strong> PDF • <strong>Maximum size:</strong> 50 MB
        </p>
      </div>
    </div>
  );
}
