import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/tasks/:id',
    name: 'Task',
    component: () => import(/* webpackChunkName: "hint" */ '@/views/Task.vue')
  },
  {
    path: '/:id',
    name: 'ContenstHome',
    component: () => import(/* webpackChunkName: "contest_home" */ '@/views/ContestHome.vue')
  },
  {
    path: '/:contestId/teams/:id',
    name: 'TeamHome',
    component: () => import(/* webpackChunkName: "team_home" */ '@/views/TeamHome.vue')
  },
  {
    path: '/hints/:id',
    name: 'Hint',
    component: () => import(/* webpackChunkName: "hint" */ '@/views/Hint.vue')
  },
  {
    path: '/:contestId/questions/:id',
    name: 'Question',
    component: () => import(/* webpackChunkName: "hint" */ '@/views/Question.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
