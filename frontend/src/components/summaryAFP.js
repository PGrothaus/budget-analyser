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
import {is_retirement_account} from '../helpers/accounts';
import {sum_account_values} from '../helpers/accounts';
import {sum_account_investments} from '../helpers/accounts';


export default class SummaryAFP extends Component {
  constructor(props) {
    super(props);
    this.state = {
      account_values: [],
      retirementHistory: [],
      retirementInvestmentHistory: [],
    }
    this.fetch_all = this.fetch_all.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onChangeRetirementHistory = this.onChangeRetirementHistory.bind(this);
    this.onChangeRetirementInvestmentHistory = this.onChangeRetirementInvestmentHistory.bind(this);
    this.selector = this.selector.bind(this);
  }

  componentDidMount() {
    this.fetch_all();
  }

  onChange(newState) {
    console.log("Setting new state", newState);
    this.setState({account_values: newState.content});
  }

  onChangeRetirementHistory(newState) {
    console.log("Setting new retirement history state", newState);
    this.setState({retirementHistory: newState.content});
  }

  onChangeRetirementInvestmentHistory(newState) {
    console.log("Setting new retirement investment history state", newState);
    this.setState({retirementInvestmentHistory: newState.content});
  }

  selector(val) {return val.data;}

  fetch_all() {
    fetch(UserService.getCurrentAccountValues, 0, this.onChange, this.selector);
    fetch(UserService.getRetirementHistory, 0, this.onChangeRetirementHistory, this.selector);
    fetch(UserService.getRetirementInvestmentHistory, 0, this.onChangeRetirementInvestmentHistory, this.selector);
  }

  render() {
    const elems = this.state.account_values;
    const retirementHistory = this.state.retirementHistory;
    const retirementInvestmentHistory = this.state.retirementInvestmentHistory;
    console.log("rendering afp page", elems);
    if (elems.length === 0) {
        return ""
    }
    const elems_retirement = copy(elems.filter(elem => is_retirement_account(elem)));
    const total_retirement = sum_account_values(elems_retirement);
    const total_investments = sum_account_investments(elems_retirement);
    const total_gains = total_retirement - total_investments;
    return (<div>
            <Container>
              <Row>
              <Col>
                <SummarisingValueRenderer title="Total Money Invested"
                                          total={formatCLP(total_investments)} />
                </Col>
                <Col>
                  <SummarisingValueRenderer title="Total Retirement"
                                            total={formatCLP(total_retirement)} />
                </Col>
                <Col>
                  <SummarisingValueRenderer title="Total Gains"
                                            total={formatCLP(total_gains)} />
                </Col>
              </Row>
              <AccountTable elems={elems_retirement} />
            </Container>
            <StackedAreaChart data={[retirementHistory, retirementInvestmentHistory]} />
            </div>
          );
  }
}
