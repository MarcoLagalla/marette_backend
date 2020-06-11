<template>
    <div class="body" id="CONTATTI">
<div  class="contattaci">
    <base-rest-h1> Info </base-rest-h1>
    <base-rest-info > </base-rest-info>
</div>
    </div>
</template>
<script>
export default {
    name:'restinfo',
    created() {
        this.$store.dispatch("restaurants/getUserRestaurants")
    }
}
</script>
<style scoped>
.contattaci {
    margin: auto;
    width: 100%;
}

.body {
    background: var(--whitesmoke);
}
</style>