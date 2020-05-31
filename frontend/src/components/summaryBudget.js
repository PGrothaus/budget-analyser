import React, { Component } from 'react';
import DatePicker from 'react-datepicker';
import {SummarisingValueRenderer} from './expenses';
import {TransactionList} from './transactions';
import UserService from "../services/user.services";
import {fetch} from "../services/user.services";
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import {PieChart} from './pieChart';
import TransactionTypeSwitch from './switches';
import {formatCLP} from '../helpers/formats';
import {formatPct} from '../helpers/formats';


import "react-datepicker/dist/react-datepicker.css";

export default class MonthlySummary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      income: 0,
      expenses: 0,
      date: new Date(),
      selections: {selectExpenses: true},
    };
    this.handleChangeIncome = this.handleChangeIncome.bind(this);
    this.handleChangeExpenses = this.handleChangeExpenses.bind(this);
    this.handleChangeDate = this.handleChangeDate.bind(this);
    this.handleChangeSelections = this.handleChangeSelections.bind(this);
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
  handleChangeExpenses(newVal) {this.setState({expenses: newVal.content});}
  handleChangeDate(newVal) {this.setState({date: newVal});}
  totalValueSelector(val) {return val.data[0].total;}

  componentDidMount() {this.fetchAll();}

  fetchAll() {
    console.log("Fetch data for monthly summary");
    const date = this.state.date;
    const month = date.getMonth() + 1;
    fetch(UserService.getIncome, month, this.handleChangeIncome, this.totalValueSelector);
    fetch(UserService.getExpenses, month, this.handleChangeExpenses, this.totalValueSelector);
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
  const expenses = this.state.expenses;
  const savings = Math.max(0, income - expenses);
  const expenses_selected = this.state.selections.selectExpenses;
  const selections = this.state.selections;
  const savingsRate = 100 * savings / income;

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
      total={formatCLP(income)} />
    </Col>
    <Col>
    <SummarisingValueRenderer
      title={"Total Expenses"}
      total={formatCLP(expenses)} />
    </Col>
    <Col>
    <SummarisingValueRenderer
      title={"Savings Rate"}
      total={formatPct(savingsRate)} />
    </Col>
    </Row>

    <Row>
    <Col md={4}>
    <ShowChart
      expenses_selected={expenses_selected}
      month={month} />
    </Col>
    <Col>
    <ShowList
      expenses_selected={expenses_selected}
      month={month} />
    </Col>

    </Row>
    </Container>
  );}
}

function ShowList(props) {
  console.log("Decide which list", props);
  if (props.expenses_selected === true) {
    console.log("Render expenses");
    return (<TransactionList
      collect={UserService.getOutgoingTransactions}
      name={"content"}
      month={props.month}/>);
  }
  console.log("Render income");
  return (<TransactionList
    collect={UserService.getIncomingTransactions}
    name={"content"}
    month={props.month} />);
}


function ShowChart(props) {
  console.log("Decide which chart", props);
  if (props.expenses_selected === true) {
    console.log("Render expenses");
    return (<PieChart
      collect={UserService.getGroupedExpenses}
      name={"content"}
      month={props.month}
      title={"Expenses"}/>);
  }
  console.log("Render income");
  return (<PieChart
    month={props.month}
    collect={UserService.getGroupedIncome}
    name={"content"}
    title={"Income"} />);
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
