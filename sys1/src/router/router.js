const routes = [
    {
        name: 'home',
        path: '/home',
        component: () => import('@/view/Home')
    },
    //重定向，定位至首页
    {
        path: "/",
        redirect: "/home"
    },
    
];

export default routes
