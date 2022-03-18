class Category:
    def __init__(self, category):
        self.balance = 0
        self.ledger = list()
        self.category = category

    def __str__(self):
        finalStr = ""

        categoryLen = len(self.category)
        remainingSpace = int((30 - categoryLen) / 2)
        titleStr = f'{remainingSpace * "*"}{self.category}{remainingSpace * "*"}\n'

        historyStr = ""
        for item in self.ledger:
            descLen = len(item["description"][:23])
            itemAmt = format(item["amount"], ".2f")
            amountLen = len(str(itemAmt)[:7])
            spaces = int(30 - descLen - amountLen) * " "
            historyStr += f"{item['description'][:23]}{spaces}{itemAmt}\n"

        totalStr = f"Total: {self.balance}"

        finalStr = f"{titleStr}{historyStr}{totalStr}"
        return finalStr

    def deposit(self, amount, description=""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append(
                {
                    "amount": -1 * amount,
                    "description": description,
                }
            )
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category_instance):
        if self.check_funds(amount):
            self.ledger.append(
                {
                    "amount": -1 * amount,
                    "description": f"Transfer to {category_instance.category}",
                }
            )
            category_instance.ledger.append(
                {"amount": amount, "description": f"Transfer from {self.category}"}
            )
            self.balance -= amount
            category_instance.balance += amount
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.balance < amount:
            return False
        else:
            return True


def create_spend_chart(categories):
    finalStr = "Percentage spent by category\n"

    spendingTotalForCategoryList = list()
    percentagesForspending = list()
    categoriesStringList = list()

    for category in categories:
        spendingTotal = 0
        for item in category.ledger:
            itemAmt = format(item["amount"], ".2f")
            if "-" in itemAmt:
                spendingTotal += abs(float(itemAmt))
        spendingTotal = int(spendingTotal)
        spendingTotalForCategoryList.append(spendingTotal)

        categoriesStringList.append(category.category)

    totalOfSpendingList = sum(spendingTotalForCategoryList)

    for item in spendingTotalForCategoryList:
        percentageValue = int((item / totalOfSpendingList) * 100)
        roundedPercentageValue = round(percentageValue, 2)
        percentagesForspending.append(roundedPercentageValue)

    for i in range(100, -10, -10):
        finalStr += str(i).rjust(3) + "|"

        for j in percentagesForspending:
            if j >= i:
                finalStr += f" o "
            else:
                finalStr += f"   "

        finalStr += " \n"

    finalStr += "    " + "-" * (len(percentagesForspending) * 3 + 1) + "\n"

    for i in range(len(max(categoriesStringList, key=len))):
        finalStr += "    "
        for categoryStr in categoriesStringList:
            try:
                if i < len(categoryStr):
                    finalStr += f" {categoryStr[i]} "
                else:
                    finalStr += f"   "
            except:
                continue

        finalStr += " \n"

    return finalStr.rstrip("\n")
