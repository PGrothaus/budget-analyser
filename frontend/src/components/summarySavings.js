import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import UserService from "../services/user.services";
import {fetch} from "../services/user.services";

import {SummarisingValueRenderer} from './expenses';
import {AccountTable} from './tables';
import {StackedAreaChart} from "./charts";

import {copy} from "../helpers/misc";
import {formatCLP} from '../helpers/formats';
import {is_liquid_account} from '../helpers/accounts';
import {sum_account_values} from '../helpers/accounts';
import {sum_account_investments} from '../helpers/accounts';


export default class SummarySavings extends Component {
  constructor(props) {
    super(props);
    this.state = {
      account_values: [],
      savingsHistory: [],
      savingsInvestmentHistory: [],
    }
    this.fetch_all = this.fetch_all.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onChangeSavingsHistory = this.onChangeSavingsHistory.bind(this);
    this.onChangeSavingsInvestmentHistory = this.onChangeSavingsInvestmentHistory.bind(this);
    this.selector = this.selector.bind(this);
  }

  componentDidMount() {
    this.fetch_all();
  }

  onChange(newState) {
    console.log("Setting new state", newState);
    this.setState({account_values: newState.content});
  }

  onChangeSavingsHistory(newState) {
    console.log("Updating state: savingsHistory", newState);
    this.setState({savingsHistory: newState.content});
  }

  onChangeSavingsInvestmentHistory(newState) {
    console.log("Updating state: savingsInvestmentHistory", newState);
    this.setState({savingsInvestmentHistory: newState.content});
  }

  selector(val) {return val.data;}

  fetch_all() {
    fetch(UserService.getCurrentAccountValues, 0, this.onChange, this.selector);
    fetch(UserService.getSavingsHistory, 0, this.onChangeSavingsHistory, this.selector);
    fetch(UserService.getSavingsInvestmentHistory, 0, this.onChangeSavingsInvestmentHistory, this.selector);
  }

  render() {
    const elems = this.state.account_values;
    const savingsHistory = this.state.savingsHistory;
    const savingsInvestmentHistory = this.state.savingsInvestmentHistory;
    if (elems.length === 0) {
        return ""
    }
    const elems_liquid = copy(elems.filter(elem => is_liquid_account(elem)));
    const total_liquid = sum_account_values(elems_liquid);
    const total_investments = sum_account_investments(elems_liquid);
    const total_gains = total_liquid - total_investments;
    return (<div>
            <Container>
              <Row>
                <Col>
                  <SummarisingValueRenderer title="Total Savings"
                                            total={formatCLP(total_liquid)} />
                </Col>
                <Col>
                  <SummarisingValueRenderer title="Gains Included"
                                            total={formatCLP(total_gains)} />
                </Col>
              </Row>
              <AccountTable elems={elems_liquid} />
            </Container>
            <StackedAreaChart data={[savingsHistory, savingsInvestmentHistory]} />
            </div>
          );
  }
}
