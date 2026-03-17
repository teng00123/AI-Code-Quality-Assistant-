import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'cqa_settings'

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const useSettingsStore = defineStore('settings', () => {
  const saved = loadFromStorage()

  // 通用设置
  const language = ref(saved?.language ?? 'zh-CN')
  const theme = ref(saved?.theme ?? 'dark')
  const refreshInterval = ref(saved?.refreshInterval ?? 60)

  // API 设置
  const apiBaseURL = ref(saved?.apiBaseURL ?? 'localhost:8000')
  const apiTimeout = ref(saved?.apiTimeout ?? 10000)
  const httpsEnabled = ref(saved?.httpsEnabled ?? false)

  // 通知设置
  const notifAnalysisComplete = ref(saved?.notifAnalysisComplete ?? true)
  const notifNewIssues = ref(saved?.notifNewIssues ?? true)
  const notifQualityDrop = ref(saved?.notifQualityDrop ?? true)

  // 持久化到 localStorage
  function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      language: language.value,
      theme: theme.value,
      refreshInterval: refreshInterval.value,
      apiBaseURL: apiBaseURL.value,
      apiTimeout: apiTimeout.value,
      httpsEnabled: httpsEnabled.value,
      notifAnalysisComplete: notifAnalysisComplete.value,
      notifNewIssues: notifNewIssues.value,
      notifQualityDrop: notifQualityDrop.value,
    }))
  }

  // 主题应用：写入 CSS 变量到 :root
  function applyTheme(t) {
    const themes = {
      dark:  { '--bg-deep': '#030712', '--bg-card': 'rgba(255,255,255,0.03)', '--cyan': '#00f5ff', '--purple': '#7b2ff7' },
      cyber: { '--bg-deep': '#050515', '--bg-card': 'rgba(255,255,255,0.04)', '--cyan': '#00e5ff', '--purple': '#9b00ff' },
      auto:  { '--bg-deep': '#0d1117', '--bg-card': 'rgba(255,255,255,0.03)', '--cyan': '#58a6ff', '--purple': '#bc8cff' },
    }
    const vars = themes[t] || themes.dark
    const root = document.documentElement
    Object.entries(vars).forEach(([k, v]) => root.style.setProperty(k, v))
  }

  // 语言应用：设置 html lang 属性（可扩展 i18n）
  function applyLanguage(l) {
    document.documentElement.lang = l
  }

  // watch 实时生效
  watch(theme, (t) => { applyTheme(t); persist() }, { immediate: true })
  watch(language, (l) => { applyLanguage(l); persist() }, { immediate: true })
  watch([refreshInterval, apiBaseURL, apiTimeout, httpsEnabled,
         notifAnalysisComplete, notifNewIssues, notifQualityDrop], persist)

  function reset() {
    language.value = 'zh-CN'
    theme.value = 'dark'
    refreshInterval.value = 60
    apiBaseURL.value = 'localhost:8000'
    apiTimeout.value = 10000
    httpsEnabled.value = false
    notifAnalysisComplete.value = true
    notifNewIssues.value = true
    notifQualityDrop.value = true
  }

  return {
    language, theme, refreshInterval,
    apiBaseURL, apiTimeout, httpsEnabled,
    notifAnalysisComplete, notifNewIssues, notifQualityDrop,
    persist, reset, applyTheme, applyLanguage,
  }
})
