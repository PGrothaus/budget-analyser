import React, { Component } from "react";
import AuthService from "../services/auth.service";
import UserService from "../services/user.services"
import {fetch} from "../services/user.services";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import {AreaChart} from "./charts";
import {VerticalBarChart} from "./charts";
import {formatCLP} from "../helpers/formats";
import {formatPct} from "../helpers/formats";
import {SummarisingValueRenderer} from "./expenses";
import {Chart} from "./charts";
import {copy} from "../helpers/misc";

export default class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      currentUser: AuthService.getCurrentUser(),
      expenses: 0,
      income: 0,
      netWorth: 0,
      netWorthHistory: [],
      showPlot: "networth",
      monthwiseExpenses: [],
      monthwiseIncome: [],
    };
    this.handleChangeExpenses = this.handleChangeExpenses.bind(this);
    this.handleChangeIncome = this.handleChangeIncome.bind(this);
    this.handleChangeNetWorth = this.handleChangeNetWorth.bind(this);
    this.handleChangeNetWorthHistory = this.handleChangeNetWorthHistory.bind(this);
    this.handleChangeMonthwiseExpenses = this.handleChangeMonthwiseExpenses.bind(this);
    this.handleChangeMonthwiseIncome = this.handleChangeMonthwiseIncome.bind(this);
    this.chosePlotSavingsRate = this.chosePlotSavingsRate.bind(this);
    this.chosePlotSavings = this.chosePlotSavings.bind(this);
    this.chosePlotNetworth = this.chosePlotNetworth.bind(this);
    this.chosePlotIncome = this.chosePlotIncome.bind(this);
    this.chosePlotExpenses = this.chosePlotExpenses.bind(this);
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
    fetch(UserService.getMonthwiseExpenses,
          0,
          this.handleChangeMonthwiseExpenses,
          this.selector);
    fetch(UserService.getMonthwiseIncome,
          0,
          this.handleChangeMonthwiseIncome,
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

  handleChangeMonthwiseExpenses(e) {
    console.log("update state: monthwise expenses", e);
    this.setState({monthwiseExpenses: e.content[0]});
  }

  handleChangeMonthwiseIncome(e) {
    console.log("update state: monthwise income", e);
    this.setState({monthwiseIncome: e.content[0]});
  }

  chosePlotNetworth() {
    console.log("Update state: show plot networth");
    this.setState({showPlot: "networth"})
  }

  chosePlotSavingsRate() {
    console.log("Update state: show plot savingsrate");
    this.setState({showPlot: "savingsrate"})
  }

  chosePlotSavings() {
    console.log("Update state: show plot savings");
    this.setState({showPlot: "savings"})
  }

  chosePlotIncome() {
    console.log("Update state: show plot income");
    this.setState({showPlot: "income"})
  }

  chosePlotExpenses() {
    console.log("Update state: show plot expenses");
    this.setState({showPlot: "expenses"})
  }

  selector(response) {
    return response.data
  }

  render() {
    console.log("Rendering Profile", this.state);
    const nwHistory = copy(this.state.netWorthHistory);
    const monthwiseIncome = copy(this.state.monthwiseIncome);
    const monthwiseExpenses = copy(this.state.monthwiseExpenses);
    const monthwiseSavings = calculateDifference(monthwiseIncome, monthwiseExpenses);
    const savingRates = calculateSRs(monthwiseSavings, monthwiseIncome);
    const keyPlot = this.state.showPlot;
    const plotData = {"networth": nwHistory,
                      "income": monthwiseIncome,
                      "expenses": monthwiseExpenses,
                      "savings": monthwiseSavings,
                      "savingsrate": savingRates};
    return (
      <div>
      <Container>
      <Row>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Income"}
        onClickHandler={this.chosePlotIncome}
        total={formatCLP(this.state.income)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Expenses"}
        onClickHandler={this.chosePlotExpenses}
        total={formatCLP(this.state.expenses)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Savings"}
        onClickHandler={this.chosePlotSavings}
        total={formatCLP(this.state.income - this.state.expenses)}/>
      </Col>
      </Row>
      <Row>
      <Col>
      <SummarisingValueRenderer
        title={"Networth"}
        onClickHandler={this.chosePlotNetworth}
        total={formatCLP(this.state.netWorth)}/>
      </Col>
      <Col>
      <SummarisingValueRenderer
        title={"Average Monthly Savings Rate"}
        onClickHandler={this.chosePlotSavingsRate}
        total={formatPct(100*(this.state.income - this.state.expenses) / (this.state.income))}/>
      </Col>
      <Col>
      </Col>
      </Row>
      <ShowPlot selection={keyPlot} data={plotData} />
      </Container>
      </div>
    );
  }
}


const ShowMonth = ({elem}) => (
  <p>{elem.month.toString() + ": " + elem.total.toString()}</p>
);


function ShowPlot(props) {
  if ("networth" === props.selection) {
    return <AreaChart data={props.data["networth"]} />
  } else if ("income" === props.selection) {
      return <VerticalBarChart data={props.data["income"]} />
    } else if ("expenses" === props.selection) {
        return <VerticalBarChart data={props.data["expenses"]} />
      } else if ("savings" === props.selection) {
          return <VerticalBarChart data={props.data["savings"]} />
        } else if ("savingsrate" === props.selection) {
            return <VerticalBarChart data={props.data["savingsrate"]} />
        } else {
    return props.selection
  }
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


function calculateSRs(savings, income) {
  const rates = copy(savings);
  rates.forEach((item, i) => {
    const exp = findCorrespondingExpenses(item, income);
    const delta = 100. * item.monthly_total / exp.monthly_total;
    console.log("rate", delta)
    item.monthly_total = delta
  });
  return rates
}


function calculateDifference(income, expenses) {
  const savings = copy(income);
  savings.forEach((elem, i) => {
    const exp = findCorrespondingExpenses(elem, expenses);
    console.log(elem.monthly_total, exp.monthly_total);
    const delta = elem.monthly_total - exp.monthly_total;
    elem.monthly_total = delta
  });
  return savings
}

function findCorrespondingExpenses(elem, expenses) {
  var selected = 0;
  expenses.forEach((item, i) => {
    if (elem.month === item.month) {
      selected = copy(item);
    }

  });
  return selected
}
