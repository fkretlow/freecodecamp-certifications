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
    let result = { change: [] };

    if (amount === this._total()) {
      // This part of the specification is a little peculiar.
      // Why give all the empty coin stacks? Oh well...
      result.status = "CLOSED";
      for (const [value, count] of this.cash) {
        result.change.push([
          VALUE_TO_UNIT.get(value),
          round_float(count * value, 2),
        ]);
        this.cash.set(value, 0);
      }

    } else {
      const change = this._in_cash(0, amount);

      if (change === IMPOSSIBLE) {
        result.status = "INSUFFICIENT_FUNDS";

      } else {
        result.status = "OPEN";
        for (const [value, count] of change) {
          result.change.push([
            VALUE_TO_UNIT.get(value),
            round_float(count * value, 2),
          ])
          this.cash.set(value, this.cash.get(value) - count);
        }
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
    // The algorithm finds a way to give out the requested amount as a set of
    // coins and bills, depending on which denominations are available.
    // The problem is a variant of the knapsack problem where the knapsack must
    // be filled exactly. We have a basic recursive solution where we try to
    // take as many pieces of the biggest available denomination as possible,
    // backtracking only when we hit a dead end.
    if (amount === 0) {
      return DONE;
    } else if (value_index >= VALUES.length) {
      return IMPOSSIBLE;
    }

    const value = VALUES[value_index];
    for (let count = Math.min(Math.floor(amount / value), this.cash.get(value));
         count >= 0;
         --count) {
      let rest = round_float(amount - count * value, 2);
      let sub_solution = this._in_cash(value_index + 1, rest);

      if (sub_solution === DONE) {
        return [ [value, count] ];
      } else if (sub_solution === IMPOSSIBLE) {
        continue;
      } else {
        if (count > 0) {
          return [ [value, count], ...sub_solution ];
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
