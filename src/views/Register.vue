<template>
  <div id="register">
    <articles>
      <banner />
    </articles>
    <regform />

    <about />

    <subscribe />

    <social />
  </div>
</template>

<script>
  export default {
    name: 'Register',

    components: {
      Regform: () => import('@/components/Regform'),
      About: () => import('@/components/home/About'),
      //Articles: () => import('@/components/home/Articles'),
      //Banner: () => import('@/components/home/Banner'),
      Social: () => import('@/components/home/Social'),
      Subscribe: () => import('@/components/home/Subscribe')
    }
  }
</script>
