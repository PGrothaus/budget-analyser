import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://127.0.0.1:8000/api/';

class UserService {

  getNetWorth(props) {
    console.log("NetWorth", props);
    return axios.get(API_URL + 'networth', { headers: authHeader() });
  }

  getNetWorthHistory(props) {
    console.log("NetWorth", props);
    return axios.get(API_URL + 'networth/history', { headers: authHeader() });
  }

  getAverageExpenses(props) {
    console.log("MonthwiseExpenses", props);
    return axios.get(API_URL + 'expenses/average', { headers: authHeader() });
  }

  getAverageIncome(props) {
    console.log("MonthwiseIncome", props);
    return axios.get(API_URL + 'income/average', { headers: authHeader() });
  }

  getExpenses(props) {
    console.log("getExpenses", props);
    const month = props.toString();
    return axios.get(API_URL + 'expenses?date__month=' + month, { headers: authHeader() });
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
