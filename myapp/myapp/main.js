import Vue from 'vue'
import App from './App'
import api from '@/common/vmeitime-http/'


import cuCustom from './colorui/components/cu-custom.vue'
Vue.component('cu-custom',cuCustom)

Vue.config.productionTip = false
// 全局挂载后使用数据接口
Vue.prototype.$api = api

import store from './store/index.js' //状态管理
Vue.prototype.$store = store

Vue.config.productionTip = false

App.mpType = 'app'

const app = new Vue({
	store,
    ...App
})
app.$mount()
