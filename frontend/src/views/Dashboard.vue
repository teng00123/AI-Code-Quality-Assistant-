<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-value">85.2</div>
          <div class="metric-label">平均质量分数</div>
          <div class="metric-unit">/ 100</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-value">127</div>
          <div class="metric-label">分析文件数</div>
          <div class="metric-unit">总计</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-value">23</div>
          <div class="metric-label">发现问题</div>
          <div class="metric-unit">需关注</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card">
          <div class="metric-value">92%</div>
          <div class="metric-label">代码覆盖率</div>
          <div class="metric-unit">良好</div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>质量趋势</span>
          </template>
          <div ref="chartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>问题分布</span>
          </template>
          <div ref="pieRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
const pieRef = ref(null)

onMounted(() => {
  // 趋势图
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    title: { text: '质量分数趋势' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [{
      name: '平均分',
      type: 'line',
      data: [78, 82, 85, 83, 87, 85],
      smooth: true
    }]
  })
  
  // 饼图
  const pie = echarts.init(pieRef.value)
  pie.setOption({
    title: { text: '问题类型分布' },
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [{
      name: '问题',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 12, name: '错误' },
        { value: 8, name: '警告' },
        { value: 3, name: '信息' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  })
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.metric-card {
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.metric-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 14px;
  opacity: 0.9;
}

.metric-unit {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 5px;
}
</style>