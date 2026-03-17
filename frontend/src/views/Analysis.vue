<template>
  <div class="analysis">
    <el-card>
      <template #header>
        <span>代码分析</span>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="上传文件" name="upload">
          <el-upload
            class="upload-area"
            drag
            action="/api/v1/analysis/upload"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept=".py,.js,.ts,.java,.go,.rs"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 Python, JavaScript, TypeScript, Java, Go, Rust 文件
              </div>
            </template>
          </el-upload>
        </el-tab-pane>
        
        <el-tab-pane label="分析路径" name="path">
          <el-form :model="pathForm" label-width="80px">
            <el-form-item label="文件路径">
              <el-input 
                v-model="pathForm.filePath" 
                placeholder="/path/to/your/code.py"
                clearable
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="analyzeByPath">
                开始分析
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 分析结果 -->
    <el-card v-if="analysisResult" style="margin-top: 20px;">
      <template #header>
        <span>分析结果 - {{ analysisResult.filename }}</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="score-circle">
            <el-progress
              type="circle"
              :percentage="analysisResult.quality_score.total_score"
              :color="getScoreColor(analysisResult.quality_score.total_score)"
            />
            <div class="score-text">
              {{ analysisResult.quality_score.grade }} 级
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <div class="score-details">
            <h4>各维度得分</h4>
            <div class="dimension-item">
              <span>可维护性:</span>
              <el-progress 
                :percentage="analysisResult.quality_score.dimensions.maintainability" 
                :stroke-width="8"
              />
            </div>
            <div class="dimension-item">
              <span>可读性:</span>
              <el-progress 
                :percentage="analysisResult.quality_score.dimensions.readability" 
                :stroke-width="8"
              />
            </div>
            <div class="dimension-item">
              <span>安全性:</span>
              <el-progress 
                :percentage="analysisResult.quality_score.dimensions.security" 
                :stroke-width="8"
              />
            </div>
            <div class="dimension-item">
              <span>性能:</span>
              <el-progress 
                :percentage="analysisResult.quality_score.dimensions.performance" 
                :stroke-width="8"
              />
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- 问题列表 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>发现问题 ({{ analysisResult.analysis.issues.length }})</span>
        </template>
        <el-table :data="analysisResult.analysis.issues" stripe>
          <el-table-column prop="line" label="行号" width="80"/>
          <el-table-column prop="type" label="类型" width="80">
            <template #default="scope">
              <el-tag :type="getIssueTagType(scope.row.type)">{{ scope.row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="问题描述"/>
          <el-table-column prop="suggestion" label="建议"/>
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const activeTab = ref('upload')
const analysisResult = ref(null)
const pathForm = ref({ filePath: '' })

const beforeUpload = (file) => {
  const validTypes = ['.py', '.js', '.ts', '.java', '.go', '.rs']
  const fileExt = '.' + file.name.split('.').pop().toLowerCase()
  if (!validTypes.includes(fileExt)) {
    ElMessage.error('不支持的文件类型！')
    return false
  }
  return true
}

const handleUploadSuccess = (response) => {
  if (response.success) {
    analysisResult.value = response
    ElMessage.success('分析完成！')
  } else {
    ElMessage.error('分析失败：' + response.message)
  }
}

const analyzeByPath = () => {
  if (!pathForm.value.filePath) {
    ElMessage.warning('请输入文件路径')
    return
  }
  // 模拟分析结果
  analysisResult.value = {
    filename: pathForm.value.filePath.split('/').pop(),
    analysis: {
      issues: [
        { line: 10, type: 'error', message: '发现硬编码密码', suggestion: '使用环境变量' },
        { line: 25, type: 'warning', message: '函数过长', suggestion: '拆分为小函数' }
      ]
    },
    quality_score: {
      total_score: 85,
      grade: 'B',
      dimensions: {
        maintainability: 80,
        readability: 85,
        security: 90,
        performance: 85
      }
    }
  }
  ElMessage.success('分析完成！')
}

const getScoreColor = (score) => {
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#409eff'
  if (score >= 70) return '#e6a23c'
  return '#f56c6c'
}

const getIssueTagType = (type) => {
  const map = { error: 'danger', warning: 'warning', info: 'info' }
  return map[type] || 'info'
}
</script>

<style scoped>
.analysis {
  padding: 20px;
}

.upload-area {
  text-align: center;
}

.score-circle {
  text-align: center;
}

.score-text {
  margin-top: 10px;
  font-weight: bold;
  font-size: 18px;
}

.score-details h4 {
  margin-bottom: 15px;
}

.dimension-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.dimension-item span {
  width: 80px;
  font-size: 14px;
}
</style>