var app = new Vue({
  el: '#app',
  data: {
    selectedActivity: ""
  },
  methods: {
    selectActivity: function (activity) {
      this.selectedActivity = activity
    }
  }
})
