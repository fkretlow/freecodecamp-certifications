class Category(object):
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self._balance = 0

    def deposit(self, amount, description=""):
        self.ledger.append({
                "amount": amount,
                "description": description
                })
        self._balance += amount

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount): return False
        self.ledger.append({
                "amount": -amount,
                "description": description
                })
        self._balance -= amount
        return True

    def get_balance(self):
        return self._balance

    def transfer(self, amount, other):
        if not self.check_funds(amount): return False
        self.ledger.append({
                "description": f"Transfer to {other.name}",
                "amount": -amount
                })
        self._balance -= amount
        other.deposit(amount, f"Transfer from {self.name}")

    def check_funds(self, amount):
        return amount <= self._balance

    def withdrawals(self):
        total = 0
        for entry in self.ledger:
            if entry["amount"] < 0 and not entry["description"].startswith("Transfer"):
                total += entry["amount"]
        return total

    def __str__(self):
        lines = []
        lines.append(f"{self.name:*^30}")
        for entry in self.ledger:
            lines.append(f"{entry['description'][:23]:<23}{entry['amount']:>7.2f}")
        lines.append(f"Total: {self._balance:.2f}")
        return "\n".join(lines)


def transpose_matrix(matrix):
    result = []
    for i in range(len(matrix[0])):
        result.append([row[i] for row in matrix])
    return result


def create_spend_chart(categories):
    columns = []
    marks = [f"{x:>3}|" for x in range(100, -1, -10)]
    columns.append(marks)

    margin = [" " for _ in range(11)] + ["-"]
    columns.append(margin)

    total_withdrawals = sum(category.withdrawals() for category in categories)
    for category in categories:
        column = []
        percentage = int(10 * category.withdrawals() / total_withdrawals) * 10
        empty_rows = (100 - percentage) // 10
        for _ in range(empty_rows): column.append(" ")
        for _ in range(percentage // 10 + 1): column.append("o")
        column.append("-")
        column += list(category.name)
        columns.append(column)
        columns.append(margin)
        columns.append(margin)

    height = max(len(column) for column in columns)
    for column in columns:
        if len(column) < height:
            width = max(len(row) for row in column)
            for _ in range(height - len(column)):
                column.append(" " * width)

    lines = ["Percentage spent by category"]
    lines += ["".join(line).rstrip() for line in transpose_matrix(columns)]
    return "\n".join(lines)
