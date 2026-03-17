<template>
  <div class="dashboard">
    <!-- 顶部指标卡 -->
    <div class="metrics-grid">
      <div
        v-for="(m, i) in metrics"
        :key="i"
        class="metric-card"
        :style="{ '--accent': m.color, '--accent-rgb': m.colorRgb }"
      >
        <div class="metric-bg-glow"></div>
        <div class="metric-icon" v-html="m.icon"></div>
        <div class="metric-body">
          <div class="metric-value">
            <span class="metric-num">{{ m.value }}</span>
            <span class="metric-unit">{{ m.unit }}</span>
          </div>
          <div class="metric-label">{{ m.label }}</div>
        </div>
        <div class="metric-trend" :class="m.trend > 0 ? 'up' : 'down'">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline v-if="m.trend > 0" points="2,12 6,6 10,9 14,3"/>
            <polyline v-else points="2,3 6,9 10,6 14,12"/>
          </svg>
          {{ Math.abs(m.trend) }}%
        </div>
        <div class="metric-border-top"></div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="charts-row">
      <!-- 质量趋势 -->
      <div class="chart-card wide">
        <div class="card-header">
          <div class="card-title">
            <span class="card-dot"></span>
            {{ t.dashboard.trend }}
          </div>
          <div class="card-tabs">
            <button
              v-for="tab in tabOptions"
              :key="tab.key"
              class="tab-btn"
              :class="{ active: activeTab === tab.key }"
              @click="activeTab = tab.key"
            >{{ tab.label }}</button>
          </div>
        </div>
        <div ref="lineRef" class="chart-area"></div>
      </div>

      <!-- 问题分布 -->
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title">
            <span class="card-dot pink"></span>
            {{ t.dashboard.distribution }}
          </div>
        </div>
        <div ref="pieRef" class="chart-area"></div>
      </div>
    </div>

    <!-- 下方行 -->
    <div class="bottom-row">
      <!-- 雷达图 -->
      <div class="chart-card">
        <div class="card-header">
          <div class="card-title">
            <span class="card-dot green"></span>
            {{ t.dashboard.radar }}
          </div>
        </div>
        <div ref="radarRef" class="chart-area"></div>
      </div>

      <!-- 最近分析 -->
      <div class="chart-card wide">
        <div class="card-header">
          <div class="card-title">
            <span class="card-dot purple"></span>
            {{ t.dashboard.recent }}
          </div>
        </div>
        <div class="recent-list">
          <div v-for="(item, i) in recentItems" :key="i" class="recent-item">
            <div class="recent-file">
              <span class="file-ext" :style="{ color: item.color }">{{ item.ext }}</span>
              <span class="file-name">{{ item.name }}</span>
            </div>
            <div class="recent-bar-wrap">
              <div class="recent-bar" :style="{ width: item.score + '%', background: item.color, boxShadow: `0 0 8px ${item.color}` }"></div>
            </div>
            <div class="recent-score" :style="{ color: item.color }">{{ item.score }}</div>
            <div class="recent-grade" :style="{ borderColor: item.color, color: item.color }">{{ item.grade }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { useI18n } from '../i18n/index.js'

const { t } = useI18n()

const lineRef = ref(null)
const pieRef = ref(null)
const radarRef = ref(null)
const activeTab = ref('7d')

const metrics = computed(() => [
  {
    label: t.value.dashboard.avgScore,
    value: '85.2',
    unit: '/ 100',
    trend: 3.2,
    color: '#00f5ff',
    colorRgb: '0,245,255',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`
  },
  {
    label: t.value.dashboard.totalFiles,
    value: '127',
    unit: t.value.dashboard.files,
    trend: 12.5,
    color: '#7b2ff7',
    colorRgb: '123,47,247',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>`
  },
  {
    label: t.value.dashboard.issues,
    value: '23',
    unit: t.value.dashboard.issues_unit,
    trend: -8.1,
    color: '#ff006e',
    colorRgb: '255,0,110',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
  },
  {
    label: t.value.dashboard.coverage,
    value: '92',
    unit: '%',
    trend: 2.4,
    color: '#00ff88',
    colorRgb: '0,255,136',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="20,6 9,17 4,12"/></svg>`
  }
])

const tabOptions = computed(() => [
  { key: '7d',  label: t.value.dashboard.days7  },
  { key: '30d', label: t.value.dashboard.days30 },
  { key: '90d', label: t.value.dashboard.days90 },
])

const recentItems = [
  { name: 'main.py', ext: '.py', score: 85, grade: 'B', color: '#00f5ff' },
  { name: 'utils.js', ext: '.js', score: 92, grade: 'A', color: '#00ff88' },
  { name: 'app.ts', ext: '.ts', score: 78, grade: 'C', color: '#ffaa00' },
  { name: 'server.go', ext: '.go', score: 88, grade: 'B', color: '#7b2ff7' },
  { name: 'lib.rs', ext: '.rs', score: 95, grade: 'A', color: '#00ff88' }
]

const trendData = {
  '7d':  [80, 83, 81, 86, 84, 87, 85],
  '30d': [72, 75, 78, 80, 79, 83, 82, 85, 84, 86, 85, 88, 87, 85, 89, 88, 86, 90, 88, 87, 85, 88, 90, 87, 86, 88, 89, 87, 85, 85],
  '90d': [68, 72, 74, 76, 75, 78, 79, 81, 80, 83, 82, 85, 84, 86, 85, 87, 86, 88, 87, 89, 88, 87, 90, 89, 88, 90, 89, 91, 90, 85]
}

let charts = []

const createLine = () => {
  const chart = echarts.init(lineRef.value, null, { renderer: 'canvas' })
  charts.push(chart)
  const data = trendData[activeTab.value]
  const labels = data.map((_, i) => `D-${data.length - 1 - i}`)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(3,7,18,0.9)',
      borderColor: 'rgba(0,245,255,0.3)',
      textStyle: { color: '#e2e8f0' }
    },
    grid: { top: 20, right: 20, bottom: 30, left: 40 },
    xAxis: {
      type: 'category',
      data: labels,
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
      axisTick: { show: false },
      axisLabel: { color: '#64748b', fontSize: 11 }
    },
    yAxis: {
      type: 'value', min: 60, max: 100,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#64748b', fontSize: 11 },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } }
    },
    series: [{
      type: 'line',
      data,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#00f5ff', width: 2, shadowBlur: 10, shadowColor: '#00f5ff' },
      itemStyle: { color: '#00f5ff', borderColor: '#030712', borderWidth: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0,245,255,0.25)' },
          { offset: 1, color: 'rgba(0,245,255,0)' }
        ])
      }
    }]
  })
  return chart
}

const createPie = () => {
  const chart = echarts.init(pieRef.value, null, { renderer: 'canvas' })
  charts.push(chart)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(3,7,18,0.9)',
      borderColor: 'rgba(0,245,255,0.3)',
      textStyle: { color: '#e2e8f0' }
    },
    legend: { orient: 'vertical', right: 10, top: 'center', textStyle: { color: '#64748b' } },
    series: [{
      name: t.value.dashboard.issues,
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['40%', '50%'],
      data: [
        { value: 12, name: t.value.dashboard.error,   itemStyle: { color: '#ff006e', shadowBlur: 15, shadowColor: '#ff006e' } },
        { value: 8,  name: t.value.dashboard.warning, itemStyle: { color: '#ffaa00', shadowBlur: 15, shadowColor: '#ffaa00' } },
        { value: 3,  name: t.value.dashboard.info,    itemStyle: { color: '#00f5ff', shadowBlur: 15, shadowColor: '#00f5ff' } }
      ],
      label: { show: false },
      emphasis: { scale: true, scaleSize: 6 }
    }]
  })
  return chart
}

const createRadar = () => {
  const chart = echarts.init(radarRef.value, null, { renderer: 'canvas' })
  charts.push(chart)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { backgroundColor: 'rgba(3,7,18,0.9)', borderColor: 'rgba(0,245,255,0.3)', textStyle: { color: '#e2e8f0' } },
    radar: {
      indicator: [
        { name: t.value.dashboard.maintainability, max: 100 },
        { name: t.value.dashboard.readability,     max: 100 },
        { name: t.value.dashboard.security,        max: 100 },
        { name: t.value.dashboard.performance,     max: 100 },
        { name: t.value.dashboard.testability,     max: 100 },
        { name: t.value.dashboard.documentation,   max: 100 }
      ],
      center: ['50%', '52%'],
      radius: '65%',
      axisName: { color: '#64748b', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
      splitArea: { areaStyle: { color: ['rgba(255,255,255,0.01)', 'rgba(255,255,255,0.02)'] } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [80, 85, 90, 85, 70, 75],
        name: t.value.dashboard.radar,
        lineStyle: { color: '#00ff88', width: 2, shadowBlur: 8, shadowColor: '#00ff88' },
        areaStyle: { color: 'rgba(0,255,136,0.1)' },
        itemStyle: { color: '#00ff88' }
      }]
    }]
  })
  return chart
}

let lineChart

watch(activeTab, () => {
  if (lineChart) {
    const data = trendData[activeTab.value]
    const labels = data.map((_, i) => `D-${data.length - 1 - i}`)
    lineChart.setOption({ xAxis: { data: labels }, series: [{ data }] })
  }
})

// 语言切换时重绘图表
watch(t, () => {
  charts.forEach(c => c.dispose())
  charts = []
  lineChart = createLine()
  createPie()
  createRadar()
})

const onResize = () => charts.forEach(c => c.resize())

onMounted(() => {
  lineChart = createLine()
  createPie()
  createRadar()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  charts.forEach(c => c.dispose())
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 20px; }

/* 指标卡 */
.metrics-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.metric-card {
  position: relative;
  padding: 20px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  gap: 14px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: default;
}
.metric-card:hover {
  border-color: rgba(var(--accent-rgb), 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(var(--accent-rgb), 0.12);
}
.metric-bg-glow {
  position: absolute;
  top: -40px; right: -40px;
  width: 100px; height: 100px;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.15) 0%, transparent 70%);
  pointer-events: none;
}
.metric-border-top {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}
.metric-card:hover .metric-border-top { opacity: 1; }
.metric-icon { width: 40px; height: 40px; color: var(--accent); flex-shrink: 0; }
.metric-icon :deep(svg) { width: 100%; height: 100%; filter: drop-shadow(0 0 6px var(--accent)); }
.metric-body { flex: 1; }
.metric-value { display: flex; align-items: baseline; gap: 4px; }
.metric-num { font-size: 28px; font-weight: 700; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
.metric-unit { font-size: 12px; color: var(--text-secondary); }
.metric-label { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
.metric-trend {
  display: flex; align-items: center; gap: 3px;
  font-size: 11px; font-weight: 600;
  padding: 3px 8px; border-radius: 20px;
}
.metric-trend svg { width: 12px; height: 12px; }
.metric-trend.up { color: #00ff88; background: rgba(0,255,136,0.1); }
.metric-trend.down { color: #ff006e; background: rgba(255,0,110,0.1); }

/* 图表卡片 */
.charts-row, .bottom-row { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
.chart-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  padding: 20px;
  overflow: hidden;
}
.chart-card.wide { /* handled by grid */ }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.card-title { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--text-primary); letter-spacing: 0.03em; }
.card-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 8px var(--cyan); flex-shrink: 0; }
.card-dot.pink { background: var(--pink); box-shadow: 0 0 8px var(--pink); }
.card-dot.green { background: var(--green); box-shadow: 0 0 8px var(--green); }
.card-dot.purple { background: var(--purple); box-shadow: 0 0 8px var(--purple); }
.chart-area { height: 220px; }
.card-tabs { display: flex; gap: 4px; }
.tab-btn { padding: 4px 10px; border-radius: 6px; border: 1px solid var(--border); background: transparent; color: var(--text-secondary); font-size: 12px; cursor: pointer; transition: all 0.2s; }
.tab-btn:hover { color: var(--text-primary); border-color: rgba(0,245,255,0.3); }
.tab-btn.active { color: var(--cyan); background: rgba(0,245,255,0.08); border-color: rgba(0,245,255,0.3); }

/* 最近记录 */
.recent-list { display: flex; flex-direction: column; gap: 14px; padding-top: 4px; }
.recent-item { display: grid; grid-template-columns: 140px 1fr 36px 32px; align-items: center; gap: 12px; }
.recent-file { display: flex; align-items: center; gap: 6px; }
.file-ext { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; }
.file-name { font-size: 13px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.recent-bar-wrap { height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.recent-bar { height: 100%; border-radius: 2px; transition: width 1s cubic-bezier(0.4,0,0.2,1); }
.recent-score { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; text-align: right; }
.recent-grade { font-size: 11px; font-weight: 700; text-align: center; border: 1px solid; border-radius: 4px; padding: 1px 4px; }
</style>
