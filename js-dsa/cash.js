const round_float = (n, places) => parseFloat(n.toFixed(places));
const DONE = 0;
const IMPOSSIBLE = -1;


const VALUE_TO_UNIT = new Map([
  [ 0.01, 'PENNY' ],
  [ 0.05, 'NICKEL' ],
  [ 0.1,  'DIME' ],
  [ 0.25, 'QUARTER' ],
  [ 1,    'ONE' ],
  [ 5,    'FIVE' ],
  [ 10,   'TEN' ],
  [ 20,   'TWENTY' ],
  [ 100,  'ONE HUNDRED' ],
]);

const UNIT_TO_VALUE = new Map([
  [ 'PENNY',       0.01 ],
  [ 'NICKEL',      0.05 ],
  [ 'DIME',        0.1 ],
  [ 'QUARTER',     0.25 ],
  [ 'ONE',         1 ],
  [ 'FIVE',        5 ],
  [ 'TEN',         10 ],
  [ 'TWENTY',      20 ],
  [ 'ONE HUNDRED', 100 ],
]);

const VALUES = [ 100, 20, 10, 5, 1, .25, .1, .05, .01 ];


class CashInDrawer {
  // A CashInDrawer has-a Map that associates counts of coins/bills with
  // denominations (values). To solve the problem we only need a constructor
  // and a method to give out cash.
  constructor(units_and_amounts) {
    // The constructor builds the Map from a list of denominations and amounts
    // like [ [ 'PENNY', 0.01 ], ... ].
    this.cash = new Map();
    for (const [unit, amount] of units_and_amounts) {
      const value = UNIT_TO_VALUE.get(unit);
      const count = Math.round(amount / value);
      this.cash.set(value, count);
    }
  }

  give_change(amount) {
    // Return an object with a status and the requested amount in cash, if possible:
    // { status: 'OPEN', change: [ [ 'PENNY', 0.01 ], ... ] }
    let result = {};

    if (amount === this._total()) {
      // This part of the specification is a little peculiar.
      // Why give all the empty coin stacks? Oh well...
      result.status = "CLOSED";
      result.change = [];
      for (const [ value, count ] of this.cash) {
        result.change.push([
          VALUE_TO_UNIT.get(value),
          round_float(count * value, 2),
        ]);
      }

      for (const value of this.cash.keys()) {
        this.cash.set(value, 0);
      }
    } else {
      const in_cash = this._in_cash(0, amount);

      if (in_cash === IMPOSSIBLE) {
        result.status = "INSUFFICIENT_FUNDS";
        result.change = [];
      } else {
        for (const [value, count] of in_cash) {
          this.cash.set(value, this.cash.get(value) - count);
        }

        result.status = "OPEN";
        result.change = in_cash.map(([value, count]) => {
          return [
            VALUE_TO_UNIT.get(value),
            count * value,
          ];
        });
      }
    }

    return result;
  }

  _total() {
    let total = 0;
    for (let value of this.cash.keys()) {
      total += this.cash.get(value) * value;
    }
    return total;
  }

  _in_cash(value_index, amount) {
    // This algorithm finds a way to give out the requested amount in terms
    // of the available coins and bills.
    // The problem is a variant of the bin-packing problem. We have a basic
    // recursive solution where we check the biggest denominations first, and
    // backtrack only when we hit a dead end.
    if (amount === 0) {
      return DONE;
    } else if (value_index >= VALUES.length) {
      return IMPOSSIBLE;
    }

    const value = VALUES[value_index];
    let max_count = Math.floor(amount / value);
    if (max_count > this.cash.get(value)) max_count = this.cash.get(value);

    for (let count = max_count; count >= 0; --count) {
      let rest = round_float(amount - count * value, 2);
      let sub_solution = this._in_cash(value_index + 1, rest);

      if (sub_solution === DONE) {
        return [ [ value, count ] ];
      } else if (sub_solution === IMPOSSIBLE) {
        continue;
      } else {
        if (count > 0) {
          return [ [ value, count ], ...sub_solution ];
        } else {
          return sub_solution;
        }
      }
    }

    return IMPOSSIBLE;
  }
};


function checkCashRegister(price, cash, cid) {
  cid = new CashInDrawer(cid);
  return cid.give_change(cash - price);
}


console.log(checkCashRegister(3.26, 100, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]]))

console.log(checkCashRegister(19.5, 20, [["PENNY", 0.5], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 0], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]]))
