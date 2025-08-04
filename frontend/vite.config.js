import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { readFileSync } from 'fs'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// 强制使用HTTPS
const forceHTTPS = true

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      imports: ['vue', 'vue-router', 'pinia'],
      dts: true
    }),
    Components({
      resolvers: [ElementPlusResolver({
        importStyle: false
      })],
      dts: true
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
    https: {
      key: readFileSync(resolve(__dirname, '../ssl/key.pem')),
      cert: readFileSync(resolve(__dirname, '../ssl/cert.pem')),
      // SSL兼容性选项
      secureProtocol: 'TLSv1_2_method',
      ciphers: 'HIGH:!aNULL:!MD5',
      honorCipherOrder: true
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 开发环境使用HTTP连接Django
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // 开发环境设置正确的协议头
            proxyReq.setHeader('X-Forwarded-Proto', 'http')
          })
        }
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    rollupOptions: {
      output: {
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    }
  }
})
