import React, { Component } from "react";
import Form from "react-validation/build/form";
import Input from "react-validation/build/input";
import CheckButton from "react-validation/build/button";

import { isEmail } from "validator";

import AuthService from "../services/auth.service";

const required = value => {
  if (!value) {
    return (
      <div className="alert alert-danger" role="alert">
        This field is required!
      </div>
    );
  }
};

const checkIsEmail = value => {
  if (!isEmail(value)) {
    return (
      <div className="alert alert-danger" role="alert">
        This is not a valid email.
      </div>
    );
  }
};

export default class Login extends Component {
  constructor(props) {
    super(props);
    this.handleLogin = this.handleLogin.bind(this);
    this.onChangeEmail = this.onChangeEmail.bind(this);
    this.onChangePassword = this.onChangePassword.bind(this);

    this.state = {
      email: "",
      password: "",
      loading: false,
      message: ""
    };
  }

  onChangeEmail(e) {
    this.setState({
      email: e.target.value
    });
  }

  onChangePassword(e) {
    this.setState({
      password: e.target.value
    });
  }

  handleLogin(e) {
    e.preventDefault();

    this.setState({
      message: "",
      loading: true
    });

    this.form.validateAll();

    if (this.checkBtn.context._errors.length === 0) {
      console.log("email", this.state.email);
      console.log("password", this.state.password);
      AuthService.login(this.state.email, this.state.password).then(
        () => {
          this.props.history.push("/overview");
          window.location.reload();
        },
        error => {
          const resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();

          this.setState({
            loading: false,
            message: resMessage
          });
        }
      );
    } else {
      this.setState({
        loading: false
      });
    }
  }

  render() {
    const email = this.state.email;
    const password = this.state.password;
    const loading = this.state.loading;
    const message = this.state.message;

    return (
      <div className="container">
      <div className="row">
      <div className="col">
      </div>
      <div className="col">
        <div className="card card-container">
          <img
            src="//ssl.gstatic.com/accounts/ui/avatar_2x.png"
            alt="profile-img"
            className="profile-img-card"
          />

          <Form
            onSubmit={this.handleLogin}
            ref={c => {
              this.form = c;
            }}
          >

            <EmailField
              value={email}
              onChange={this.onChangeEmail} />
            <PasswordField
              value={password}
              onChange={this.onChangePassword} />
            <LoginButtonField
              value={loading}
              message={message} />

            {message && (
              <div className="form-group">
                <div className="alert alert-danger" role="alert">
                  {message}
                </div>
              </div>
            )}
            <CheckButton
              style={{ display: "none" }}
              ref={c => {
                this.checkBtn = c;
              }}
            />
          </Form>
        </div>
      </div>
      <div className="col">
      </div>
      </div>
    </div>
    );
  }
}


const PasswordField = (props) => (
<div className="form-group">
  <label htmlFor="password">Password</label>
  <Input
    type="password"
    className="form-control"
    name="password"
    value={props.value}
    onChange={props.onChange}
    validations={[required]}
  />
</div>
);

const EmailField = (props) => (
  <div className="form-group">
    <label htmlFor="email">Email</label>
    <Input
      type="text"
      className="form-control"
      name="email"
      value={props.value}
      onChange={props.onChange}
      validations={[required, checkIsEmail]}
    />
  </div>
);

const LoginButtonField = (props) => (
  <div className="form-group">
    <button
      className="btn btn-primary btn-block"
      disabled={props.value}
    >
      {props.value && (
        <span className="spinner-border spinner-border-sm"></span>
      )}
      <span>Login</span>
    </button>
  </div>
);
