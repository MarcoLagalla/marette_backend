<template>
  <div id="login">
    <articles>
      <banner />
    </articles>
    <logform />

    <about />

    <subscribe />

    <social />
  </div>
</template>

<script>
  export default {
    name: 'Login',

    components: {
      Logform: () => import('@/components/Logform'),
      About: () => import('@/components/home/About'),
      //Articles: () => import('@/components/home/Articles'),
      //Banner: () => import('@/components/home/Banner'),
      Social: () => import('@/components/home/Social'),
      Subscribe: () => import('@/components/home/Subscribe')
    }
  }
</script>
