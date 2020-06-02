<template>
    <v-tooltip v-model="show" top color="rgba(0,0,0,0)">
        <template v-slot:activator="{ on }">
            <div class="products" v-on="on">
                <div class="title" v-text="product.name"></div>
                <div class="buttons">
                   <input type="checkbox"><label></label>
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
    /*Checkboxes styles*/
    input[type="checkbox"] { display: none; }

    input[type="checkbox"] + label {
        display: block;
        position: relative;
        padding-left: 35px;
        margin-bottom: 20px;
        font: 14px/20px 'Open Sans', Arial, sans-serif;
        color: #ddd;
        cursor: pointer;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }

    input[type="checkbox"] + label:last-child { margin-bottom: 0; }

    input[type="checkbox"] + label:before {
        content: '';
        display: block;
        width: 20px;
        height: 20px;
        border: 1px solid #6cc0e5;
        position: absolute;
        left: 0;
        top: 0;
        opacity: .6;
        -webkit-transition: all .12s, border-color .08s;
        transition: all .12s, border-color .08s;
    }

    input[type="checkbox"]:checked + label:before {
        width: 10px;
        top: -5px;
        left: 5px;
        border-radius: 0;
        opacity: 1;
        border-top-color: transparent;
        border-left-color: transparent;
        -webkit-transform: rotate(45deg);
        transform: rotate(45deg);
    }
</style>