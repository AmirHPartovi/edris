/// <reference types="vite/client" />

/* src/api.ts */
import axios from 'axios';

export const API_BASE_URL = `${import.meta.env.VITE_SERVER_URL || 'http://localhost:8000'}`

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 30000,
});

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ModelSettings {
  temperature: number;
  top_p: number;
  max_tokens: number;
}

export interface ChatParams {
  prompt: string;
  type: 'text' | 'image';
  model?: string;
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  frequency_penalty?: number;
  presence_penalty?: number;
  stop?: string[];
  stream?: boolean;
  history?: Message[];
  modes?: string[];
  modelSettings?: ModelSettings;
  knowledgeStacks?: string[];
}

export const sendMessage = async (params: ChatParams): Promise<{ response: string }> => {
  try {
    const response = await api.post('/query', params);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to send message');
  }
};

export const uploadKnowledgeFiles = async (stackId: string, files: File[]): Promise<void> => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  formData.append('stackId', stackId);
  
  try {
    await api.post('/knowledge/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  } catch (error) {
    console.error('Upload Error:', error);
    throw new Error('Failed to upload files');
  }
};