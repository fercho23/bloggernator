<template>
  <div class="row">
    <div class="col-12">
      <template v-if="community">
        <h3>
          Community Update: <small> {{ community.name }}</small>
        </h3>
        <div class="alert alert-danger" v-if="error">Community Error: {{ error }}</div>

        <form @submit.prevent="callUpdate" id="updateForm">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" name="name" class="form-control" :value="community.name">
          </div>

          <div class="form-group">
            <label for="slug">Slug</label>
            <input type="text" name="slug" class="form-control" :value="community.slug">
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
            <textarea name="detail" class="form-control" :value="community.detail"></textarea>
          </div>

          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </template>
      <template v-else="">
        <div class="alert alert-danger" v-if="error">Community Error: {{ error }}</div>
        <p>Please click on a Community...</p>
      </template>
    </div>
  </div>
</template>

<script>
  import AutoComplete from '../Layout/AutoComplete';
  import { getAPI } from '../../api/axios-base';
  import { URL_API_COMMUNITY_READ, URL_API_COMMUNITY_UPDATE, URL_API_USER_LIST } from '../../constants.js';

  export default {
    name: 'community-update',
    components: {
      AutoComplete
    },
    props: ['community'],
    data() {
      return {
        members: this.community ? this.community.members : undefined,
        error: undefined,
      }
    },

    beforeMount() {
      if (this.community === undefined)
        this.retrieveCommunity(this.$route.params.slug);
    },
    methods: {

      // MEMBERS
        autocompleteMembers(username) {
          let query = {};
            query.username = username;

          query.not_in_username = [];
          query.not_in_username.push(this.community.owner.username);
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

      retrieveCommunity(slug) {
        getAPI.get(URL_API_COMMUNITY_READ.replace(':slug', slug))
          .then(response => {
            this.community = response.data;
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      },

      callUpdate() {
        let formData = new FormData(document.getElementById('updateForm'));
        for (let index = 0; index < this.members.length; index++) {
          formData.append('members', this.members[index].username);
        }

        getAPI.patch(URL_API_COMMUNITY_UPDATE.replace(':slug', this.community.slug), formData)
          .then((response) => {
            console.log(response);
            this.$store.dispatch('updateLocalCurrentUser');
            this.$router.push({ name: 'community-detail', params: { slug: this.community.slug } });
          })
          .catch(e => {
            this.error = e.response.data.detail;
          });
      }
    }
  };
</script>

<style>
</style>