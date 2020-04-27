<template>
  <div>
  <router-link v-for="(name, i) in items" :key="i" :to="'#'+name" class="li" :ripple="false"
            min-width="96" type="button">{{ name }}</router-link>
    </div>
</template>

<script>
    export default {
        name: "RestMenu",
        props: ['items']
    }
</script>

<style scoped>
</style>