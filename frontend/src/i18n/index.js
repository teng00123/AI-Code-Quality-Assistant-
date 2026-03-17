import { computed } from 'vue'
import { useSettingsStore } from '../store/settings.js'
import { messages } from './messages.js'

export function useI18n() {
  const settings = useSettingsStore()

  const t = computed(() => {
    const lang = settings.language
    return messages[lang] || messages['zh-CN']
  })

  // 快捷访问：t.value.nav.dashboard
  // 也支持函数调用：$t('nav.dashboard')
  function $t(key) {
    const keys = key.split('.')
    let obj = messages[settings.language] || messages['zh-CN']
    for (const k of keys) {
      obj = obj?.[k]
      if (obj === undefined) return key
    }
    return obj
  }

  return { t, $t }
}
