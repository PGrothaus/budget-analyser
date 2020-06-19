import React, { Component } from 'react';
import DatePicker from 'react-datepicker';
import {SummarisingValueRenderer} from './expenses';
import {TransactionTable} from "./tables";
import UserService from "../services/user.services";
import {fetch} from "../services/user.services";
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import {BarChart} from './charts';
import TransactionTypeSwitch from './switches';
import {formatCLP} from '../helpers/formats';
import {formatPct} from '../helpers/formats';


import "react-datepicker/dist/react-datepicker.css";

export default class MonthlySummary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      income: 0,
      income_complete: 0,
      expenses: 0,
      groupedExpenses: [],
      groupedIncome: [],
      incomingTransactions: [],
      outgoingTransactions: [],
      date: new Date(),
      selections: {selectExpenses: true},
    };
    this.handleChangeIncome = this.handleChangeIncome.bind(this);
    this.handleChangeIncomeComplete = this.handleChangeIncomeComplete.bind(this);
    this.handleChangeExpenses = this.handleChangeExpenses.bind(this);
    this.handleChangeDate = this.handleChangeDate.bind(this);
    this.handleChangeSelections = this.handleChangeSelections.bind(this);
    this.handleChangeOutgoingTransactions = this.handleChangeOutgoingTransactions.bind(this);
    this.handleChangeIncomingTransactions = this.handleChangeIncomingTransactions.bind(this);
    this.handleChangeGroupedIncome = this.handleChangeGroupedIncome.bind(this);
    this.handleChangeGroupedExpenses = this.handleChangeGroupedExpenses.bind(this);
    this.totalValueSelector = this.totalValueSelector.bind(this);
    this.fetchAll = this.fetchAll.bind(this);
  }

  handleChangeSelections(event) {
    const curVal = this.state.selections.selectExpenses;
    const newVal = !curVal;
    const newState = {selectExpenses: newVal};
    this.setState({selections: newState});
  };

  handleChangeIncome(newVal) {this.setState({income: newVal.content});}
  handleChangeIncomeComplete(newVal) {this.setState({income_complete: newVal.content});}
  handleChangeExpenses(newVal) {this.setState({expenses: newVal.content});}
  handleChangeDate(newVal) {this.setState({date: newVal});}
  handleChangeOutgoingTransactions(newVal) {this.setState({outgoingTransactions: newVal.content});}
  handleChangeIncomingTransactions(newVal) {this.setState({incomingTransactions: newVal.content});}
  handleChangeGroupedExpenses(newVal) {this.setState({groupedExpenses: newVal.content});}
  handleChangeGroupedIncome(newVal) {this.setState({groupedIncome: newVal.content});}
  totalValueSelector(val) {return val.data[0].total;}
  valueSelector(val) {return val.data;}

  componentDidMount() {this.fetchAll();}

  fetchAll() {
    console.log("Fetch data for monthly summary");
    const date = this.state.date;
    const month = date.getMonth() + 1;
    fetch(UserService.getIncome, month, this.handleChangeIncome, this.totalValueSelector);
    fetch(UserService.getExpenses, month, this.handleChangeExpenses, this.totalValueSelector);
    fetch(UserService.getIncomeComplete, month, this.handleChangeIncomeComplete, this.totalValueSelector);
    fetch(UserService.getOutgoingTransactions, month, this.handleChangeOutgoingTransactions, this.valueSelector);
    fetch(UserService.getIncomingTransactions, month, this.handleChangeIncomingTransactions, this.valueSelector);
    fetch(UserService.getGroupedIncome, month, this.handleChangeGroupedIncome, this.valueSelector);
    fetch(UserService.getGroupedExpenses, month, this.handleChangeGroupedExpenses, this.valueSelector);
  }

  componentDidUpdate(prevProps, prevState) {
  const month_current = this.state.date.getMonth();
  console.log("update component?", this.state, prevState.date);
  if (prevState.date) {
    const month_prev = prevState.date.getMonth();
    if (month_current !== month_prev) {
      console.log("Component UPDATE", month_current);
      this.fetchAll();
      }
    }
  console.log("Done");
  }

  render() {
  console.log("RENDERING", this.state);
  const date = this.state.date;
  const month = date.getMonth() + 1;
  const income = this.state.income;
  const income_complete = this.state.income_complete;
  const expenses = this.state.expenses;
  const savings = Math.max(0, income - expenses);
  const expenses_selected = this.state.selections.selectExpenses;
  const selections = this.state.selections;
  const incomingTransactions = this.state.incomingTransactions;
  const outgoingTransactions = this.state.outgoingTransactions;
  const groupedIncome = this.state.groupedIncome;
  const groupedExpenses = this.state.groupedExpenses;
  var savingsRate = 0.;
  var savingsRateComplete = 0.;
  if (income > 0) {
    savingsRate = 100 * savings / income;
    savingsRateComplete = 100 * (savings - income + income_complete) / income_complete;
  }

  const title = "Grouped Expenses";
  var options = { year: 'numeric', month: 'long'};


  return (
    <Container>
    <Row >
    <Col className="left-column">
      <MonthPicker
        value={date}
        onChange={this.handleChangeDate} />
    </Col>
    <Col className="center-column">
      <h3>{date.toLocaleDateString("en-US", options)}</h3>
    </Col>
    <Col className="right-column">
    <TransactionTypeSwitch
      selections={selections}
      handleChange={this.handleChangeSelections} />
    </Col>
    </Row>

    <Row>
    <Col>
    <SummarisingValueRenderer
      title={"Total Income"}
      total={formatCLP(income) + " (" + formatCLP(income_complete).substring(4) + ")"} />
    </Col>
    <Col>
    <SummarisingValueRenderer
      title={"Total Expenses"}
      total={formatCLP(expenses)} />
    </Col>
    <Col>
    <SummarisingValueRenderer
      title={"Savings Rate"}
      total={formatPct(savingsRate) + " (" + formatPct(savingsRateComplete) + ")"} />
    </Col>
    </Row>

    <Row>
    <Col md={4}>
    <ShowChart
      expenses_selected={expenses_selected}
      groupedIncome={groupedIncome}
      groupedExpenses={groupedExpenses} />
    </Col>
    <Col>
    <ShowTable
      expenses_selected={expenses_selected}
      incomingTransactions={incomingTransactions}
      outgoingTransactions={outgoingTransactions} />
    </Col>

    </Row>
    </Container>
  );}
}

function ShowTable(props) {
  if (props.expenses_selected === true) {
    console.log("Render outgoing transacion table", props);
    return (<TransactionTable
      elems={props.outgoingTransactions} />);
  }
  console.log("Render incoming transaction table", props);
  return (<TransactionTable
      elems={props.incomingTransactions} />);
}


function ShowChart(props) {
  console.log("Decide which chart", props);
  if (props.expenses_selected === true) {
    console.log("Render pie chart grouped expenses", props);
    return <BarChart elems={props.groupedExpenses} />;
  }
  console.log("Render pie chart grouped income", props);
  return <BarChart elems={props.groupedIncome} />;
}


export function MonthPicker(props) {

  return (
    <div>
    <DatePicker
      selected={props.value}
      onChange={val => props.onChange(val)}
      dateFormat="MM/yyyy"
      showMonthYearPicker
    />
    </div>
  );
}
