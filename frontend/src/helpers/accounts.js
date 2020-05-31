export function is_retirement_account(elem) {
  return elem.account.type.type === "RETIREMENT"
}

export function is_liquid_account(elem) {
  return elem.account.type.type === "NORMAL" || elem.account.type.type === "INVESTMENT"
}


export function sum_account_values(elems) {
  return elems.reduce(function(cnt, o){ return cnt + o.value; }, 0)
}
