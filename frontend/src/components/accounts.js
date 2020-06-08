import React, {Component} from "react";

import MaterialTable from 'material-table';

import {fetch} from "../services/user.services";
import UserService from "../services/user.services";

import {formatCLP} from "../helpers/formats";
import {Redirect} from 'react-router-dom';

import {is_retirement_account} from '../helpers/accounts';


function fmt_value(elem) {
  elem.gains = "n.a.";
  if (elem.invested_money > 0) {
    elem.gains = elem.value - elem.invested_money;
    elem.gains = formatCLP(elem.gains);
    elem.invested_money = formatCLP(elem.invested_money);}
  if (elem.gains === "n.a.") {elem.invested_money = "n.a."}
  elem.value = formatCLP(elem.value);

  return elem
}


export class AccountValueList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      content: [],
      columns: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.selector = this.selector.bind(this);
    this.transform_data = this.transform_data.bind(this);
    this.prepare_rows = this.prepare_rows.bind(this);
    this.prepare_columns = this.prepare_columns.bind(this);
    this.changeState = this.changeState.bind(this);
    this.fetch = this.fetch.bind(this);
  }

  handleChange(newState) {
    const content = newState.content.filter(elem => this.props.choice(elem));
    content.sort((a, b) => a.value > b.value ? -1 : 1)
    content.map((elem) => fmt_value(elem));
    this.setState({content: content})
    console.log("handle change", this.state.content);
  }

  changeState(newState) {
    console.log("Changing state", newState);
    const content = newState.content.filter(elem => !is_retirement_account(elem));
    this.setState({content: content, columns: newState.columns});
  }

  transform_data() {
    const cols = this.prepare_columns();
    const content = this.state.content.filter(elem => !is_retirement_account(elem));
    console.log("transform data", content)
    this.setState({columns: cols, content: content});
  }

  prepare_columns() {
    return [{title: 'Bank', field: 'account.bank.name'},
            {title: 'Account', field: 'account.name'},
            {title: 'Money Invested', field: 'invested_money'},
            {title: 'Value Investment', field: 'value'},
            {title: 'Gains/Losses', field:'gains'},
            ]
  }

  prepare_rows(props) {
    return this.state.content;
  }

  componentDidMount() {
    this.fetch();
    this.transform_data();
  }

  fetch() {
    fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
  }

  selector(val) {
    return val.data;
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.month !== prevProps.month) {
      fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
      this.transform_data();
    }
    if (this.props.collect !== prevProps.collect) {
      fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
      this.transform_data();
    }
  }

  render() {
  const content = this.state.content;
  const cols = this.state.columns;
  console.log("rendering again", cols, content);
  return (<MaterialTable
    title="AccountValues"
    columns={cols}
    data={content}
    editable={{
    onRowAdd: (newData) =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve();
          this.changeState((prevState) => {
            const content = [...prevState.content];
            content.push(newData);
            return { ...prevState, content};
          });
        }, 600);
      }),
    onRowUpdate: (newData, oldData) =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve();
          if (oldData) {
            console.log("PUT new Data", newData);
            UserService.putTransaction(newData)
            this.fetch();
            }
        }, 600);
      }),
    onRowDelete: (oldData) =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve();
          this.changeState((prevState) => {
            const data = [...prevState.content];
            data.splice(data.indexOf(oldData), 1);
            return { ...prevState, data };
          });
        }, 600);
      }),
  }}
/>
);
  }
}
