import React from "react";
import MaterialTable from 'material-table';

import {formatAccountValueObject} from "../helpers/formats";
import {formatTransactionObject} from "../helpers/formats";
import {columnsAccountTable} from "../constants";
import {columnsTransactionTable} from "../constants";


export function AccountTable(props) {
  console.log("Rendering account table", props);
  const elems = props.elems;
  elems.map((elem) => formatAccountValueObject(elem));
  return (
    <MaterialTable
    title="Accounts"
    columns={columnsAccountTable}
    data={elems}
    />
  )
}

export function TransactionTable(props) {
  console.log("Rendering transaction table", props);
  const elems = props.elems;
  elems.map((elem) => formatTransactionObject(elem));
  return (
    <MaterialTable
      title="Transactions"
      columns={columnsTransactionTable}
      data={elems}
      />
  )
}
