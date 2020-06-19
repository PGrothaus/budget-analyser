export const columnsAccountTable =[
  {title: 'Bank', field: 'account.bank.name'},
  {title: 'Account', field: 'account.name'},
  {title: 'Money Invested', field: 'invested_money'},
  {title: 'Value Investment', field: 'value'},
  {title: 'Gains/Losses', field:'gains'},
];

export const columnsTransactionTable = [
  {title: 'Description', field: 'description'},
  {title: 'Amount', field: 'amount'},
  {title: 'Group', field: 'category.group.name'},
  {title: 'Category', field: 'category.name'}
];
