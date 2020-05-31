

export function formatCLP(val) {
  var formatter = new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'CLP',
  });
  return formatter.format(val);
}


export function formatPct(val) {
  return Number(val.toFixed(1)).toString() + "%"
}
