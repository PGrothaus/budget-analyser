import React from 'react';
import './App.css';

import { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import AuthService from "./services/auth.service";

import Login from "./components/login";
import Profile from "./components/profile";
import SummaryBudget from "./components/summaryBudget";
import SummaryAFP from "./components/summaryAFP";
import SummaryAssets from "./components/summaryAssets";
import SummarySavings from "./components/summarySavings";

class App extends Component {
  constructor(props) {
    super(props);
    this.logOut = this.logOut.bind(this);

    this.state = {
      currentUser: undefined
    };
  }

  componentDidMount() {
    const user = AuthService.getCurrentUser();

    if (user) {
      this.setState({
        currentUser: AuthService.getCurrentUser(),
      });
    }
  }

  logOut() {
    console.log("Logging out");
    AuthService.logout();
  }

  render() {
    const { currentUser } = this.state;

    return (
      <Router>
        <div>
          <nav className="navbar navbar-expand navbar-dark bg-dark">
            {currentUser ? (
              <UserMenu logOut={this.logOut}/>
            ) : (
              <LoginMenu />
            )}
          </nav>

          <div className="container mt-3">
            <Switch>
              <Route exact path="/login" component={Login} />
              <Route exact path="/overview" component={Profile} />
              <Route exact path="/budget" component={SummaryBudget} />
              <Route exact path="/afp" component={SummaryAFP} />
              <Route exact path="/savings" component={SummarySavings} />
              <Route exact path="/assets" component={SummaryAssets} />
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}


const UserMenu = (props) => {
  return (
    <div className="navbar-nav mr-auto">
      <li className="nav-item">
        <Link to={"/overview"} className="nav-link">
          Overview
        </Link>
      </li>
      <li className="nav-item">
        <Link to={"/budget"} className="nav-link">
          Monthly Budget
        </Link>
      </li>
      <li className="nav-item">
        <Link to={"/afp"} className="nav-link">
          AFP/APV
        </Link>
      </li>
      <li className="nav-item">
        <Link to={"/savings"} className="nav-link">
          Savings
        </Link>
      </li>
      <li className="nav-item">
        <Link to={"/assets"} className="nav-link">
          Investments
        </Link>
      </li>
      <li className="nav-item ml-auto">
        <a href="/logout" className="nav-link" onClick={props.logOut}>
          LogOut
        </a>
      </li>
    </div>
  );
}


const LoginMenu = (props) => {
  return (
    <div className="navbar-nav mr-auto">
      <li className="nav-item">
        <Link to={"/login"} className="nav-link">
          Login
        </Link>
      </li>
    </div>
  )
}

export default App;
