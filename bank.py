class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, '*') + '\n'
        items = ''
        for entry in self.ledger:
            description = entry['description'][:23]
            amount = f"{entry['amount']:.2f}"[:7]
            line = description + amount.rjust(30 - len(description))
            items += line + '\n'
        total = f'Total: {self.get_balance():.2f}'
        return title + items + total


def create_spend_chart(categories):
    withdrawals = []
    for category in categories:
        spent = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        withdrawals.append(spent)

    total_spent = sum(withdrawals)
    percentages = [(spent / total_spent) * 100 // 10 * 10 for spent in withdrawals]

    chart = 'Percentage spent by category\n'

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + '|'
        for percentage in percentages:
            if percentage >= i:
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'

    chart += '    ' + '-' * (len(categories) * 3 + 1) + '\n'

    max_len = max(len(category.name) for category in categories)
    names = [category.name.ljust(max_len) for category in categories]

    for i in range(max_len):
        chart += '    '
        for name in names:
            chart += ' ' + name[i] + ' '
        chart += ' \n'
        if i != max_len - 1:
            pass

    return chart.rstrip('\n')
