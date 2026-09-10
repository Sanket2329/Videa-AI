import { apiClient, unwrapResponse } from './client';
import { User, Token, UserCreate, UserLogin } from '../types/auth';

export const authApi = {
  login: async (data: UserLogin): Promise<Token> => {
    // OAuth2PasswordRequestForm expects form-urlencoded
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);
    
    const response = await apiClient.post<Token>('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },

  register: async (data: UserCreate): Promise<User> => {
    return unwrapResponse(apiClient.post('/auth/register', data));
  },

  getMe: async (): Promise<User> => {
    return unwrapResponse(apiClient.get('/auth/me'));
  },
};
