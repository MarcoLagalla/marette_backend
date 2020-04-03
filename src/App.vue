<template>
    <div id="app">
        <!-- Navigation -->
        <navigation></navigation>
        <!-- Menu -->
        <app-menu></app-menu>
        <!-- Header -->
        <app-header></app-header>
        <!-- Page Content -->
        <page-content></page-content>

        <!-- Footer -->
        <app-footer></app-footer>
    </div>
</template>

<script>
    import Navigation from './components/Navigation'
    import Header from './components/Header'
    import Footer from './components/Footer'
    import Menu from './components/Menu'
    import PageContent from './components/PageContent'
    export default {
        components: {
            'navigation': Navigation,
            'app-header': Header,
            'app-footer': Footer,
            'app-menu': Menu,
            'pageContent': PageContent,
        }
    }
</script>

<style>

</style>
