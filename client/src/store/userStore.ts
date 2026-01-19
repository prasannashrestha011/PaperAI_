import { create } from 'zustand';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

interface User {
  user_id: string;
  username: string;
  created_at: string;
}

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  fetchUser: () => Promise<void>;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  fetchUser: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        withCredentials: true,
      });

      if (response.data) {
        set({
          user: response.data,
          isAuthenticated: true,
          isLoading: false,
        });
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch user';
      set({
        user: null,
        isAuthenticated: false,
        error: errorMessage,
        isLoading: false,
      });
    }
  },

  setUser: (user: User) => {
    set({
      user,
      isAuthenticated: true,
      error: null,
    });
  },

  clearUser: () => {
    set({
      user: null,
      isAuthenticated: false,
      error: null,
    });
  },
}));
