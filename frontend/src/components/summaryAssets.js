import React, { Component } from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar'
import UserService from "../services/user.services"
import {fetch} from "../services/user.services";
import {formatPct} from "../helpers/formats";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

export default class SummaryAssets extends Component {
  constructor(props) {
    super(props);
    this.state = {
      assets: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.selector = this.selector.bind(this);
    this.fetch_all = this.fetch_all.bind(this);
  }

  handleChange(newState) {
    console.log("New state assets", newState);
    this.setState({assets: newState.content});
  }

  selector(val) {return val.data}

  fetch_all() {
    fetch(UserService.getAssetList, 0, this.handleChange, this.selector);
  }

  componentDidMount() {
    this.fetch_all();
  }

  render() {
    const assets = this.state.assets;
    console.log("Rendering assets", assets);
    return <AssetsRenderer assets={assets} />
  }
}


function AssetsRenderer(props) {
  const assets = props.assets
  const assetList = assets.map((asset) => <Asset asset={asset} />)
  return (<Container >
          <Header />
          {assetList}
          </Container >
        );
}

function Asset(props) {
  const asset = props.asset;
  const pct_paid = Number((100 * asset.percentage_paid).toFixed(1));
  return (
    <Row>
    <Col>
    {asset.asset.name}
    </Col>
    <Col>
    {asset.value} {asset.asset.currency.code}
    </Col>
    <Col>
    {asset.asset.cost} {asset.asset.currency.code}
    </Col>
    <Col md={6}>
    <ProgressBar variant="success" now={pct_paid} label={`${pct_paid}%`}/>
    </Col>
    </Row>
  );
}

function Header() {
  return (
    <Row>
    <Col>
    Asset
    </Col>
    <Col>
    Value
    </Col>
    <Col>
    Cost
    </Col>
    <Col md={6}>
    Percentage Paid
    </Col>
    </Row>
  );
}
