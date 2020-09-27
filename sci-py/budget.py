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

    def __str__(self):
        lines = []
        lines.append(f"{self.name:*^30}")
        for entry in self.ledger:
            lines.append(f"{entry['description'][:23]:<23}{entry['amount']:>7.2f}")
        lines.append(f"Total: {self._balance:.2f}")
        return "\n".join(lines)


if __name__ == "__main__":
    food = Category("Food")
    clothing = Category("Clothing")
    food.deposit(1000, "initial deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(18.89, "restaurant and more food")
    food.transfer(50, clothing)

    print(food)
    print(clothing)
