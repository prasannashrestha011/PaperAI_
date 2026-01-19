'use client';

import { useEffect } from 'react';
import { useUserStore } from '@/store/userStore';

export default function AuthInitializer() {
  const { fetchUser, isAuthenticated } = useUserStore();

  useEffect(() => {
    // Fetch user data on component mount/refresh
    // This will populate the userStore with fresh data from /auth/me
    const initializeUser = async () => {
      await fetchUser();
    };

    initializeUser();
  }, []); // Empty dependency array means this runs once on mount

  return null; // This component doesn't render anything
}
