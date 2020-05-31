import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/";

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
