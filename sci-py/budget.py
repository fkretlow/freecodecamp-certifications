class Category(object):
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self._balance = 0

    def deposit(self, amount, description=""):
        self.ledger.append({ "amount": amount, "description": description })
        self._balance += amount

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount): return False
        self.ledger.append({ "amount": -amount, "description": description })
        self._balance -= amount
        return True

    def get_balance(self):
        return self._balance

    def transfer(self, amount, other):
        if not self.check_funds(amount): return False
        self.withdraw(amount, f"Transfer to {other.name}")
        other.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        return amount <= self._balance

    def total_spent(self):
        total = 0
        for entry in self.ledger:
            if entry["amount"] < 0 and not entry["description"].startswith("Transfer"):
                total += entry["amount"]
        return total

    def __str__(self):
        lines = [f"{self.name:*^30}"]
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
    labelling = [f"{x:>3}|" for x in range(100, -1, -10)]
    gap = list(" " * 11) + ["-"]
    columns = [labelling, gap]

    total_spent = sum(category.total_spent() for category in categories)
    for category in categories:
        column = []
        percentage = int(10 * category.total_spent() / total_spent) * 10
        for _ in range((100 - percentage) // 10): column.append(" ")
        for _ in range(percentage // 10 + 1): column.append("o")
        column.append("-")
        column += list(category.name)
        columns.append(column)
        columns.append(gap)
        columns.append(gap)

    # Make all columns equally tall.
    height = max(len(column) for column in columns)
    for column in columns:
        if len(column) < height:
            width = max(len(row) for row in column)
            for _ in range(height - len(column)):
                column.append(" " * width)

    # Remove .rstrip() for the tests on repl.it to succeed.
    lines = ["Percentage spent by category"] \
          + ["".join(line).rstrip() for line in transpose_matrix(columns)]
    return "\n".join(lines)
