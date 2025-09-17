import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import IsRegisted from '@/views/isRegisted.vue'
import IsLogged from '@/views/isLogged.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },
    { path: '/isRegisted', name: 'isRegisted', component: IsRegisted},
    { path: '/isLogged', name: 'isLogged', component: IsLogged}
  ],
})
