
import axios from "axios"
import store from "../store"
import { URL_BACKEND } from '../constants.js';

const axiosBase = axios.create({
  baseURL: URL_BACKEND,
  headers: {
    contentType: "application/json"
  }
})

const getAPI = axios.create({
  baseURL: URL_BACKEND,
  withCredentials: false, // This is the default
  headers: {
    Accept: "application/json",
    contentType: "application/json"
  }
});

getAPI.interceptors.request.use(function (config) {
    // Do something before request is sent
    let token = store.getters.accessToken
    config.headers["Authorization"] = "Token " + token;
    return config;
});

// getAPI.interceptors.response.use(undefined, function (err) {
//   // if error response status is 401, it means the request was invalid due to expired access token
//   if (err.config && err.response && err.response.status === 401) {
//     store.dispatch('refreshToken') // attempt to obtain new access token by running 'refreshToken' action
//       .then(access => {
//         // if successful re-send the request to get the data from server
//         axios.request({
//           baseURL: URL_BACKEND,
//           method: 'get',
//           headers: { Authorization: `Bearer ${access}` }, // the new access token is attached to the authorization header
//           url: '/mods/'
//         }).then(response => {
//           // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
//           // data from it and display to the client.
//           console.log('Success getting the Mods')
//           store.state.APIData = response.data
//         }).catch(err => {
//           console.log('Got the new access token but error while trying to fetch data from the API using it')
//           return Promise.reject(err)
//         })
//       })
//       .catch(err => {
//         return Promise.reject(err)
//       })
//   }
// })

export { axiosBase, getAPI }

// const apiClient = axios.create({
//     withCredentials: false, // This is the default
//     headers: {
//         Accept: 'application/json',
//         'Content-Type': 'application/json'
//     }
// });

// apiClient.interceptors.request.use(function (config) {
//     // Do something before request is sent
//     let authKey = store.getters.getAuthKey
//     config.headers["Authorization"] = "Basic " + authKey;
//     return config;
// });

// export default apiClient;