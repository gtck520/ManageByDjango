import Vue from 'vue'
import App from './App'
import api from '@/common/vmeitime-http/'


import cuCustom from './colorui/components/cu-custom.vue'
Vue.component('cu-custom',cuCustom)

Vue.config.productionTip = false
// 全局挂载后使用数据接口
Vue.prototype.$api = api

App.mpType = 'app'

const app = new Vue({
    ...App
})
app.$mount()
