<template>
  <div class="row">
    <div class="col-12">
      <h3>
        Community Create
      </h3>

      <form @submit.prevent="callCreate" id="createForm">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" name="name" id="name" class="form-control">
        </div>

        <div class="form-group">
          <label for="slug">Slug</label> <b-button size="sm" variant="outline-primary" @click="generateSlug()">Generate Slug</b-button>
          <input type="text" name="slug" id="slug" class="form-control">
        </div>

        <div class="form-group">
          <label>Members</label>
          <span v-for="(member, index) in members" :key="index" class="badge badge-secondary mx-1 mb-1">
            {{ member.username }}
            <button type="button" class="btn btn-outline-dark btn-sm" aria-label="Close" @click="removeMember(index)">
              <span aria-hidden="true">&times;</span>
            </button>
            <input type="hidden" v-model="members[index]">
          </span>

          <AutoComplete :api="autocompleteMembers" :prop-to-show="'username'" :function-after="autocompleteMembersAfter" />
        </div>

        <div class="form-group">
          <label for="detail">Detail</label>
          <textarea name="detail" id="detail" class="form-control"></textarea>
        </div>

        <button type="submit" class="btn btn-primary">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
  import AutoComplete from '../Layout/AutoComplete';
  import { getAPI } from '../../api/axios-base';
  import strToSlug from '../../utils/strToSlug.js';
  import { URL_API_COMMUNITY_CREATE, URL_API_USER_LIST } from '../../constants.js';
  import { mapState } from 'vuex';

  export default {
    name: 'community-create',
    components: {
      AutoComplete,
    },
    mixins: [
      strToSlug,
    ],
    computed: mapState(['currentUser']),

    data() {
      return {
        members: undefined,
      }
    },

    methods: {

      // MEMBERS
        autocompleteMembers(username) {
          let query = {};
            query.username = username;

          query.not_in_username = [];
          query.not_in_username.push(this.currentUser.username);
          if (Array.isArray(this.members))
            query.not_in_username = query.not_in_username.concat(this.members.map(({ username }) => username))

          return getAPI.get(URL_API_USER_LIST, {
            params: query
          });
        },

        autocompleteMembersAfter(selected) {
          if (selected) {
            if (this.members === undefined)
              this.members = [];
            this.members.push(selected);
          }
        },

        removeMember(index) {
          if (this.members[index] !== undefined) {
            this.members.splice(index, 1);
          }
        },
      // -- MEMBERS

      generateSlug() {
        if (document.getElementById('name') && document.getElementById('name').value) {
          document.getElementById('slug').value = this.strToSlug(document.getElementById('name').value);
        }
      },

      callCreate() {
        let formData = new FormData(document.getElementById('createForm'));
        for (let index = 0; index < this.members.length; index++) {
          formData.append('members', this.members[index].username);
        }

        getAPI.post(URL_API_COMMUNITY_CREATE, formData)
          .then((response) => {
            this.$root.$bvToast.toast(`Community "${response.data.name}" was successfully created.`, {
              title: 'Success',
              variant: 'success',
              solid: true
            });
            this.$store.dispatch('updateLocalCurrentUser');
            this.$router.push({ name: 'community-list' });
          })
          .catch(e => {
            this.$bvToast.toast(e.response.data.detail, {
              title: 'Error',
              variant: 'danger',
              solid: true
            });
          });
      }
    }
  };
</script>

<style>
</style>