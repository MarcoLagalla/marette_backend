<template>
    <v-tooltip v-model="show" top color="rgba(0,0,0,0)">
        <template v-slot:activator="{ on }">
            <div class="products" v-on="on">
                <div class="title" v-text="product.name"></div>
                <div class="buttons">
                    <button class="select"><i class="fas fa-cart-arrow-down"></i></button>

                </div>
            </div>
        </template>
        <v-card color="var(--ming)" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
                <div class="quant">
                    <div class>
                        <v-avatar class="ma-3" size="100" tile>
                            <v-img :src="product.image"></v-img>
                        </v-avatar>
                    </div>
                    <div class>
                        <v-card-title class="prodtitle" v-text="product.name"></v-card-title>
                        <v-card-subtitle class="pb-0" v-text="product.category"></v-card-subtitle>
                        <div class="description" v-text="product.description"></div>
                    </div>
                </div>
                <div class="pos2" v-for="(item, j) in product.tags" :key="j" v-text="item.name"></div>
            </div>
        </v-card>
    </v-tooltip>
</template>

<script>
    export default {
        name: "Product",
        data() {
            return {
                show: false,
            }
        },
        props: {
            product: {
                type: Object,
                required: true
            },
            delete: {
                type: Boolean,
                required: false,
                default: false
            },
            basket: {
                type: Boolean,
                required: false,
                default: false
            },
            edit: {
                type: Boolean,
                required: false,
                default: false
            },
            price: {
                type: Boolean,
                required: false,
                default: false
            },
        },
        methods: {}
    }
</script>

<style scoped>
    .products {
        position: relative;
        width: 100%;
        height: 50px;
        display: flex;
       box-shadow: 0 0 4px var(--lightgrey);
        padding: 10px;
        transition: ease-in-out 0.3s;
    }
    .products:hover {
        box-shadow: 0 0 10px var(--ming);
    }

    .buttons {
        position: absolute;
        right: 0;

    }
    i{
        margin-right: 10px;
    }

    .title {
        text-transform: capitalize;
    }

    h1 {
        color: white;
        margin-bottom: 10px;
        margin-left: 10px;
    }

    .prodtitle {
        font-size: 1.2em;
        text-transform: capitalize;
    }

    .quant {
        padding: 5px;
        display: flex;
        align-items: center;
    }

    .description {
        padding: 15px;
        transition: ease-in-out 0.3s;
        margin-bottom: 10px;
    }

    .product {
        transition: ease-in-out 0.4s;
        margin: 0 !important;
        padding: 0 !important;
        width: 40vmax;
    }

    .product:hover {
        box-shadow: 0 0 10px black;
    }
</style>