/* eslint-disable no-unused-vars */

const state = {
  FOOD_CATEGORY_CHOICES : [
        'Altro',
        'Antipasto',
        'Primo',
        'Secondo',
        'Contorno',
        'Dessert',
        'Caffetteria',
        'Panetteria',
        'Panini e Piadine',
        'Pizza',
        'Secondo',
        'Snack',
    ],

    DISCOUNT_TYPE_CHOICE: [
        'Fisso',
        'Percentuale'
    ],

}

const getters = {
    food_category_choice: state => state.food_category_choice,
    discount_type_choice: state => state.discount_type_choice,
}

const actions = {

}

const mutations = {

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}