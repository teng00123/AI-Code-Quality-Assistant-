<template>
  <div class="reports">
    <div class="panel">
      <div class="panel-header">
        <span class="panel-dot"></span>
        <span>{{ t.reports.title }}</span>
        <button class="export-btn" @click="exportReport">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          {{ t.reports.export }}
        </button>
      </div>

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

        <div
          v-for="row in reports"
          :key="row.id"
          class="table-row"
        >
          <span class="cell-filename">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
            </svg>
            {{ row.filename }}
          </span>
          <span class="cell-date">{{ row.date }}</span>
          <span class="cell-score" :style="{ color: getScoreColor(row.score) }">{{ row.score }}</span>
          <span class="cell-grade">
            <span class="grade-badge" :style="getGradeStyle(row.grade)">{{ row.grade }}</span>
          </span>
          <span class="cell-issues">{{ row.issues }}</span>
          <span class="cell-status">
            <span class="status-dot" :class="row.status === 'done' ? 'green' : 'yellow'"></span>
            {{ row.status === 'done' ? t.reports.done : row.status }}
          </span>
          <span class="cell-actions">
            <button class="action-btn view" @click="viewReport(row)">{{ t.reports.view }}</button>
            <button class="action-btn delete" @click="deleteReport(row)">{{ t.reports.delete }}</button>
          </span>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <span class="page-info">{{ reports.length }} / {{ totalReports }}</span>
        <div class="page-btns">
          <button class="page-btn" :disabled="currentPage <= 1" @click="currentPage--">&lt;</button>
          <span class="page-num">{{ currentPage }}</span>
          <button class="page-btn" :disabled="currentPage >= totalPages" @click="currentPage++">&gt;</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const currentPage = ref(1)
const pageSize = ref(10)
const totalReports = ref(25)
const totalPages = computed(() => Math.ceil(totalReports.value / pageSize.value))

const reports = ref([
  { id: 1, filename: 'main.py',   date: '2024-03-17', score: 85, grade: 'B', issues: 3, status: 'done' },
  { id: 2, filename: 'utils.js',  date: '2024-03-16', score: 92, grade: 'A', issues: 1, status: 'done' },
  { id: 3, filename: 'app.ts',    date: '2024-03-15', score: 78, grade: 'C', issues: 8, status: 'done' },
  { id: 4, filename: 'server.go', date: '2024-03-14', score: 88, grade: 'B', issues: 2, status: 'done' },
  { id: 5, filename: 'lib.rs',    date: '2024-03-13', score: 95, grade: 'A', issues: 0, status: 'done' }
])

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

const viewReport = (report) => {
  ElMessage.info(`${t.value.reports.viewMsg}: ${report.filename}`)
}

const deleteReport = (report) => {
  ElMessageBox.confirm(
    `${t.value.reports.confirmDelete} "${report.filename}"？`,
    t.value.reports.confirmTitle,
    {
      confirmButtonText: t.value.reports.confirm,
      cancelButtonText:  t.value.reports.cancel,
      type: 'warning'
    }
  ).then(() => {
    const index = reports.value.findIndex(r => r.id === report.id)
    if (index !== -1) {
      reports.value.splice(index, 1)
      totalReports.value--
      ElMessage.success(t.value.reports.deleted)
    }
  }).catch(() => {
    ElMessage.info(t.value.reports.cancelDelete)
  })
}

const exportReport = () => {
  ElMessage.success(t.value.reports.exporting)
}
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

.export-btn {
  margin-left: auto;
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px;
  background: linear-gradient(135deg, var(--cyan), var(--purple));
  border: none; border-radius: 8px;
  color: #030712; font-weight: 700; font-size: 12px;
  cursor: pointer; transition: all 0.2s; letter-spacing: 0.04em;
}
.export-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,245,255,0.3); }

/* Table */
.reports-table { overflow-x: auto; }

.table-head {
  display: grid;
  grid-template-columns: 1.6fr 1.2fr 80px 60px 70px 90px 120px;
  gap: 12px; padding: 8px 12px;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--text-muted); border-bottom: 1px solid var(--border);
}

.table-row {
  display: grid;
  grid-template-columns: 1.6fr 1.2fr 80px 60px 70px 90px 120px;
  gap: 12px; padding: 12px; align-items: center;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-size: 13px; transition: background 0.2s;
}
.table-row:hover { background: rgba(255,255,255,0.02); }
.table-row:last-child { border-bottom: none; }

.cell-filename {
  display: flex; align-items: center; gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-primary); font-size: 13px;
}
.cell-filename svg { color: var(--cyan); flex-shrink: 0; }

.cell-date { font-size: 12px; color: var(--text-secondary); font-family: 'JetBrains Mono', monospace; }

.cell-score { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px; }

.grade-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px;
  border: 1.5px solid; border-radius: 6px;
  font-weight: 700; font-size: 13px;
  background: var(--bg-deep);
}

.cell-issues { font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); }

.cell-status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.green { background: var(--green); box-shadow: 0 0 6px var(--green); }
.status-dot.yellow { background: #ffaa00; box-shadow: 0 0 6px #ffaa00; }

.cell-actions { display: flex; gap: 8px; }
.action-btn {
  padding: 4px 10px; border-radius: 6px; border: 1px solid;
  font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;
  background: transparent;
}
.action-btn.view {
  color: var(--cyan); border-color: rgba(0,245,255,0.3);
}
.action-btn.view:hover { background: rgba(0,245,255,0.08); }
.action-btn.delete {
  color: var(--pink); border-color: rgba(255,0,110,0.3);
}
.action-btn.delete:hover { background: rgba(255,0,110,0.08); }

/* Pagination */
.pagination {
  display: flex; align-items: center; justify-content: flex-end;
  gap: 16px; margin-top: 16px; padding-top: 16px;
  border-top: 1px solid var(--border);
}
.page-info { font-size: 12px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }
.page-btns { display: flex; align-items: center; gap: 8px; }
.page-btn {
  width: 28px; height: 28px; border-radius: 6px;
  border: 1px solid var(--border); background: transparent;
  color: var(--text-secondary); cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: center; font-size: 12px;
}
.page-btn:hover:not(:disabled) { border-color: var(--cyan); color: var(--cyan); }
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.page-num { font-size: 13px; font-family: 'JetBrains Mono', monospace; color: var(--text-primary); min-width: 24px; text-align: center; }
</style>
