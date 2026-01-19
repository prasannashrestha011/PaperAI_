'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/authService';

export default function RegisterForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await authService.register(username, password);
      if (response && response.id && response.username) {
        router.push('/home');
      } else {
        setError('Registration failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

      {/* Grid background */}
      <div className="absolute inset-0 pointer-events-none opacity-5" style={{
        backgroundImage: `
          linear-gradient(rgba(34, 211, 238, 0.5) 1px, transparent 1px),
          linear-gradient(90deg, rgba(34, 211, 238, 0.5) 1px, transparent 1px)
        `,
        backgroundSize: '60px 60px'
      }}></div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300 mb-2" style={{ fontFamily: 'var(--font-sora)' }}>
            PaperAI
          </h1>
          <h2 className="mt-4 text-2xl font-bold text-white" style={{ fontFamily: 'var(--font-outfit)' }}>
            Create Account
          </h2>
          <p className="mt-2 text-gray-400" style={{ fontFamily: 'var(--font-inter)' }}>
            Start analyzing documents with AI
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="rounded-xl bg-red-500/10 border border-red-500/30 p-4">
            <p className="text-sm font-medium text-red-300" style={{ fontFamily: 'var(--font-inter)' }}>
              {error}
            </p>
          </div>
        )}

        {/* Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            {/* Username Input */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2" style={{ fontFamily: 'var(--font-inter)' }}>
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-cyan-500/20 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all duration-200 backdrop-blur-sm"
                style={{ fontFamily: 'var(--font-inter)' }}
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2" style={{ fontFamily: 'var(--font-inter)' }}>
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-cyan-500/20 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all duration-200 backdrop-blur-sm"
                style={{ fontFamily: 'var(--font-inter)' }}
                placeholder="Minimum 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Confirm Password Input */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2" style={{ fontFamily: 'var(--font-inter)' }}>
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                className="w-full px-4 py-3 rounded-lg bg-slate-800/50 border border-cyan-500/20 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all duration-200 backdrop-blur-sm"
                style={{ fontFamily: 'var(--font-inter)' }}
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 rounded-lg bg-gradient-to-r from-blue-500 to-cyan-400 text-slate-950 font-bold shadow-lg hover:shadow-cyan-500/50 transition-all duration-200 hover:scale-105 transform disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ fontFamily: 'var(--font-sora)' }}
          >
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        {/* Sign In Link */}
        <div className="text-center">
          <p className="text-gray-400" style={{ fontFamily: 'var(--font-inter)' }}>
            Already have an account?{' '}
            <a href="/login" className="font-semibold text-cyan-300 hover:text-cyan-200 transition-colors">
              Sign In
            </a>
          </p>
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
      `}</style>
    </div>
  );
}
