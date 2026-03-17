<template>
  <div class="analysis">
    <!-- 上传/分析区 -->
    <div class="analysis-grid">
      <div class="panel upload-panel">
        <div class="panel-header">
          <span class="panel-dot"></span>
          <span>{{ t.analysis.title }}</span>
        </div>
        <div class="panel-tabs">
          <button
            v-for="t in tabs"
            :key="t.key"
            class="ptab"
            :class="{ active: activeTab === t.key }"
            @click="activeTab = t.key"
          >{{ t.label }}</button>
        </div>

        <!-- 拖拽上传 -->
        <div v-if="activeTab === 'upload'" class="upload-zone" :class="{ dragging }"
          @dragover.prevent="dragging = true"
          @dragleave="dragging = false"
          @drop.prevent="onDrop"
        >
          <div class="upload-icon">
            <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M24 8v24M16 16l8-8 8 8"/>
              <path d="M8 32v4a4 4 0 0 0 4 4h24a4 4 0 0 0 4-4v-4"/>
            </svg>
          </div>
          <p class="upload-title">{{ t.analysis.dropHint }} <span class="upload-link" @click="triggerFile">{{ t.analysis.clickSelect }}</span></p>
          <p class="upload-hint">{{ t.analysis.supportedTypes }}</p>
          <input ref="fileInput" type="file" style="display:none" accept=".py,.js,.ts,.java,.go,.rs" @change="onFileSelect"/>
        </div>

        <!-- 路径分析 -->
        <div v-if="activeTab === 'path'" class="path-form">
          <div class="input-group">
            <label>{{ t.analysis.filePath }}</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
              </span>
              <input v-model="pathForm.filePath" placeholder="/path/to/your/code.py" class="cyber-input"/>
            </div>
          </div>
          <button class="cyber-btn" @click="analyzeByPath" :disabled="loading">
            <span v-if="!loading">{{ t.analysis.startAnalysis }}</span>
            <span v-else class="loading-dots"><i></i><i></i><i></i></span>
          </button>
        </div>

        <!-- 文件名显示 -->
        <div v-if="selectedFile" class="selected-file">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14,2 14,8 20,8"/></svg>
          <span>{{ selectedFile }}</span>
          <button class="analyze-file-btn" @click="analyzeFile" :disabled="loading">
            {{ loading ? t.analysis.analyzing : t.analysis.analyzeFile }}
          </button>
        </div>
      </div>

      <!-- 分析结果 -->
      <div class="panel result-panel" v-if="analysisResult">
        <div class="panel-header">
          <span class="panel-dot green"></span>
          <span>{{ t.analysis.result }} — {{ analysisResult.filename }}</span>
        </div>

        <!-- 分数展示 -->
        <div class="score-section">
          <div class="score-ring-wrap">
            <svg class="score-ring" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
              <circle
                cx="60" cy="60" r="50" fill="none"
                :stroke="scoreColor"
                stroke-width="8"
                stroke-linecap="round"
                :stroke-dasharray="`${2 * Math.PI * 50 * analysisResult.quality_score.total_score / 100} ${2 * Math.PI * 50}`"
                stroke-dashoffset="0"
                transform="rotate(-90 60 60)"
                :style="{ filter: `drop-shadow(0 0 8px ${scoreColor})` }"
              />
              <text x="60" y="55" text-anchor="middle" :fill="scoreColor" font-size="22" font-weight="700" font-family="JetBrains Mono">
                {{ analysisResult.quality_score.total_score }}
              </text>
              <text x="60" y="72" text-anchor="middle" fill="#64748b" font-size="11">/ 100</text>
            </svg>
            <div class="grade-badge" :style="{ color: scoreColor, borderColor: scoreColor, boxShadow: `0 0 15px ${scoreColor}40` }">
              {{ analysisResult.quality_score.grade }}
            </div>
          </div>
          <div class="dimension-bars">
            <div v-for="(val, key) in analysisResult.quality_score.dimensions" :key="key" class="dim-row">
              <span class="dim-label">{{ dimLabels[key] }}</span>
              <div class="dim-bar-track">
                <div class="dim-bar-fill" :style="{ width: val + '%', background: getDimColor(val) }"></div>
              </div>
              <span class="dim-val">{{ val }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 问题列表 -->
    <div class="panel issues-panel" v-if="analysisResult && analysisResult.analysis.issues.length">
      <div class="panel-header">
        <span class="panel-dot pink"></span>
        <span>{{ t.analysis.issuesFound }}</span>
        <span class="issue-count">{{ analysisResult.analysis.issues.length }}</span>
      </div>
      <div class="issues-table">
        <div class="issues-head">
          <span>{{ t.analysis.line }}</span>
          <span>{{ t.analysis.type }}</span>
          <span>{{ t.analysis.message }}</span>
          <span>{{ t.analysis.suggestion }}</span>
        </div>
        <div
          v-for="(issue, i) in analysisResult.analysis.issues"
          :key="i"
          class="issue-row"
          :class="issue.type"
        >
          <span class="issue-line">L{{ issue.line }}</span>
          <span class="issue-type-badge" :class="issue.type">{{ issue.type }}</span>
          <span class="issue-msg">{{ issue.message }}</span>
          <span class="issue-suggestion">{{ issue.suggestion }}</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!analysisResult" class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 80 80" fill="none">
          <polygon points="40,4 76,22 76,58 40,76 4,58 4,22" stroke="rgba(0,245,255,0.2)" stroke-width="1.5" fill="none"/>
          <polygon points="40,14 66,28 66,52 40,66 14,52 14,28" stroke="rgba(0,245,255,0.1)" stroke-width="1" fill="none"/>
          <circle cx="40" cy="40" r="12" stroke="rgba(0,245,255,0.4)" stroke-width="1.5" fill="rgba(0,245,255,0.05)"/>
          <line x1="40" y1="33" x2="40" y2="40" stroke="#00f5ff" stroke-width="2" stroke-linecap="round"/>
          <circle cx="40" cy="45" r="1.5" fill="#00f5ff"/>
        </svg>
      </div>
      <p class="empty-title">{{ t.analysis.waitingTitle }}</p>
      <p class="empty-hint">{{ t.analysis.waitingHint }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const activeTab = ref('upload')
const dragging = ref(false)
const selectedFile = ref('')
const fileInput = ref(null)
const analysisResult = ref(null)
const loading = ref(false)
const pathForm = ref({ filePath: '' })

const tabs = computed(() => [
  { key: 'upload', label: t.value.analysis.upload },
  { key: 'path',   label: t.value.analysis.path   }
])

const dimLabels = computed(() => ({
  maintainability: t.value.analysis.dim_maintainability,
  readability:     t.value.analysis.dim_readability,
  security:        t.value.analysis.dim_security,
  performance:     t.value.analysis.dim_performance,
}))

const scoreColor = computed(() => {
  const s = analysisResult.value?.quality_score.total_score || 0
  if (s >= 90) return '#00ff88'
  if (s >= 80) return '#00f5ff'
  if (s >= 70) return '#ffaa00'
  return '#ff006e'
})

const getDimColor = (v) => {
  if (v >= 90) return 'linear-gradient(90deg, #00ff88, #00f5ff)'
  if (v >= 80) return 'linear-gradient(90deg, #00f5ff, #7b2ff7)'
  if (v >= 70) return 'linear-gradient(90deg, #ffaa00, #ff6b00)'
  return 'linear-gradient(90deg, #ff006e, #ff4444)'
}

const triggerFile = () => fileInput.value?.click()

const onFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) selectedFile.value = file.name
}

const onDrop = (e) => {
  dragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) selectedFile.value = file.name
}

const mockAnalyze = (filename) => {
  loading.value = true
  setTimeout(() => {
    analysisResult.value = {
      filename,
      analysis: {
        issues: [
          { line: 10, type: 'error', message: '发现硬编码密码', suggestion: '使用环境变量存储敏感信息' },
          { line: 25, type: 'warning', message: '函数过长（超过50行）', suggestion: '拆分为更小的独立函数' },
          { line: 42, type: 'warning', message: '缺少错误处理', suggestion: '添加 try-catch 异常处理' },
          { line: 67, type: 'info', message: '变量命名不规范', suggestion: '使用 camelCase 命名规范' }
        ]
      },
      quality_score: {
        total_score: 85,
        grade: 'B',
        dimensions: { maintainability: 80, readability: 85, security: 90, performance: 85 }
      }
    }
    loading.value = false
    ElMessage({ message: t.value.analysis.analysisDone, type: 'success', customClass: 'cyber-toast' })
  }, 1200)
}

const analyzeFile = () => selectedFile.value && mockAnalyze(selectedFile.value)

const analyzeByPath = () => {
  if (!pathForm.value.filePath) { ElMessage.warning(t.value.analysis.enterPath); return }
  mockAnalyze(pathForm.value.filePath.split('/').pop())
}
</script>

<style scoped>
.analysis { display: flex; flex-direction: column; gap: 20px; }

.analysis-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  padding: 20px;
}
.panel-header {
  display: flex; align-items: center; gap: 10px;
  font-size: 14px; font-weight: 600; color: var(--text-primary);
  margin-bottom: 20px; letter-spacing: 0.03em;
}
.panel-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }
.panel-dot.green { background: var(--green); box-shadow: 0 0 8px var(--green); }
.panel-dot.pink { background: var(--pink); box-shadow: 0 0 8px var(--pink); }

.panel-tabs { display: flex; gap: 4px; margin-bottom: 20px; }
.ptab { padding: 6px 14px; border-radius: 8px; border: 1px solid var(--border); background: transparent; color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.ptab:hover { color: var(--text-primary); }
.ptab.active { color: var(--cyan); background: rgba(0,245,255,0.08); border-color: rgba(0,245,255,0.3); }

/* 上传区 */
.upload-zone {
  border: 1.5px dashed rgba(0,245,255,0.2);
  border-radius: 10px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
}
.upload-zone:hover, .upload-zone.dragging {
  border-color: rgba(0,245,255,0.5);
  background: rgba(0,245,255,0.04);
}
.upload-icon { width: 48px; height: 48px; color: rgba(0,245,255,0.4); margin: 0 auto 12px; }
.upload-icon svg { width: 100%; height: 100%; }
.upload-title { font-size: 14px; color: var(--text-secondary); margin-bottom: 6px; }
.upload-link { color: var(--cyan); cursor: pointer; text-decoration: underline; }
.upload-hint { font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }

/* 路径表单 */
.path-form { display: flex; flex-direction: column; gap: 16px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.08em; }
.input-wrap { position: relative; }
.input-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--text-muted); }
.input-icon svg { width: 100%; height: 100%; }
.cyber-input {
  width: 100%; padding: 10px 12px 10px 36px;
  background: rgba(255,255,255,0.04); border: 1px solid var(--border);
  border-radius: 8px; color: var(--text-primary); font-family: 'JetBrains Mono', monospace;
  font-size: 13px; outline: none; transition: all 0.2s;
}
.cyber-input:focus { border-color: var(--cyan); box-shadow: 0 0 0 2px rgba(0,245,255,0.15); }
.cyber-btn {
  padding: 10px 20px; background: linear-gradient(135deg, var(--cyan), var(--purple));
  border: none; border-radius: 8px; color: #030712; font-weight: 700;
  font-size: 13px; letter-spacing: 0.05em; cursor: pointer; transition: all 0.2s;
  align-self: flex-start;
}
.cyber-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0,245,255,0.3); }
.cyber-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* 选中文件 */
.selected-file {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  background: rgba(0,245,255,0.05);
  border: 1px solid rgba(0,245,255,0.2);
  border-radius: 8px; margin-top: 12px;
  font-size: 13px; color: var(--text-primary);
}
.selected-file svg { width: 16px; height: 16px; color: var(--cyan); flex-shrink: 0; }
.selected-file span { flex: 1; font-family: 'JetBrains Mono', monospace; }
.analyze-file-btn {
  padding: 5px 12px; background: var(--cyan); border: none; border-radius: 6px;
  color: #030712; font-weight: 600; font-size: 12px; cursor: pointer; white-space: nowrap;
  transition: all 0.2s;
}
.analyze-file-btn:hover:not(:disabled) { opacity: 0.85; }
.analyze-file-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* 分数 */
.score-section { display: flex; align-items: center; gap: 24px; }
.score-ring-wrap { position: relative; flex-shrink: 0; }
.score-ring { width: 120px; height: 120px; }
.grade-badge {
  position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
  font-size: 16px; font-weight: 700; width: 32px; height: 32px;
  border: 1.5px solid; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg-deep);
}
.dimension-bars { flex: 1; display: flex; flex-direction: column; gap: 12px; }
.dim-row { display: grid; grid-template-columns: 70px 1fr 30px; align-items: center; gap: 10px; }
.dim-label { font-size: 12px; color: var(--text-secondary); }
.dim-bar-track { height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.dim-bar-fill { height: 100%; border-radius: 3px; transition: width 1.2s cubic-bezier(0.4,0,0.2,1); }
.dim-val { font-size: 12px; font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); text-align: right; }

/* 问题表 */
.issue-count { margin-left: auto; background: rgba(255,0,110,0.15); color: var(--pink); border: 1px solid rgba(255,0,110,0.3); border-radius: 20px; padding: 2px 10px; font-size: 12px; font-weight: 600; }
.issues-table { overflow-x: auto; }
.issues-head {
  display: grid; grid-template-columns: 60px 80px 1fr 1fr;
  gap: 12px; padding: 8px 12px;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
.issue-row {
  display: grid; grid-template-columns: 60px 80px 1fr 1fr;
  gap: 12px; padding: 12px; align-items: center;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-size: 13px; transition: background 0.2s;
}
.issue-row:hover { background: rgba(255,255,255,0.02); }
.issue-line { font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); font-size: 12px; }
.issue-type-badge { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-align: center; display: inline-block; border: 1px solid; }
.issue-type-badge.error { color: var(--pink); border-color: rgba(255,0,110,0.3); background: rgba(255,0,110,0.08); }
.issue-type-badge.warning { color: #ffaa00; border-color: rgba(255,170,0,0.3); background: rgba(255,170,0,0.08); }
.issue-type-badge.info { color: var(--cyan); border-color: rgba(0,245,255,0.3); background: rgba(0,245,255,0.08); }
.issue-msg { color: var(--text-primary); }
.issue-suggestion { color: var(--text-secondary); font-size: 12px; }

/* 空状态 */
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 60px 0; }
.empty-icon svg { width: 80px; height: 80px; animation: rotate-slow 20s linear infinite; }
@keyframes rotate-slow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.empty-title { font-size: 16px; font-weight: 600; color: var(--text-secondary); }
.empty-hint { font-size: 13px; color: var(--text-muted); }

/* loading */
.loading-dots { display: flex; gap: 4px; align-items: center; justify-content: center; }
.loading-dots i { width: 5px; height: 5px; background: currentColor; border-radius: 50%; animation: blink 1.2s infinite; }
.loading-dots i:nth-child(2) { animation-delay: 0.2s; }
.loading-dots i:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 80%, 100% { opacity: 0.2; } 40% { opacity: 1; } }
</style>
