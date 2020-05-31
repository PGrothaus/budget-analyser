import React, {Component} from "react";

import MaterialTable from 'material-table';

import {fetch} from "../services/user.services";
import UserService from "../services/user.services";

import {formatCLP} from "../helpers/formats";
import {Redirect} from 'react-router-dom';


function fmt_value(elem) {
  elem.amount = formatCLP(elem.amount)
  return elem
}


export class TransactionList extends Component {
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
    newState.content.map((elem) => fmt_value(elem));
    this.setState({content: newState.content})
    console.log("handle change", this.state.content);
  }

  changeState(newState) {
    console.log("Changing state", newState);
    this.setState({content: newState.content, columns: newState.columns});
  }

  transform_data() {
    const cols = this.prepare_columns();
    const content = this.state.content;
    console.log("transform data", content)
    this.setState({columns: cols, content: content});
  }

  prepare_columns() {
    return [{title: 'Description', field: 'description'},
            {title: 'Amount', field: 'amount'},
            {title: 'Group', field: 'category.group.name'},
            {title: 'Category', field: 'category.name'}]
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
    title="Transactions"
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

// deprecated

const TransactionTable = (props) => {

    return (
      <table >
      <thead >
      <tr > {props.header}
      </tr>
      </thead>
      <tbody > {props.rowData}
      </tbody>
      </table>
    );
  }

class ClickableRow extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.state = {redirect: false};
  }

  handleClick(e) {
    const redirect = this.state.redirect;
    e.preventDefault();
    if (!redirect) {
      console.log("clicked");
      this.setState({redirect: true});};
  }

  render() {
    const redirect = this.state.redirect;
    if (redirect) {return  <Redirect  to="/profile" />};
    return (<div onClick={this.handleClick}>
            <RenderRow key={this.props.key} data={this.props.data} keys={this.props.keys} />
            </div>
    );
  }
}


const RenderRow = (props) => {
  return props.keys.map((key, index)=>{return <td key={props.data[key]}>{format(props.data[key], key)}</td>});
}


function format(datum, key) {
  if (key === 'amount') {
    return formatCLP(datum)
  }
  return datum
}
