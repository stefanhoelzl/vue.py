
        Vue.component('native', {
          template: '<div id="content">{{ message }}</div>',
          computed: {
            message () {
              return this.$store.state.message
            }
          }
        });
    