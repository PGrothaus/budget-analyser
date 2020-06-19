

export function formatCLP(val) {
  if (! isNaN(val)) {
    var formatter = new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency: 'CLP',
    });
    return formatter.format(val);
  }
  return val
}


export function formatPct(val) {
  return Number(val.toFixed(1)).toString() + "%"
}


export function formatAccountValueObject(elem) {
  elem.gains = "n.a.";
  if (elem.invested_money > 0) {
    elem.gains = elem.value - elem.invested_money;
    elem.gains = formatCLP(elem.gains);
    elem.invested_money = formatCLP(elem.invested_money);}
  if (elem.gains === "n.a.") {elem.invested_money = "n.a."}
  elem.value = formatCLP(elem.value);
  return elem
}


export function formatTransactionObject(elem) {
  elem.amount = formatCLP(elem.amount);
  return elem
}
