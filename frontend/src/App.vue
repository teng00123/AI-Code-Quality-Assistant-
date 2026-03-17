<template>
  <div id="app">
    <!-- Three.js 3D 背景画布 -->
    <canvas ref="bgCanvas" class="bg-canvas"></canvas>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polygon points="20,2 38,12 38,28 20,38 2,28 2,12" fill="none" stroke="url(#grad1)" stroke-width="2"/>
            <polygon points="20,8 32,15 32,25 20,32 8,25 8,15" fill="url(#grad2)" opacity="0.3"/>
            <circle cx="20" cy="20" r="5" fill="url(#grad1)"/>
            <defs>
              <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00f5ff"/>
                <stop offset="100%" style="stop-color:#7b2ff7"/>
              </linearGradient>
              <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00f5ff"/>
                <stop offset="100%" style="stop-color:#7b2ff7"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="logo-text">CodeAI</span>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
          <span class="nav-glow"></span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="status-dot"></div>
        <span class="status-text">{{ t.nav.online }}</span>
      </div>

      <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline v-if="!sidebarCollapsed" points="15,18 9,12 15,6"/>
          <polyline v-else points="9,18 15,12 9,6"/>
        </svg>
      </button>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <!-- 顶部栏 -->
      <header class="topbar">
        <div class="topbar-left">
          <div class="breadcrumb">
            <span class="breadcrumb-home">{{ t.topbar.brand }}</span>
            <span class="breadcrumb-sep">/</span>
            <span class="breadcrumb-current">{{ currentPageName }}</span>
          </div>
        </div>
        <div class="topbar-right">
          <div class="topbar-badge">
            <span class="pulse-dot"></span>
            <span>{{ t.topbar.realtime }}</span>
          </div>
          <div class="topbar-time">{{ currentTime }}</div>
        </div>
      </header>

      <!-- 页面内容 -->
      <div class="page-content">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import * as THREE from 'three'
import { useSettingsStore } from './store/settings.js'
import { useI18n } from './i18n/index.js'

const route = useRoute()
const bgCanvas = ref(null)
const sidebarCollapsed = ref(false)
const currentTime = ref('')

// 接入设置 store — 启动时自动应用主题/语言（store 内部 watch immediate）
useSettingsStore()
const { t } = useI18n()

const navItems = computed(() => [
  {
    path: '/dashboard',
    label: t.value.nav.dashboard,
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`
  },
  {
    path: '/analysis',
    label: t.value.nav.analysis,
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>`
  },
  {
    path: '/reports',
    label: t.value.nav.reports,
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10,9 9,9 8,9"/></svg>`
  },
  {
    path: '/settings',
    label: t.value.nav.settings,
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`
  }
])

const currentPageName = computed(() => {
  const map = {
    '/dashboard': t.value.nav.dashboard,
    '/analysis':  t.value.nav.analysis,
    '/reports':   t.value.nav.reports,
    '/settings':  t.value.nav.settings,
  }
  return map[route.path] || ''
})

// 时间更新
let timeInterval
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

// Three.js 粒子背景
let renderer, scene, camera, particles, animId

const initThree = () => {
  const canvas = bgCanvas.value
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 30

  // 粒子系统
  const count = 2000
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)

  const colorOptions = [
    new THREE.Color(0x00f5ff),
    new THREE.Color(0x7b2ff7),
    new THREE.Color(0x00ff88),
    new THREE.Color(0xff006e),
  ]

  for (let i = 0; i < count; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 100
    positions[i * 3 + 1] = (Math.random() - 0.5) * 100
    positions[i * 3 + 2] = (Math.random() - 0.5) * 60

    const c = colorOptions[Math.floor(Math.random() * colorOptions.length)]
    colors[i * 3] = c.r
    colors[i * 3 + 1] = c.g
    colors[i * 3 + 2] = c.b
  }

  const geo = new THREE.BufferGeometry()
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))

  const mat = new THREE.PointsMaterial({
    size: 0.15,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    sizeAttenuation: true
  })

  particles = new THREE.Points(geo, mat)
  scene.add(particles)

  // 连接线 — 构建网格感
  const lineMat = new THREE.LineBasicMaterial({
    color: 0x00f5ff,
    transparent: true,
    opacity: 0.06
  })
  const lineCount = 150
  for (let i = 0; i < lineCount; i++) {
    const lineGeo = new THREE.BufferGeometry()
    const p = new Float32Array(6)
    for (let j = 0; j < 6; j++) p[j] = (Math.random() - 0.5) * 100
    lineGeo.setAttribute('position', new THREE.BufferAttribute(p, 3))
    scene.add(new THREE.Line(lineGeo, lineMat))
  }

  const animate = () => {
    animId = requestAnimationFrame(animate)
    particles.rotation.x += 0.0003
    particles.rotation.y += 0.0005
    renderer.render(scene, camera)
  }
  animate()

  window.addEventListener('resize', onResize)
}

const onResize = () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}

onMounted(() => {
  initThree()
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  cancelAnimationFrame(animId)
  renderer?.dispose()
  window.removeEventListener('resize', onResize)
  clearInterval(timeInterval)
})
</script>

<style>
/* ===== 全局重置 ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --cyan: #00f5ff;
  --purple: #7b2ff7;
  --green: #00ff88;
  --pink: #ff006e;
  --bg-deep: #030712;
  --bg-card: rgba(255,255,255,0.03);
  --bg-card-hover: rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.08);
  --border-glow: rgba(0,245,255,0.3);
  --text-primary: #e2e8f0;
  --text-secondary: #64748b;
  --text-muted: #334155;
  --sidebar-w: 220px;
  --sidebar-w-collapsed: 68px;
  --topbar-h: 60px;
  --radius: 12px;
}

html, body { height: 100%; background: var(--bg-deep); color: var(--text-primary); font-family: 'Inter', sans-serif; overflow: hidden; }

/* 滚动条 */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.3); }

/* Element Plus 深色主题覆盖 */
.el-card { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; backdrop-filter: blur(20px); color: var(--text-primary) !important; }
.el-card__header { border-bottom: 1px solid var(--border) !important; color: var(--text-primary) !important; font-weight: 600; letter-spacing: 0.03em; }
.el-card__body { color: var(--text-primary) !important; }
.el-table { background: transparent !important; color: var(--text-primary) !important; }
.el-table tr, .el-table th, .el-table td { background: transparent !important; border-color: var(--border) !important; color: var(--text-primary) !important; }
.el-table--striped .el-table__body tr.el-table__row--striped td { background: rgba(255,255,255,0.02) !important; }
.el-table__header-wrapper th { color: var(--cyan) !important; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; }
.el-table__body tr:hover td { background: rgba(0,245,255,0.04) !important; }
.el-input__wrapper { background: rgba(255,255,255,0.04) !important; border-color: var(--border) !important; box-shadow: none !important; }
.el-input__wrapper:hover, .el-input__wrapper.is-focus { border-color: var(--cyan) !important; box-shadow: 0 0 0 1px var(--cyan) !important; }
.el-input__inner { color: var(--text-primary) !important; }
.el-button--primary { background: linear-gradient(135deg, var(--cyan), var(--purple)) !important; border: none !important; font-weight: 600; letter-spacing: 0.05em; }
.el-button--primary:hover { opacity: 0.85; transform: translateY(-1px); box-shadow: 0 8px 25px rgba(0,245,255,0.3) !important; }
.el-button--danger { background: linear-gradient(135deg, #ff006e, #7b2ff7) !important; border: none !important; }
.el-tabs__nav-wrap::after { background: var(--border) !important; }
.el-tabs__item { color: var(--text-secondary) !important; }
.el-tabs__item.is-active { color: var(--cyan) !important; }
.el-tabs__active-bar { background: var(--cyan) !important; }
.el-form-item__label { color: var(--text-secondary) !important; }
.el-select .el-input__wrapper { background: rgba(255,255,255,0.04) !important; }
.el-select-dropdown { background: #0f1929 !important; border-color: var(--border) !important; }
.el-select-dropdown__item { color: var(--text-primary) !important; }
.el-select-dropdown__item.hover, .el-select-dropdown__item:hover { background: rgba(0,245,255,0.08) !important; }
.el-radio__label { color: var(--text-primary) !important; }
.el-radio__inner { border-color: var(--border) !important; background: transparent !important; }
.el-radio__input.is-checked .el-radio__inner { border-color: var(--cyan) !important; background: var(--cyan) !important; }
.el-switch.is-checked .el-switch__core { background: var(--cyan) !important; border-color: var(--cyan) !important; }
.el-pagination { color: var(--text-secondary) !important; }
.el-pagination button, .el-pagination .el-pager li { background: transparent !important; color: var(--text-secondary) !important; border-color: var(--border) !important; }
.el-pagination .el-pager li.is-active { color: var(--cyan) !important; }
.el-progress-bar__outer { background: rgba(255,255,255,0.06) !important; }
.el-tag { border: 1px solid !important; }
.el-tag--success { background: rgba(0,255,136,0.1) !important; border-color: rgba(0,255,136,0.3) !important; color: #00ff88 !important; }
.el-tag--warning { background: rgba(255,170,0,0.1) !important; border-color: rgba(255,170,0,0.3) !important; color: #ffaa00 !important; }
.el-tag--danger { background: rgba(255,0,110,0.1) !important; border-color: rgba(255,0,110,0.3) !important; color: #ff006e !important; }
.el-tag--primary { background: rgba(0,245,255,0.1) !important; border-color: rgba(0,245,255,0.3) !important; color: var(--cyan) !important; }
.el-tag--info { background: rgba(100,116,139,0.1) !important; border-color: rgba(100,116,139,0.3) !important; color: #94a3b8 !important; }
.el-input-number .el-input__wrapper { background: rgba(255,255,255,0.04) !important; }
.el-upload-dragger { background: rgba(255,255,255,0.02) !important; border-color: var(--border) !important; }
.el-upload-dragger:hover { border-color: var(--cyan) !important; }
</style>

<style scoped>
#app {
  width: 100vw;
  height: 100vh;
  display: flex;
  overflow: hidden;
  position: relative;
}

/* ===== 3D 背景 ===== */
.bg-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: relative;
  z-index: 10;
  width: var(--sidebar-w);
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: rgba(3, 7, 18, 0.85);
  backdrop-filter: blur(30px);
  border-right: 1px solid var(--border);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  overflow: hidden;
}
.sidebar.collapsed { width: var(--sidebar-w-collapsed); }

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  border-bottom: 1px solid var(--border);
}
.logo-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  filter: drop-shadow(0 0 8px rgba(0,245,255,0.5));
}
.logo-icon svg { width: 100%; height: 100%; }
.logo-text {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--cyan), var(--purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  white-space: nowrap;
  letter-spacing: 0.05em;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  overflow: hidden;
  white-space: nowrap;
}
.nav-item:hover {
  color: var(--text-primary);
  background: rgba(255,255,255,0.04);
}
.nav-item.active {
  color: var(--cyan);
  background: rgba(0,245,255,0.08);
  border: 1px solid rgba(0,245,255,0.15);
}
.nav-item.active .nav-glow {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--cyan);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 10px var(--cyan);
}
.nav-icon { width: 20px; height: 20px; flex-shrink: 0; }
.nav-icon :deep(svg) { width: 100%; height: 100%; }
.nav-label { font-size: 14px; font-weight: 500; }

.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--border);
}
.status-dot {
  width: 8px; height: 8px;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--green);
  animation: pulse-dot 2s infinite;
  flex-shrink: 0;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px var(--green); }
  50% { opacity: 0.6; box-shadow: 0 0 16px var(--green); }
}
.status-text { font-size: 12px; color: var(--green); white-space: nowrap; }

.collapse-btn {
  position: absolute;
  bottom: 60px;
  right: -12px;
  width: 24px;
  height: 24px;
  background: var(--bg-deep);
  border: 1px solid var(--border);
  border-radius: 50%;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 1;
}
.collapse-btn:hover { border-color: var(--cyan); color: var(--cyan); }
.collapse-btn svg { width: 12px; height: 12px; }

/* ===== 主内容 ===== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  position: relative;
  z-index: 5;
  transition: all 0.3s ease;
}

/* ===== 顶栏 ===== */
.topbar {
  height: var(--topbar-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(3, 7, 18, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.breadcrumb { display: flex; align-items: center; gap: 8px; font-size: 14px; }
.breadcrumb-home { color: var(--text-muted); }
.breadcrumb-sep { color: var(--text-muted); }
.breadcrumb-current { color: var(--text-primary); font-weight: 500; }
.topbar-right { display: flex; align-items: center; gap: 20px; }
.topbar-badge {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: var(--cyan);
  background: rgba(0,245,255,0.08);
  border: 1px solid rgba(0,245,255,0.2);
  padding: 4px 10px; border-radius: 20px;
}
.pulse-dot {
  width: 6px; height: 6px; background: var(--cyan);
  border-radius: 50%; animation: pulse-dot 1.5s infinite;
  box-shadow: 0 0 6px var(--cyan);
}
.topbar-time {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--text-secondary);
  letter-spacing: 0.05em;
}

/* ===== 页面内容 ===== */
.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* ===== 页面切换动画 ===== */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.25s ease;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
