import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import Files from '../components/Files.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [ // verschiedene Pfade/Routes auf der Website
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/files',
      name: 'Files',
      component: Files
    },
    {
      path: '/impressum',
      name: 'Impressum',
      component: () => import('../components/Impressum.vue') // impressum wird nur geladen, wenn besucht
    }
  ]
})

export default router
