import axios from 'axios';

import { ApiResponse } from '../types/api';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Standardize error format for UI consumption
    if (error.response?.data?.error) {
      return Promise.reject(error.response.data.error);
    }
    return Promise.reject({
      code: 'NETWORK_ERROR',
      message: 'Unable to connect to the server. Please try again later.',
    });
  }
);

/** Helper to extract data from the ApiResponse wrapper */
export async function unwrapResponse<T>(request: Promise<{ data: ApiResponse<T> }>): Promise<T> {
  const response = await request;
  if (!response.data.success || !response.data.data) {
    throw response.data.error || new Error('Unknown error occurred');
  }
  return response.data.data;
}
