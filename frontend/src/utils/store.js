
import Vue from "vue"
import Vuex from "vuex"
import { axiosBase, getAPI } from "../api/axios-base"
import {
  URL_API_ACCOUNT_SIGNUP,
  URL_API_ACCOUNT_LOGOUT,
  URL_API_ACCOUNT_LOGIN,
  URL_API_LANGUAGE_LIST
} from "../constants.js";

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
     accessToken: localStorage.getItem("access_token") || null,
     currentUser: localStorage.getItem("current_user") !== null ? JSON.parse(localStorage.getItem("current_user")) : null,
     allLanguages: localStorage.getItem("all_languages") !== null ? JSON.parse(localStorage.getItem("all_languages")) : null,
    // refreshing the page
     // refreshToken: localStorage.getItem("refresh_token") || null,
     APIData: "" // received data from the backend API is stored here.
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null;
    }
  },
  mutations: {
    updateToken (state, token) {
      localStorage.setItem("access_token", token);
      state.accessToken = token;
    },
    updateCurrentUser (state, current_user) {
      localStorage.setItem("current_user", JSON.stringify(current_user));
      state.currentUser = current_user;
    },
    /*
    // updateLocalStorage (state, { access, refresh }) {
    updateLocalStorage (state, { token, current_user }) {
      localStorage.setItem("access_token", token);
      localStorage.setItem("current_user", JSON.stringify(current_user));
      // localStorage.setItem("refresh_token", refresh);
      state.accessToken = token;
      state.currentUser = current_user;
      // state.refreshToken = refresh
    },
    */
    // updateCurrentuser (state, current_user) {
    //   localStorage.setItem("current_user", JSON.stringify(current_user))
    // },
    // updateAccess (state, token) {
    //   state.accessToken = token
    // },
    destroyToken (state) {
      state.accessToken = null
      state.currentUser = null
      // state.allLanguages = null
      // state.refreshToken = null

      localStorage.removeItem("access_token");
      localStorage.removeItem("current_user");
      // localStorage.removeItem("all_languages");
      // localStorage.removeItem("refresh_token");
    }
  },
  actions: {
    // run the below action to get a new access token on expiration
    // refreshToken (context) {
    //   return new Promise((resolve, reject) => {
    //     axiosBase.post("/api/token/refresh/", {
    //       refresh: context.state.refreshToken
    //     }) // send the stored refresh token to the backend API
    //       .then(response => { // if API sends back new access and refresh token update the store
    //         console.log("New access successfully generated")
    //         context.commit("updateAccess", response.data.access)
    //         resolve(response.data.access)
    //       })
    //       .catch(err => {
    //         console.log("error in refreshToken Task")
    //         reject(err) // error generating new access and refresh token because refresh token has expired
    //       })
    //   })
    // },
    registerUser (context, data) {
      return new Promise((resolve, reject) => {
        axiosBase.post(URL_API_ACCOUNT_SIGNUP, {
          name: data.name,
          email: data.email,
          username: data.username,
          password: data.password,
          confirm: data.confirm
        })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error);
          })
      })
    },
    logoutUser (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          axiosBase.post(URL_API_ACCOUNT_LOGOUT)
            .then(response => {
              context.commit("destroyToken");
              resolve(response);
            })
            .catch(err => {
              context.commit("destroyToken");
              reject(err);
            })
        })
      }
    },
    loginUser (context, credentials) {
      return new Promise((resolve, reject) => {
        // send the email and password to the backend API:
        axiosBase.post(URL_API_ACCOUNT_LOGIN, {
          email: credentials.email,
          password: credentials.password
        })
        // if successful update local storage:
          .then(response => {
            context.commit("updateToken", response.data.token);
            context.commit("updateCurrentUser", response.data.user);
            // context.commit("updateLocalStorage", { token: response.data.token, current_user: response.data.user });
            // context.commit("updateLocalStorage", { access: response.data.access, refresh: response.data.refresh }); // store the access and refresh token in localstorage
            resolve();
          })
          .catch(err => {
            reject(err);
          })
      })
    },
    getLanguages () {
      getAPI.get(URL_API_LANGUAGE_LIST)
        .then((response) => {
          localStorage.setItem("all_languages", JSON.stringify(response.data));
        });
    }

  }
})