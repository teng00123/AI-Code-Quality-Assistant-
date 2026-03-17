import { useSettingsStore } from '../store/settings.js'

function getBaseURL() {
  const store = useSettingsStore()
  const protocol = store.httpsEnabled ? 'https' : 'http'
  return `${protocol}://${store.apiBaseURL}`
}

async function request(path, options = {}) {
  const store = useSettingsStore()
  const url = `${getBaseURL()}${path}`
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), store.apiTimeout || 10000)
  try {
    const res = await fetch(url, { signal: controller.signal, ...options })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }
    return await res.json()
  } finally {
    clearTimeout(timer)
  }
}

// ── Reports ──────────────────────────────────────────────
export const reportsApi = {
  /** 获取分析记录列表 */
  list(limit = 50) {
    return request(`/api/v1/analysis/?limit=${limit}`)
  },

  /** 获取单条分析详情 */
  get(analysisId) {
    return request(`/api/v1/analysis/${analysisId}`)
  },

  /** 删除单条分析记录 */
  delete(analysisId) {
    return request(`/api/v1/analysis/${analysisId}`, { method: 'DELETE' })
  },

  /** 导出报告（触发浏览器下载 JSON） */
  export(report) {
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = `report-${report.analysis_id ?? report.filename ?? 'export'}.json`
    a.click()
    URL.revokeObjectURL(url)
  },

  /** 导出全部报告 */
  exportAll(reports) {
    const blob = new Blob([JSON.stringify(reports, null, 2)], { type: 'application/json' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = `reports-${new Date().toISOString().slice(0,10)}.json`
    a.click()
    URL.revokeObjectURL(url)
  }
}

// ── Analysis ─────────────────────────────────────────────
export const analysisApi = {
  /** 按路径分析 */
  analyzeByPath(filePath, language = null) {
    const params = new URLSearchParams({ file_path: filePath })
    if (language) params.set('language', language)
    return request(`/api/v1/analysis/file?${params}`, { method: 'POST' })
  },

  /** 上传文件分析 */
  analyzeUpload(file) {
    const form = new FormData()
    form.append('file', file)
    return request('/api/v1/analysis/upload', { method: 'POST', body: form })
  }
}
