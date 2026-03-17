<template>
  <div class="settings">
    <div class="settings-grid">
      <!-- 侧边菜单 -->
      <div class="settings-nav">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="snav-item"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          <span class="snav-icon" v-html="tab.icon"></span>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- 设置内容 -->
      <div class="settings-body">

        <!-- 通用设置 -->
        <div v-if="activeTab === 'general'" class="settings-section">
          <div class="section-title">通用设置</div>
          <div class="field-group">

            <div class="field">
              <label>界面语言</label>
              <div class="radio-group">
                <label class="radio-opt" v-for="l in languages" :key="l.value">
                  <input type="radio" v-model="settings.language" :value="l.value"/>
                  <span class="radio-box"></span>
                  <span>{{ l.label }}</span>
                </label>
              </div>
              <p class="field-hint">当前：{{ settings.language === 'zh-CN' ? '中文' : 'English' }} — 已实时应用</p>
            </div>

            <div class="field">
              <label>主题模式</label>
              <div class="theme-cards">
                <div
                  v-for="t in themes"
                  :key="t.key"
                  class="theme-card"
                  :class="{ active: settings.theme === t.key }"
                  @click="settings.theme = t.key"
                >
                  <div class="theme-preview" :style="t.preview">
                    <div class="theme-preview-dots">
                      <span v-for="c in t.dots" :key="c" :style="{ background: c }"></span>
                    </div>
                  </div>
                  <span>{{ t.label }}</span>
                  <span v-if="settings.theme === t.key" class="theme-active-mark">✓</span>
                </div>
              </div>
              <p class="field-hint">主题已实时切换 CSS 变量</p>
            </div>

            <div class="field">
              <label>自动刷新间隔</label>
              <div class="slider-wrap">
                <input
                  type="range"
                  v-model.number="settings.refreshInterval"
                  min="30" max="3600" step="30"
                  class="cyber-range"
                />
                <span class="slider-val">{{ formatInterval(settings.refreshInterval) }}</span>
              </div>
            </div>

          </div>
        </div>

        <!-- API设置 -->
        <div v-if="activeTab === 'api'" class="settings-section">
          <div class="section-title">API 设置</div>
          <div class="field-group">

            <div class="field">
              <label>后端 API 地址</label>
              <div class="input-wrap">
                <span class="input-prefix">{{ settings.httpsEnabled ? 'https://' : 'http://' }}</span>
                <input v-model="settings.apiBaseURL" class="cyber-input with-prefix" placeholder="localhost:8000"/>
              </div>
              <p class="field-hint">完整地址：{{ settings.httpsEnabled ? 'https' : 'http' }}://{{ settings.apiBaseURL }}</p>
            </div>

            <div class="field">
              <label>请求超时 (ms)</label>
              <input v-model.number="settings.apiTimeout" type="number" class="cyber-input" min="1000" max="60000" step="1000"/>
              <p class="field-hint">当前：{{ settings.apiTimeout / 1000 }}s</p>
            </div>

            <div class="field">
              <label>启用 HTTPS</label>
              <div class="toggle-wrap">
                <div class="cyber-toggle" :class="{ on: settings.httpsEnabled }" @click="settings.httpsEnabled = !settings.httpsEnabled">
                  <div class="toggle-thumb"></div>
                </div>
                <span class="toggle-label" :class="{ active: settings.httpsEnabled }">
                  {{ settings.httpsEnabled ? '✓ 已启用' : '已关闭' }}
                </span>
              </div>
            </div>

          </div>
        </div>

        <!-- 通知设置 -->
        <div v-if="activeTab === 'notifications'" class="settings-section">
          <div class="section-title">通知设置</div>
          <div class="field-group">
            <div v-for="n in notifOptions" :key="n.key" class="field row">
              <div class="field-info">
                <span class="field-label">{{ n.label }}</span>
                <span class="field-desc">{{ n.desc }}</span>
              </div>
              <div class="cyber-toggle" :class="{ on: settings[n.storeKey] }" @click="settings[n.storeKey] = !settings[n.storeKey]">
                <div class="toggle-thumb"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="settings-actions">
          <button class="cyber-btn" @click="save">
            <span class="btn-icon">💾</span> 保存设置
          </button>
          <button class="ghost-btn" @click="handleReset">恢复默认</button>
          <span v-if="savedTip" class="saved-tip">✓ 已保存</span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useSettingsStore } from '../store/settings.js'

const activeTab = ref('general')
const savedTip = ref(false)
const settings = useSettingsStore()

const tabs = [
  {
    key: 'general', label: '通用设置',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg>`
  },
  {
    key: 'api', label: 'API 设置',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>`
  },
  {
    key: 'notifications', label: '通知设置',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`
  }
]

const languages = [
  { value: 'zh-CN', label: '中文' },
  { value: 'en-US', label: 'English' }
]

const themes = [
  {
    key: 'dark', label: '深色',
    preview: 'background: linear-gradient(135deg, #030712, #0f1929)',
    dots: ['#00f5ff', '#7b2ff7', '#00ff88']
  },
  {
    key: 'cyber', label: '赛博',
    preview: 'background: linear-gradient(135deg, #050515, #0a0a2e)',
    dots: ['#00e5ff', '#9b00ff', '#ff006e']
  },
  {
    key: 'auto', label: '星空',
    preview: 'background: linear-gradient(135deg, #0d1117, #161b22)',
    dots: ['#58a6ff', '#bc8cff', '#3fb950']
  }
]

const notifOptions = [
  { key: 'analysisComplete', storeKey: 'notifAnalysisComplete', label: '分析完成通知', desc: '代码分析任务完成后发送提醒' },
  { key: 'newIssues',        storeKey: 'notifNewIssues',        label: '新问题提醒',   desc: '检测到新的代码问题时通知' },
  { key: 'qualityDrop',      storeKey: 'notifQualityDrop',      label: '质量下降告警', desc: '代码质量评分下降超过阈值时警报' }
]

const formatInterval = (s) => s >= 60 ? `${Math.floor(s / 60)}m ${s % 60 ? s % 60 + 's' : ''}`.trim() : `${s}s`

const save = () => {
  settings.persist()
  savedTip.value = true
  setTimeout(() => savedTip.value = false, 2000)
  ElMessage({ message: '✓ 设置已保存并生效', type: 'success' })
}

const handleReset = () => {
  ElMessageBox.confirm('确定恢复所有默认设置？', '确认重置', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    settings.reset()
    ElMessage.info('已恢复默认设置')
  }).catch(() => {})
}
</script>

<style scoped>
.settings { height: 100%; }
.settings-grid { display: grid; grid-template-columns: 200px 1fr; gap: 20px; }

.settings-nav {
  display: flex; flex-direction: column; gap: 4px;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius); padding: 12px;
  height: fit-content;
}
.snav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  border: none; background: transparent;
  color: var(--text-secondary); font-size: 13px; font-weight: 500;
  cursor: pointer; transition: all 0.2s; text-align: left; width: 100%;
}
.snav-item:hover { color: var(--text-primary); background: rgba(255,255,255,0.04); }
.snav-item.active { color: var(--cyan); background: rgba(0,245,255,0.08); border: 1px solid rgba(0,245,255,0.15); }
.snav-icon { width: 18px; height: 18px; flex-shrink: 0; }
.snav-icon :deep(svg) { width: 100%; height: 100%; }

.settings-body {
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius); padding: 24px;
}
.section-title { font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 24px; letter-spacing: 0.03em; }
.field-group { display: flex; flex-direction: column; gap: 24px; }
.field { display: flex; flex-direction: column; gap: 10px; }
.field.row { flex-direction: row; align-items: center; justify-content: space-between; padding: 16px; background: rgba(255,255,255,0.02); border-radius: 10px; border: 1px solid var(--border); }
.field > label, .field-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-secondary); }
.field-hint { font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; margin-top: -4px; }
.field-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
.field-info { display: flex; flex-direction: column; gap: 2px; }

/* 单选 */
.radio-group { display: flex; gap: 16px; }
.radio-opt { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; color: var(--text-primary); }
.radio-opt input { display: none; }
.radio-box { width: 16px; height: 16px; border-radius: 50%; border: 1.5px solid var(--border); transition: all 0.2s; }
.radio-opt input:checked ~ .radio-box { border-color: var(--cyan); background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }
.radio-opt input:checked + .radio-box { border-color: var(--cyan); background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }

/* 主题卡 */
.theme-cards { display: flex; gap: 12px; flex-wrap: wrap; }
.theme-card {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 12px; border-radius: 10px; border: 1.5px solid var(--border);
  cursor: pointer; transition: all 0.2s; min-width: 90px; position: relative;
}
.theme-card:hover { border-color: rgba(0,245,255,0.3); transform: translateY(-2px); }
.theme-card.active { border-color: var(--cyan); box-shadow: 0 0 16px rgba(0,245,255,0.2); }
.theme-preview { width: 66px; height: 40px; border-radius: 6px; display: flex; align-items: flex-end; padding: 6px; }
.theme-preview-dots { display: flex; gap: 3px; }
.theme-preview-dots span { width: 8px; height: 8px; border-radius: 50%; display: block; }
.theme-card span { font-size: 12px; color: var(--text-secondary); }
.theme-active-mark { position: absolute; top: 6px; right: 8px; font-size: 11px; color: var(--cyan); font-weight: 700; }

/* 滑块 */
.slider-wrap { display: flex; align-items: center; gap: 12px; }
.cyber-range { flex: 1; -webkit-appearance: none; height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; outline: none; }
.cyber-range::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); cursor: pointer; }
.slider-val { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--cyan); min-width: 52px; text-align: right; }

/* 输入框 */
.input-wrap { display: flex; align-items: center; }
.input-prefix { padding: 10px 10px 10px 14px; background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-right: none; border-radius: 8px 0 0 8px; font-size: 13px; color: var(--cyan); font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
.cyber-input { width: 100%; padding: 10px 14px; background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: 8px; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; font-size: 13px; outline: none; transition: all 0.2s; }
.cyber-input.with-prefix { border-radius: 0 8px 8px 0; flex: 1; }
.cyber-input:focus { border-color: var(--cyan); box-shadow: 0 0 0 2px rgba(0,245,255,0.12); }

/* 开关 */
.toggle-wrap { display: flex; align-items: center; gap: 10px; }
.cyber-toggle { width: 44px; height: 24px; border-radius: 12px; background: rgba(255,255,255,0.08); border: 1px solid var(--border); cursor: pointer; position: relative; transition: all 0.3s; flex-shrink: 0; }
.cyber-toggle.on { background: rgba(0,245,255,0.2); border-color: var(--cyan); box-shadow: 0 0 10px rgba(0,245,255,0.2); }
.toggle-thumb { position: absolute; top: 2px; left: 2px; width: 18px; height: 18px; border-radius: 50%; background: var(--text-muted); transition: all 0.3s; }
.cyber-toggle.on .toggle-thumb { left: 22px; background: var(--cyan); box-shadow: 0 0 6px var(--cyan); }
.toggle-label { font-size: 13px; color: var(--text-secondary); transition: color 0.2s; }
.toggle-label.active { color: var(--cyan); }

/* 按钮 */
.settings-actions { display: flex; align-items: center; gap: 12px; margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border); }
.cyber-btn { display: flex; align-items: center; gap: 6px; padding: 10px 24px; background: linear-gradient(135deg, var(--cyan), var(--purple)); border: none; border-radius: 8px; color: #030712; font-weight: 700; font-size: 13px; letter-spacing: 0.05em; cursor: pointer; transition: all 0.2s; }
.cyber-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0,245,255,0.3); }
.ghost-btn { padding: 10px 24px; background: transparent; border: 1px solid var(--border); border-radius: 8px; color: var(--text-secondary); font-size: 13px; cursor: pointer; transition: all 0.2s; }
.ghost-btn:hover { border-color: rgba(0,245,255,0.3); color: var(--text-primary); }
.saved-tip { font-size: 13px; color: var(--green); animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateX(-8px); } to { opacity: 1; transform: translateX(0); } }
</style>
