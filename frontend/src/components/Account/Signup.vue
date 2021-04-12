<template>
  <div>
    <h3>Signup</h3>

    <form @submit.prevent="signupUser">
      <div class="form-group">
        <label for="el">Email</label>
        <input type="email" name="el" id="el" class="form-control" v-model="form.email">
      </div>

      <div class="form-group">
        <label for="ur">Username</label>
        <input type="text" name="ur" id="ur" class="form-control" v-model="form.username">
      </div>

      <div class="form-group">
        <label for="pwr">Password</label>
        <input type="password" name="pwr" id="pwr" class="form-control" v-model="form.password">
      </div>

      <div class="form-group">
        <label for="pass">Password Confirmation</label>
        <input type="password" name="pass" id="pass" class="form-control" v-model="form.confirm">
      </div>

      <button type="submit" class="btn btn-primary">signup</button>
    </form>
  </div>
</template>

<script>
  export default {
    name: 'signup',
    data () {
      return {
        form: {
          email: '',
          username: '',
          password: '',
          confirm: ''
        }
      }
    },
    methods: {
      signupUser () {
        this.$store.dispatch('signupUser', this.form)
          .then(() => {
            this.$router.push({ name: 'login' })
          });
      }
    }
  }
</script>