/// <reference types="vite/client" />

/* src/api.ts */
import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_SERVER_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 30000, // 30 seconds
});

export interface ChatParams {
  prompt: string;
  type: 'text' | 'image';
  temperature: number;
  max_tokens: number;
  stop: string[];
}

export const sendMessage = async (params: ChatParams): Promise<string> => {
  try {
    const resp = await api.post('/query', params);
    return resp.data.response;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to send message');
  }
};