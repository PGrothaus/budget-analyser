import React, { Component } from "react";
import AuthService from "../services/auth.service";
import UserService from "../services/user.services"
import {fetch} from "../services/user.services";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import {formatCLP} from "../helpers/formats";
import {formatPct} from "../helpers/formats";
import {SummarisingValueRenderer} from "./expenses";
import {Chart} from "./charts";

export default class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      currentUser: AuthService.getCurrentUser(),
      expenses: 0,
      income: 0,
      netWorth: 0,
      netWorthHistory: [],
    };
    this.handleChangeExpenses = this.handleChangeExpenses.bind(this);
    this.handleChangeIncome = this.handleChangeIncome.bind(this);
    this.handleChangeNetWorth = this.handleChangeNetWorth.bind(this);
    this.handleChangeNetWorthHistory = this.handleChangeNetWorthHistory.bind(this);
    this.selector = this.selector.bind(this);
  }

  componentDidMount() {
    fetch(UserService.getAverageExpenses,
          0,
          this.handleChangeExpenses,
          this.selector);
    fetch(UserService.getAverageIncome,
          0,
          this.handleChangeIncome,
          this.selector);
    fetch(UserService.getNetWorth,
          0,
          this.handleChangeNetWorth,
          this.selector);
    fetch(UserService.getNetWorthHistory,
          0,
          this.handleChangeNetWorthHistory,
          this.selector);
  }

  handleChangeExpenses(e) {
    console.log("ChangeExpenses", e);
    this.setState({expenses: e.content[0].total});
  }

  handleChangeIncome(e) {
    console.log("ChangeIncome", e);
    this.setState({income: e.content[0].total});
  }

  handleChangeNetWorth(e) {
    console.log("ChangeNetWorth", e);
    this.setState({netWorth: e.content[0].total});
  }

  handleChangeNetWorthHistory(e) {
    console.log("ChangeNetWorthHistroy", e);
    this.setState({netWorthHistory: e.content});
  }

  selector(response) {
    return response.data
  }

  render() {
    console.log(this.state);
    const nwHistory = this.state.netWorthHistory;
    return (
      <div>
      <Container>
      <Row>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Income"}
        total={formatCLP(this.state.income)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Expenses"}
        total={formatCLP(this.state.expenses)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Savings"}
        total={formatCLP(this.state.income - this.state.expenses)}/>
      </Col>
      </Row>
      <Row>
      <Col>
      <SummarisingValueRenderer
        title={"Networth"}
        total={formatCLP(this.state.netWorth)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Savings Rate"}
        total={formatPct(100*(this.state.income - this.state.expenses) / (this.state.income))}/>
      </Col>
      <Col>
      </Col>
      </Row>
      <ShowNetWorthHistoryChart data={nwHistory} />
      </Container>
      </div>
    );
  }
}


const ShowMonth = ({elem}) => (
  <p>{elem.month.toString() + ": " + elem.total.toString()}</p>
);


function ShowNetWorthHistoryChart(props) {
  return (<Chart
    type="area"
    month={0}
    data={props.data}
    />);
  }


const ProfileRenderer = ({user}) => (
  <div className="container">
    <header className="jumbotron">
      <h3>
        <strong>{user.name}</strong> Profile
      </h3>
    </header>
    <p>
      <strong>Token:</strong>{" "}
      {user.access.substring(0, 20)} ...{" "}
      {user.access.substr(user.access.length - 20)}
    </p>
  </div>
);
