'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/authService';
import { useUserStore } from '@/store/userStore';

export default function HomeHeader() {
  const router = useRouter();
  const { user, clearUser } = useUserStore();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      // Call logout API to clear server-side session/cookie
      await authService.logout();
      // Clear client-side user store
      clearUser();
      // Refresh to trigger middleware check
      router.refresh();
      // Redirect to login
      setTimeout(() => {
        router.push('/login');
      }, 100);
    } catch (error) {
      console.error('Logout failed:', error);
      // Still redirect even if logout fails
      clearUser();
      router.refresh();
      setTimeout(() => {
        router.push('/login');
      }, 100);
    } finally {
      setIsLoggingOut(false);
    }
  };

  return (
    <nav className="fixed top-0 w-full bg-slate-950/95 backdrop-blur-md border-b border-cyan-500/20 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300" style={{ fontFamily: 'var(--font-sora)' }}>
            PaperAI
          </div>
        </div>

        {/* Right Side - User Info & Actions */}
        <div className="flex items-center gap-4">
          <div className="hidden sm:block text-right">
            <p className="text-sm text-gray-400">Welcome back,</p>
            <p className="text-md font-semibold text-white">{user?.username}</p>
          </div>
          <button
            onClick={handleLogout}
            disabled={isLoggingOut}
            className="px-4 py-2 text-sm font-medium text-slate-950 bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 rounded-lg transition duration-200 transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoggingOut ? 'Logging Out...' : 'Logout'}
          </button>
        </div>
      </div>
    </nav>
  );
}
