import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueResource from 'vue-resource'
import axios from "axios";
const app = createApp(App);
axios.defaults.headers.post['Content-Type'] = 'application/json';
app.config.globalProperties.$http = axios;


import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
 
import 'element-plus/theme-chalk/index.css'
// import locale from 'element-plus/lib/locale/lang/zh-cn'

// Vue.config.productionTip = true;
app.use(ElementPlus)
app.use(router).mount('#app');
