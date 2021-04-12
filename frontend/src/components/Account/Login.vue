<template>
  <div>
    <h3>Login</h3>

    <h5 v-if="wrongCred">Wrong credentials entered!. Please enter your correct details.</h5>
    <form v-on:submit.prevent="loginUser">
      <div class="form-group">
        <label for="user">Email</label>
        <input type="email" name="email" id="user" class="form-control" v-model="form.email">
      </div>

      <div class="form-group">
        <label for="pass">Password</label>
        <input type="password" name="password" id="pass" class="form-control" v-model="form.password">
      </div>

      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script>
  export default {
    name: 'login',
    data () {
      return {
        form: {
          email: '',
          password: '',
        },
        wrongCred: false // activates appropriate message if set to true
      }
    },
    methods: {
      loginUser () { // call loginUSer action
        this.$store.dispatch('loginUser', this.form)
          .then(() => {
            this.wrongCred = false
            this.$router.push({ name: 'home' })
          })
        .catch(err => {
          console.log(err)
          this.wrongCred = true // if the credentials were wrong set wrongCred to true
        });
      }
    }
  }
</script>