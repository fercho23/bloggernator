
import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../components/Home.vue'),
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../components/Account/Login.vue'),
      meta: {
        requiresLogged: true
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../components/Account/Signup.vue'),
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../components/Account/Logout.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/profile/:username?',
      name: 'profile',
      component: () => import('../components/Account/Profile.vue'),
      meta: {
        requiresAuth: true
      },
      props: true
    },
    {
      path: '/profile/:username?/update',
      name: 'profile-update',
      component: () => import('../components/Account/ProfileUpdate.vue'),
      meta: {
        requiresAuth: true
      },
      props: true
    },

    {
      path: '/community/list',
      name: 'community-list',
      component: () => import('../components/Community/CommunityList.vue'),
      props: true
    },
    {
      path: '/community/create',
      name: 'community-create',
      component: () => import('../components/Community/CommunityCreate.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/community/:slug',
      name: 'community-detail',
      component: () => import('../components/Community/CommunityDetail.vue'),
      props: true
    },
    // {
    //   path: '/community/:slug/delete',
    //   name: 'community-delete',
    //   component: () => import('../components/Community/CommunityDelete.vue'),
    //   meta: {
    //     requiresAuth: true
    //   }
    //   props: true
    // },
    {
      path: '/community/:slug/update',
      name: 'community-update',
      component: () => import('../components/Community/CommunityUpdate.vue'),
      meta: {
        requiresAuth: true
      },
      props: true
    },

    {
      path: '/post/list',
      name: 'post-list',
      component: () => import('../components/Post/PostList.vue'),
      props: true
    },
    {
      path: '/post/create',
      name: 'post-create',
      component: () => import('../components/Post/PostCreate.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/post/:slug',
      name: 'post-detail',
      component: () => import('../components/Post/PostDetail.vue'),
      props: true
    },
    // {
    //   path: '/post/:slug/delete',
    //   name: 'post-delete',
    //   component: () => import('../components/Post/PostDelete.vue'),
    //   meta: {
    //     requiresAuth: true
    //   }
    //   props: true
    // },
    {
      path: '/post/:slug/update',
      name: 'post-update',
      component: () => import('../components/Post/PostUpdate.vue'),
      meta: {
        requiresAuth: true
      },
      props: true
    }
  ]
});

export default router;