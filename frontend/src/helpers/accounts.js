export function is_retirement_account(elem) {
  return elem.account.type.type === "RETIREMENT"
}

export function is_liquid_account(elem) {
  return elem.account.type.type === "NORMAL" || elem.account.type.type === "INVESTMENT"
}


export function sum_account_values(elems) {
  return elems.reduce(function(cnt, o){ return cnt + o.value; }, 0)
}


export function sum_account_investments(elems) {
  return elems.reduce(function(cnt, o){ return cnt + amount_invested(o); }, 0)
}


function amount_invested(elem) {
  console.log("amount invested", elem);
  if (elem.invested_money === null) {
    return elem.value
  }
  return elem.invested_money
}
