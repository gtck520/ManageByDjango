import Vue from 'vue'
import App from './App'
import common from './common/common.js'
Vue.config.productionTip = false
Vue.prototype.ApiHost='http://127.0.0.1:8000/';
Vue.use(common)
App.mpType = 'app'

const app = new Vue({
    ...App
})
app.$mount()
