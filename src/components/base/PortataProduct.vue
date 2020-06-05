<template>
    <v-tooltip v-model="show" top color="rgba(0,0,0,0)">
        <template v-slot:activator="{ on }">
            <div class="products" v-on="on">


                    <div class="inputGroup">
                        <input :id="product.name" name="product.name" type="checkbox"/>
                        <label :for="product.name"><div class="title" v-text="product.name"></div></label>
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


    .inputGroup {
        background-color: #fff;
        display: block;
        margin: 10px 0;
        position: relative;
        box-shadow: 0 0 2px lightgrey;
    }
    .inputGroup label {
        padding: 12px 30px;
        width: 100%;
        display: block;
        text-align: left;
        color: #3C454C;
        cursor: pointer;
        position: relative;
        z-index: 2;
        -webkit-transition: color 200ms ease-in;
        transition: color 200ms ease-in;
        overflow: hidden;
    }
    .inputGroup label:before {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        content: '';
        background-color: var(--emerald);
        position: absolute;
        left: 50%;
        top: 50%;
        -webkit-transform: translate(-50%, -50%) scale3d(1, 1, 1);
        transform: translate(-50%, -50%) scale3d(1, 1, 1);
        -webkit-transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
        transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
        z-index: -1;
    }
    .inputGroup label:after {
        width: 32px;
        height: 32px;
        content: '';
        border: 2px solid #D1D7DC;
        background-color: #fff;
        background-image: url("data:image/svg+xml,%3Csvg width='32' height='32' viewBox='0 0 32 32' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5.414 11L4 12.414l5.414 5.414L20.828 6.414 19.414 5l-10 10z' fill='%23fff' fill-rule='nonzero'/%3E%3C/svg%3E ");
        background-repeat: no-repeat;
        background-position: 2px 3px;
        border-radius: 50%;
        z-index: 2;
        position: absolute;
        right: 30px;
        top: 50%;
        -webkit-transform: translateY(-50%);
        transform: translateY(-50%);
        cursor: pointer;
        -webkit-transition: all 200ms ease-in;
        transition: all 200ms ease-in;
    }
    .inputGroup input:checked ~ label {
        color: #fff;
    }
    .inputGroup input:checked ~ label:before {
        -webkit-transform: translate(-50%, -50%) scale3d(56, 56, 1);
        transform: translate(-50%, -50%) scale3d(56, 56, 1);
        opacity: 1;
    }
    .inputGroup input:checked ~ label:after {
        background-color: var(--ming);
        border-color: var(--ming);
    }
    .inputGroup input {
        width: 32px;
        height: 32px;
        -webkit-box-ordinal-group: 2;
        order: 1;
        z-index: 2;
        position: absolute;
        right: 30px;
        top: 50%;
        -webkit-transform: translateY(-50%);
        transform: translateY(-50%);
        cursor: pointer;
        visibility: hidden;
    }


</style>