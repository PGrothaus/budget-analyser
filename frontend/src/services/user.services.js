import axios from 'axios';
import authHeader from './auth-header';

const TARGET_ENV = process.env["REACT_APP_TARGET_ENV"];

const API_URL = TARGET_ENV === "PRODUCTION" ? process.env["REACT_APP_API_URL_PROD"] : process.env["REACT_APP_API_URL_DEV"];
console.log(API_URL);

class UserService {

  getNetWorth(props) {
    console.log("Get networth", props);
    return axios.get(API_URL + 'networth', { headers: authHeader() });
  }

  getNetWorthHistory(props) {
    console.log("Get networth history", props);
    return axios.get(API_URL + 'networth/history', { headers: authHeader() });
  }

  getRetirementHistory(props) {
    console.log("Get retirement history", props);
    return axios.get(API_URL + 'retirement/history', { headers: authHeader() });
  }

  getRetirementInvestmentHistory(props) {
    console.log("Get retirement investment history", props);
    return axios.get(API_URL + 'retirement/investment/history', { headers: authHeader() });
  }

  getSavingsHistory(props) {
    console.log("Get savings history", props);
    return axios.get(API_URL + 'savings/history', { headers: authHeader() });
  }

  getSavingsInvestmentHistory(props) {
    console.log("Get savings investment history", props);
    return axios.get(API_URL + 'savings/investment/history', { headers: authHeader() });
  }

  getAverageExpenses(props) {
    console.log("MonthwiseExpenses", props);
    return axios.get(API_URL + 'expenses/average', { headers: authHeader() });
  }

  getAverageIncome(props) {
    console.log("MonthwiseIncome", props);
    return axios.get(API_URL + 'income/average', { headers: authHeader() });
  }

  getMonthwiseIncome(props) {
    console.log("get monthwise Income", props);
    const month = props.toString();
    return axios.get(API_URL + 'income/monthwise', { headers: authHeader() });
  }

  getExpenses(props) {
    console.log("getExpenses", props);
    const month = props.toString();
    return axios.get(API_URL + 'expenses?date__month=' + month, { headers: authHeader() });
  }

  getMonthwiseExpenses(props) {
    console.log("get monthwise Expenses", props);
    const month = props.toString();
    return axios.get(API_URL + 'expenses/monthwise', { headers: authHeader() });
  }

  getAssetList(props) {
    console.log("getAssetList", props);
    return axios.get(API_URL + 'asset_values', { headers: authHeader() });
  }

  getIncome(props) {
    console.log("getIncome", props);
    const month = props.toString();
    return axios.get(API_URL + 'income?date__month=' + month, { headers: authHeader() });
  }

  getIncomeComplete(props) {
    console.log("getIncomeComplete", props);
    const month = props.toString();
    return axios.get(API_URL + 'income/complete?date__month=' + month, { headers: authHeader() });
  }

  getOutgoingTransactions(props) {
    console.log("getOutgoingTransactions", props);
    const month = props.toString();
    return axios.get(API_URL + 'transactions?type=expense&date__month=' + month, { headers: authHeader() });
  }

  getIncomingTransactions(props) {
    console.log("getIncomingTransactions", props);
    const month = props.toString();
    return axios.get(API_URL + 'transactions?type=income&date__month=' + month, { headers: authHeader() });
  }

  getGroupedExpenses(props) {
    console.log("getGroupedExpenses", props);
    const month = props.toString();
    return axios.get(API_URL + 'expenses/grouped?date__month=' + month, { headers: authHeader() });
  }

  getGroupedIncome(props) {
    console.log("getGroupedIncome", props);
    const month = props.toString();
    return axios.get(API_URL + 'income/grouped?date__month=' + month, { headers: authHeader() });
  }

  putTransaction(props) {
    const url = API_URL + "transaction/" + props.id.toString();
    console.log("Put to", url, props);
    axios.put(url,
              props,
              {headers: authHeader()})
      .then(r => console.log(r.status))
      .catch(e => console.log(e));
    }

  getCurrentAccountValues(props) {
    return axios.get(API_URL + 'account_values', { headers: authHeader() });
  }
}


export function fetch(collect, month, setState, selector) {
  console.log("Fetching Data...", collect, month, setState, selector);
  collect(month).then(
    response => {
      console.log("Collected data", response);
      setState({content: selector(response)});
    },
    error => {
      setState({
        content:
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString()
      });
    }
  );
}

export default new UserService();
