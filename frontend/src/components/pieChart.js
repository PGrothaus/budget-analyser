import React, {
  Component
} from "react";
import { Chart } from './charts';
import {fetch} from "../services/user.services";

/* Component */
export class PieChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      content: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.selector = this.selector.bind(this);
  }

  handleChange(newState) {
      this.setState({
        content: newState.content
      })
      console.log("handle change barchart", this.state.content);
    }

  componentDidMount() {
    console.log("Fetch data for bar chart");
    fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
  }

  selector(val) {
    console.log("selected", val.data);
    return val.data;
  }

  componentDidUpdate(prevProps) {
    if (this.props.month !== prevProps.month) {
      fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
    }
    if (this.props.collect !== prevProps.collect) {
      fetch(this.props.collect, this.props.month, this.handleChange, this.selector);
    }
  }

  render () {

    return (
            <Chart
              type="pie"
              month={this.props.month}
              data={this.state.content}
            />
  );
}
}
