<template>
  <div class="reports">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>分析报告</span>
          <el-button type="primary" @click="exportReport">
            导出报告
          </el-button>
        </div>
      </template>
      
      <el-table :data="reports" stripe style="width: 100%">
        <el-table-column prop="filename" label="文件名" width="200"/>
        <el-table-column prop="date" label="分析日期" width="150"/>
        <el-table-column prop="score" label="质量分数" width="100">
          <template #default="scope">
            <el-tag :type="getScoreTagType(scope.row.score)">
              {{ scope.row.score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="等级" width="80">
          <template #default="scope">
            <el-tag :type="getGradeTagType(scope.row.grade)">
              {{ scope.row.grade }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="issues" label="问题数" width="80"/>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已完成' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="viewReport(scope.row)">
              查看
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteReport(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalReports"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const currentPage = ref(1)
const pageSize = ref(10)
const totalReports = ref(25)

const reports = ref([
  { id: 1, filename: 'main.py', date: '2024-03-17', score: 85, grade: 'B', issues: 3, status: '已完成' },
  { id: 2, filename: 'utils.js', date: '2024-03-16', score: 92, grade: 'A', issues: 1, status: '已完成' },
  { id: 3, filename: 'app.ts', date: '2024-03-15', score: 78, grade: 'C', issues: 8, status: '已完成' },
  { id: 4, filename: 'server.go', date: '2024-03-14', score: 88, grade: 'B', issues: 2, status: '已完成' },
  { id: 5, filename: 'lib.rs', date: '2024-03-13', score: 95, grade: 'A', issues: 0, status: '已完成' }
])

const getScoreTagType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  return 'danger'
}

const getGradeTagType = (grade) => {
  const map = { 'A': 'success', 'B': 'primary', 'C': 'warning', 'D': 'danger', 'F': 'danger' }
  return map[grade] || 'info'
}

const viewReport = (report) => {
  ElMessage.info(`查看报告: ${report.filename}`)
}

const deleteReport = (report) => {
  ElMessageBox.confirm(`确定删除报告 