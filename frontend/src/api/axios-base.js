
import axios from "axios";
import store from "../utils/store";
import { URL_BACKEND } from "../constants.js";

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
    if (store.getters.loggedIn)
      config.headers["Authorization"] = "Token " + store.state.accessToken;
    return config;
});

export { axiosBase, getAPI }
