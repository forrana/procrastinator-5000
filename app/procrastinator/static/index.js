var app = new Vue({
  el: '#app',
  data: {
    selectedCategory: ""
  },
  methods: {
    selectCategory: function (category) {
      this.selectedCategory = category
    }
  }
})