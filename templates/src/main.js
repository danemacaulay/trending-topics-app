import './assets/favicon.png'
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import VueMasonry from 'vue-masonry-css'
import 'bootstrap-css-only/css/bootstrap.css'
import 'open-iconic/font/css/open-iconic-bootstrap.css'

Vue.use(VueMasonry);
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'tweetList',
      component: App,
      query: {page: 'page'}
    },
  ],
})

new Vue({
  router: router
}).$mount('#app')

