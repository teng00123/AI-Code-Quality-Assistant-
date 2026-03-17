<template>
  <div class="reports">
    <div class="panel">
      <div class="panel-header">
        <span class="panel-dot"></span>
        <span>{{ t.reports.title }}</span>
        <div class="header-right">
          <button class="icon-btn" :disabled="loading" @click="loadReports" title="刷新">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14"
              :class="{ spinning: loading }">
              <polyline points="23 4 23 10 17 10"/>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
          </button>
          <button class="export-btn" :disabled="loading || !reports.length" @click="exportAll">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            {{ t.reports.export }}
          </button>
        </div>
      </div>

      <!-- 加载中 / 空状态 -->
      <div v-if="loading" class="empty-state">
        <div class="loading-dots"><i></i><i></i><i></i></div>
        <p class="empty-hint">加载中...</p>
      </div>
      <div v-else-if="!reports.length" class="empty-state">
        <svg viewBox="0 0 48 48" fill="none" width="48" height="48">
          <path d="M28 4H12a4 4 0 0 0-4 4v32a4 4 0 0 0 4 4h24a4 4 0 0 0 4-4V16z" stroke="rgba(0,245,255,0.3)" stroke-width="1.5"/>
          <polyline points="28,4 28,16 40,16" stroke="rgba(0,245,255,0.3)" stroke-width="1.5"/>
        </svg>
        <p class="empty-hint">暂无分析报告，请先在「代码分析」页面提交分析任务</p>
      </div>

      <!-- 表格 -->
      <template v-else>
        <div class="reports-table">
          <div class="table-head">
            <span>{{ t.reports.filename }}</span>
            <span>{{ t.reports.date }}</span>
            <span>{{ t.reports.score }}</span>
            <span>{{ t.reports.grade }}</span>
            <span>{{ t.reports.issues }}</span>
            <span>{{ t.reports.status }}</span>
            <span>{{ t.reports.actions }}</span>
          </div>

          <div v-for="row in pagedReports" :key="row.analysis_id" class="table-row">
            <span class="cell-filename">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
              </svg>
              {{ row.filename }}
            </span>
            <span class="cell-date">{{ formatDate(row.created_at) }}</span>
            <span class="cell-score" :style="{ color: getScoreColor(row.score) }">{{ row.score }}</span>
            <span class="cell-grade">
              <span class="grade-badge" :style="getGradeStyle(row.grade)">{{ row.grade }}</span>
            </span>
            <span class="cell-issues">{{ row.issues }}</span>
            <span class="cell-status">
              <span class="status-dot green"></span>
              {{ t.reports.done }}
            </span>
            <span class="cell-actions">
              <button class="action-btn view" @click="viewReport(row)">{{ t.reports.view }}</button>
              <button class="action-btn export-single" @click="exportOne(row)">↓</button>
              <button class="action-btn delete" @click="deleteReport(row)">{{ t.reports.delete }}</button>
            </span>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination">
          <span class="page-info">{{ reports.length }} {{ t.reports.total ?? '条记录' }}</span>
          <div class="page-btns">
            <button class="page-btn" :disabled="currentPage <= 1" @click="currentPage--">&lt;</button>
            <span class="page-num">{{ currentPage }} / {{ totalPages }}</span>
            <button class="page-btn" :disabled="currentPage >= totalPages" @click="currentPage++">&gt;</button>
          </div>
        </div>
      </template>
    </div>

    <!-- 详情 Modal -->
    <div v-if="detailVisible" class="modal-mask" @click.self="detailVisible = false">
      <div class="modal">
        <div class="modal-header">
          <span>{{ detailReport?.filename }}</span>
          <button class="modal-close" @click="detailVisible = false">✕</button>
        </div>
        <div class="modal-body" v-if="detailReport">
          <div class="detail-score-row">
            <span class="detail-score" :style="{ color: getScoreColor(detailReport.score) }">
              {{ detailReport.score }} <small>/ 100</small>
            </span>
            <span class="grade-badge" :style="getGradeStyle(detailReport.grade)">{{ detailReport.grade }}</span>
          </div>
          <div v-if="detailReport.dimensions" class="detail-dims">
            <div v-for="(val, key) in detailReport.dimensions" :key="key" class="dim-row">
              <span class="dim-label">{{ dimLabel(key) }}</span>
              <div class="dim-bar-track">
                <div class="dim-bar-fill" :style="{ width: val + '%', background: getDimColor(val) }"></div>
              </div>
              <span class="dim-val">{{ val }}</span>
            </div>
          </div>
          <div v-if="detailReport.issues?.length" class="detail-issues">
            <p class="detail-section-title">问题列表（{{ detailReport.issues.length }}）</p>
            <div v-for="(issue, i) in detailReport.issues" :key="i" class="issue-row" :class="issue.type">
              <span class="issue-line">L{{ issue.line }}</span>
              <span class="issue-type-badge" :class="issue.type">{{ issue.type }}</span>
              <span class="issue-msg">{{ issue.message }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="export-btn" @click="exportOne(detailReport)">导出 JSON</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from '../i18n/index.js'
import { reportsApi } from '../api/index.js'

const { t } = useI18n()

// ── state ──────────────────────────────────────
const reports      = ref([])
const loading      = ref(false)
const currentPage  = ref(1)
const pageSize     = ref(10)
const detailVisible = ref(false)
const detailReport  = ref(null)

const totalPages  = computed(() => Math.max(1, Math.ceil(reports.value.length / pageSize.value)))
const pagedReports = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return reports.value.slice(start, start + pageSize.value)
})

// ── load ───────────────────────────────────────
const loadReports = async () => {
  loading.value = true
  try {
    const res = await reportsApi.list(100)
    // 后端返回格式: { success, total, results: [...] }
    const raw = res.results ?? res.data ?? []
    reports.value = raw.map(item => ({
      analysis_id: item.analysis_id,
      filename:    item.file_path ? item.file_path.split('/').pop() : (item.filename ?? '—'),
      created_at:  item.created_at,
      score:       item.quality_score?.total_score ?? item.score ?? '—',
      grade:       item.quality_score?.grade       ?? item.grade ?? '—',
      issues:      item.issues?.length ?? item.summary?.total_issues ?? 0,
      dimensions:  item.quality_score?.dimensions  ?? null,
      issues_detail: item.issues ?? [],
    }))
  } catch (e) {
    ElMessage.error(`加载失败：${e.message}`)
  } finally {
    loading.value = false
  }
}

// ── actions ────────────────────────────────────
const viewReport = async (row) => {
  loading.value = true
  try {
    const res = await reportsApi.get(row.analysis_id)
    const item = res.data ?? res
    detailReport.value = {
      analysis_id: item.analysis_id,
      filename:    item.file_path ? item.file_path.split('/').pop() : row.filename,
      created_at:  item.created_at,
      score:       item.quality_score?.total_score ?? row.score,
      grade:       item.quality_score?.grade       ?? row.grade,
      dimensions:  item.quality_score?.dimensions  ?? null,
      issues:      item.issues ?? [],
    }
    detailVisible.value = true
  } catch (e) {
    ElMessage.error(`获取详情失败：${e.message}`)
  } finally {
    loading.value = false
  }
}

const deleteReport = (row) => {
  ElMessageBox.confirm(
    `${t.value.reports.confirmDelete} "${row.filename}"？`,
    t.value.reports.confirmTitle,
    { confirmButtonText: t.value.reports.confirm, cancelButtonText: t.value.reports.cancel, type: 'warning' }
  ).then(async () => {
    try {
      await reportsApi.delete(row.analysis_id)
      reports.value = reports.value.filter(r => r.analysis_id !== row.analysis_id)
      ElMessage.success(t.value.reports.deleted)
    } catch (e) {
      ElMessage.error(`删除失败：${e.message}`)
    }
  }).catch(() => ElMessage.info(t.value.reports.cancelDelete))
}

const exportOne = (row) => {
  reportsApi.export(row)
  ElMessage.success(t.value.reports.exporting)
}

const exportAll = () => {
  reportsApi.exportAll(reports.value)
  ElMessage.success(t.value.reports.exporting)
}

// ── helpers ────────────────────────────────────
const formatDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('zh-CN', { hour12: false })
}

const getScoreColor = (score) => {
  if (score >= 90) return '#00ff88'
  if (score >= 80) return '#00f5ff'
  if (score >= 70) return '#ffaa00'
  return '#ff006e'
}

const getGradeStyle = (grade) => {
  const color = getScoreColor({ A: 95, B: 85, C: 75, D: 65, F: 50 }[grade] || 50)
  return { color, borderColor: color, boxShadow: `0 0 8px ${color}40` }
}

const getDimColor = (v) => {
  if (v >= 90) return 'linear-gradient(90deg,#00ff88,#00f5ff)'
  if (v >= 80) return 'linear-gradient(90deg,#00f5ff,#7b2ff7)'
  if (v >= 70) return 'linear-gradient(90deg,#ffaa00,#ff6b00)'
  return 'linear-gradient(90deg,#ff006e,#ff4444)'
}

const dimLabel = (key) => ({
  maintainability: '可维护性', readability: '可读性', security: '安全性', performance: '性能'
}[key] ?? key)

onMounted(loadReports)
</script>

<style scoped>
.reports { display: flex; flex-direction: column; gap: 20px; }

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

.header-right { margin-left: auto; display: flex; align-items: center; gap: 8px; }

.icon-btn {
  width: 30px; height: 30px; border-radius: 8px;
  border: 1px solid var(--border); background: transparent;
  color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.icon-btn:hover:not(:disabled) { border-color: var(--cyan); color: var(--cyan); }
.icon-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.spinning { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.export-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px;
  background: linear-gradient(135deg, var(--cyan), var(--purple));
  border: none; border-radius: 8px;
  color: #030712; font-weight: 700; font-size: 12px;
  cursor: pointer; transition: all 0.2s; letter-spacing: 0.04em;
}
.export-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,245,255,0.3); }
.export-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* Empty / loading */
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 60px 0; color: var(--text-muted); font-size: 13px; }
.loading-dots { display: flex; gap: 5px; }
.loading-dots i { width: 6px; height: 6px; background: var(--cyan); border-radius: 50%; animation: blink 1.2s infinite; }
.loading-dots i:nth-child(2) { animation-delay: 0.2s; }
.loading-dots i:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80%,100%{opacity:0.2} 40%{opacity:1} }

/* Table */
.reports-table { overflow-x: auto; }
.table-head {
  display: grid; grid-template-columns: 1.6fr 1.4fr 70px 55px 65px 80px 150px;
  gap: 12px; padding: 8px 12px;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--text-muted); border-bottom: 1px solid var(--border);
}
.table-row {
  display: grid; grid-template-columns: 1.6fr 1.4fr 70px 55px 65px 80px 150px;
  gap: 12px; padding: 12px; align-items: center;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-size: 13px; transition: background 0.2s;
}
.table-row:hover { background: rgba(255,255,255,0.02); }
.table-row:last-child { border-bottom: none; }

.cell-filename { display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono',monospace; color: var(--text-primary); }
.cell-filename svg { color: var(--cyan); flex-shrink: 0; }
.cell-date { font-size: 12px; color: var(--text-secondary); font-family: 'JetBrains Mono',monospace; }
.cell-score { font-family: 'JetBrains Mono',monospace; font-weight: 700; font-size: 14px; }
.grade-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border: 1.5px solid; border-radius: 6px;
  font-weight: 700; font-size: 13px; background: var(--bg-deep);
}
.cell-issues { font-family: 'JetBrains Mono',monospace; color: var(--text-secondary); }
.cell-status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.green { background: var(--green); box-shadow: 0 0 6px var(--green); }

.cell-actions { display: flex; gap: 6px; }
.action-btn {
  padding: 4px 8px; border-radius: 6px; border: 1px solid;
  font-size: 11px; font-weight: 600; cursor: pointer; transition: all 0.2s; background: transparent;
}
.action-btn.view { color: var(--cyan); border-color: rgba(0,245,255,0.3); }
.action-btn.view:hover { background: rgba(0,245,255,0.08); }
.action-btn.export-single { color: #00ff88; border-color: rgba(0,255,136,0.3); }
.action-btn.export-single:hover { background: rgba(0,255,136,0.08); }
.action-btn.delete { color: var(--pink); border-color: rgba(255,0,110,0.3); }
.action-btn.delete:hover { background: rgba(255,0,110,0.08); }

/* Pagination */
.pagination {
  display: flex; align-items: center; justify-content: flex-end;
  gap: 16px; margin-top: 16px; padding-top: 16px;
  border-top: 1px solid var(--border);
}
.page-info { font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono',monospace; }
.page-btns { display: flex; align-items: center; gap: 8px; }
.page-btn {
  width: 28px; height: 28px; border-radius: 6px;
  border: 1px solid var(--border); background: transparent;
  color: var(--text-secondary); cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center; font-size: 12px;
}
.page-btn:hover:not(:disabled) { border-color: var(--cyan); color: var(--cyan); }
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.page-num { font-size: 12px; font-family: 'JetBrains Mono',monospace; color: var(--text-primary); min-width: 50px; text-align: center; }

/* Modal */
.modal-mask {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(3,7,18,0.8); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
}
.modal {
  background: #0f1929; border: 1px solid var(--border-glow);
  border-radius: 14px; width: min(640px, 92vw); max-height: 80vh;
  display: flex; flex-direction: column; overflow: hidden;
  box-shadow: 0 0 40px rgba(0,245,255,0.15);
}
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  font-weight: 600; font-size: 14px; color: var(--text-primary);
  font-family: 'JetBrains Mono',monospace;
}
.modal-close {
  background: transparent; border: none; color: var(--text-muted);
  cursor: pointer; font-size: 16px; transition: color 0.2s;
}
.modal-close:hover { color: var(--pink); }
.modal-body { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; }
.modal-footer { padding: 12px 20px; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; }

.detail-score-row { display: flex; align-items: center; gap: 16px; }
.detail-score { font-size: 36px; font-weight: 700; font-family: 'JetBrains Mono',monospace; }
.detail-score small { font-size: 14px; color: var(--text-muted); }

.detail-dims { display: flex; flex-direction: column; gap: 12px; }
.dim-row { display: grid; grid-template-columns: 80px 1fr 36px; align-items: center; gap: 10px; }
.dim-label { font-size: 12px; color: var(--text-secondary); }
.dim-bar-track { height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.dim-bar-fill { height: 100%; border-radius: 3px; transition: width 1s ease; }
.dim-val { font-size: 12px; font-family: 'JetBrains Mono',monospace; color: var(--text-secondary); text-align: right; }

.detail-section-title { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 8px; }
.issue-row { display: grid; grid-template-columns: 50px 70px 1fr; gap: 10px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 12px; }
.issue-line { font-family: 'JetBrains Mono',monospace; color: var(--text-muted); }
.issue-type-badge { padding: 1px 6px; border-radius: 4px; border: 1px solid; text-align: center; font-weight: 600; }
.issue-type-badge.error   { color: var(--pink);  border-color: rgba(255,0,110,0.3);  background: rgba(255,0,110,0.08); }
.issue-type-badge.warning { color: #ffaa00;       border-color: rgba(255,170,0,0.3);  background: rgba(255,170,0,0.08); }
.issue-type-badge.info    { color: var(--cyan);   border-color: rgba(0,245,255,0.3);  background: rgba(0,245,255,0.08); }
.issue-msg { color: var(--text-primary); }
</style>
