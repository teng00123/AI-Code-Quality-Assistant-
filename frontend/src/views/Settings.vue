<template>
  <div class="settings">
    <el-card>
      <template #header>
        <span>系统设置</span>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="通用设置" name="general">
          <el-form :model="generalSettings" label-width="150px">
            <el-form-item label="默认语言">
              <el-select v-model="generalSettings.language">
                <el-option label="中文" value="zh-CN"/>
                <el-option label="English" value="en-US"/>
              </el-select>
            </el-form-item>
            
            <el-form-item label="主题模式">
              <el-radio-group v-model="generalSettings.theme">
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
                <el-radio label="auto">自动</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="自动刷新间隔(秒)">
              <el-input-number 
                v-model="generalSettings.refreshInterval" 
                :min="30" 
                :max="3600"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="API设置" name="api">
          <el-form :model="apiSettings" label-width="150px">
            <el-form-item label="后端API地址">
              <el-input v-model="apiSettings.baseURL" placeholder="http://localhost:8000"/>
            </el-form-item>
            
            <el-form-item label="超时时间(毫秒)">
              <el-input-number v-model="apiSettings.timeout" :min="5000" :max="60000"/>
            </el-form-item>
            
            <el-form-item label="启用HTTPS">
              <el-switch v-model="apiSettings.httpsEnabled"/>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="通知设置" name="notifications">
          <el-form :model="notificationSettings" label-width="150px">
            <el-form-item label="分析完成通知">
              <el-switch v-model="notificationSettings.analysisComplete"/>
            </el-form-item>
            
            <el-form-item label="新问题提醒">
              <el-switch v-model="notificationSettings.newIssues"/>
            </el-form-item>
            
            <el-form-item label="质量下降告警">
              <el-switch v-model="notificationSettings.qualityDrop"/>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      
      <div class="form-actions">
        <el-button type="primary" @click="saveSettings">
          保存设置
        </el-button>
        <el-button @click="resetSettings">
          重置
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('general')

const generalSettings = ref({
  language: 'zh-CN',
  theme: 'light',
  refreshInterval: 60
})

const apiSettings = ref({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  httpsEnabled: false
})

const notificationSettings = ref({
  analysisComplete: true,
  newIssues: true,
  qualityDrop: true
})

const saveSettings = () => {
  ElMessage.success('设置已保存')
  console.log('保存设置:', {
    generalSettings: generalSettings.value,
    apiSettings: apiSettings.value,
    notificationSettings: notificationSettings.value
  })
}

const resetSettings = () => {
  ElMessage.info('设置已重置为默认值')
}
</script>

<style scoped>
.settings {
  padding: 20px;
}

.form-actions {
  margin-top: 20px;
  text-align: right;
}
</style>