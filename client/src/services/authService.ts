import axios from 'axios';
import { AuthRequest, AuthResponse } from '@/lib/types';

const API_BASE_URL = 'http://localhost:8000';

export const authService = {
    async login(username: string, password: string): Promise<AuthResponse> {
        const payload: AuthRequest = { username, password };
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/login`, payload, {
                headers: { 'Content-Type': 'application/json' }, withCredentials: true,
            });
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.message || 'Login failed'
            );
        }
    },

    async register(username: string, password: string): Promise<any> {
        const payload: AuthRequest = { username, password };
        try {
            const response = await axios.post(`${API_BASE_URL}/auth/register`, payload, {
                headers: { 'Content-Type': 'application/json' },
            });
            return response.data;
        } catch (error: any) {
            throw new Error(
                error.response?.data?.message || 'Registration failed'
            );
        }
    },

    async logout(): Promise<void> {
        try {
            await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
                withCredentials: true,
            });
        } catch (error: any) {
            console.error('Logout error:', error);
            // Still consider logout successful even if API call fails
            // Cookie will be cleared by backend
        }
    },

    // Token is now managed via HTTP-only cookie (access_token). No client-side storage needed.
};

