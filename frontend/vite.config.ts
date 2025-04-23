import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dotenv from 'dotenv';

// Load environment variables from .env
dotenv.config();

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    cors: true
  },
  define: {
    'process.env': process.env
  }
});