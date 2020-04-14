<template>
    <div>
        <router-link tag="button" v-if="business">Aggiungi ristorante</router-link>

    </div>
</template>

<script>
    //import { mapActions } from 'vuex'
    export default {
        name: "Profile",
        data () {
            return {
                business: true
            }
        },
        methods:
        {
            //...mapActions('userAuthentication', ['signIn']),

        },
        computed:
        {

        }
    }
</script>

<style scoped>

</style>
