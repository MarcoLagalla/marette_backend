<template>
    <div>
        <input type="checkbox" id="nav-toggle" hidden>
        <!--
        Panello uscente posizioniamo sotto il checkbox, ma non obbligatoriamente subito sotto, posiamo metterlo anche in fondo della pagina
        -->
        <nav class="nav">
            <label for="nav-toggle" class="nav-toggle" onclick></label>
            <!--
        Qui posiamo mettere qualsiasi contenuto nel nostro caso un menu realizzato in base del elenco non numerato <ul>
        -->
            <h2 class="logo"> Marette
            </h2>
            <ul>
                <li><a href="#1">Uno </a></li>
                <li><a href="#2">Due</a></li>
                <li><a href="#3">Tre</a></li>
                <li><a href="#4">Quattro</a></li>
            </ul>
        </nav>
        </div>
</template>

<script>
    export default {
        name: "Menu"
    }
</script>

<style scoped>

</style>