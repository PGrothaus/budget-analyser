import axios from "axios";
console.log(process.env);

const TARGET_ENV = process.env["REACT_APP_TARGET_ENV"];

const API_URL = TARGET_ENV === "PRODUCTION" ? process.env["REACT_APP_API_URL_PROD"] : process.env["REACT_APP_API_URL_DEV"];
console.log(API_URL);

class AuthService {
  login(email, password) {
    return axios
      .post(API_URL + "token/", {
        email,
        password
      })
      .then(response => {
        console.log(response.data);
        if (response.data) {
          console.log("Writing to local storage");
          localStorage.setItem("user", JSON.stringify(response.data));
        }
        console.log("return data");
        return response.data;
      });
  }

  logout() {
    localStorage.removeItem("user");
  }

  getCurrentUser() {
  return JSON.parse(localStorage.getItem('user'));;
  }
}

export default new AuthService();
