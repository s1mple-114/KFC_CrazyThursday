import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api/auth/users': {
        target: 'https://wkpgptfg-8000.asse.devtunnels.ms',
        changeOrigin: true
      }
    }
  }
});