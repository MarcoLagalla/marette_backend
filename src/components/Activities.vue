<template>
     <div class="row">
            <div class="col-md-4 mb-5">
                <div class="card h-100">
                    <img class="card-img-top" src="http://placehold.it/300x200" alt="">
                    <div class="card-body">
                        <h4 class="card-title">{{ nome }}</h4>
                        <p class="card-text">{{card_text}}</p>
                    </div>
                    <div class="card-footer">
                        <router-link v-bind:to='"/" + nome' class="btn btn-primary">Entra nel negozio</router-link >
                    </div>
                </div>
            </div>
     </div>
</template>

<script>
    export default {
        name: "Activities",
        props: ['nome', 'card_text'],
        data () {
            return {

            }
        }
    }
</script>

<style scoped>

</style>