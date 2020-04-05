<template>
<div class="container">
    <div class="row">
        <div class="col-md-6 mb-5">
            <h2>Per i clienti</h2>
            <hr>
            <p>Qua spieghiamo come funziona il nostro sito per i clienti</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Omnis optio neque consectetur consequatur magni in nisi, natus beatae quidem quam odit commodi ducimus totam eum, alias, adipisci nesciunt voluptate. Voluptatum.</p>
            <a class="btn btn-primary btn-lg" href="#">Iscriviti &raquo;</a>
        </div>
        <div class="col-md-6 mb-5">
            <h2>Per le aziende</h2>
            <hr>
            <p>Qua scriviamo cosa facciamo e cosa forniamo ai negozi/aziende che si affidano a noi</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Omnis optio neque consectetur consequatur magni in nisi, natus beatae quidem quam odit commodi ducimus totam eum, alias, adipisci nesciunt voluptate. Voluptatum.</p>
            <a class="btn btn-primary btn-lg" href="#">Apri un negozio &raquo;</a>
        </div>
    </div>
    <!-- /.row -->
    <h1>Negozi</h1>
    <hr>
    <activities v-for="prova in prove" v-bind:nome="prova.nome" v-bind:card_text="prova.card_text"></activities>

</div>
</template>

<script>
    import Activities from './Activities'

    export default {
        name: "PageContent",
        components: {
            'activities': Activities
        },
        data () {
            return {
                prove: [
                    {
                         nome:'bouvette',
                        card_text: 'questo è un testo a caso che ho scritto io'
                    },
                    {
                         nome:'hjasdfhijblasdfhiljk',
                        card_text: 'Mayiudsicuhgolijkdhafsg'
                    },
                    {
                         nome:'Urca',
                        card_text: 'questo è un altro messaggio'
                    }
                ],



            }
        }
    }
</script>

<style scoped>

</style>