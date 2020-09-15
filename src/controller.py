""" 
ATMController is our controller:
It tries to hide the functionality of the
Account class by only exposing the main functions
"""

from accounts import Account

class ATMController:

    # It assumes that ATMController Constructor 
    # works as a card reader that reads the card number 
    # and user inputted pin
    def __init__(self, account, pin, log=True):

        self.account = account
        self.pin = pin
        self._user_account = Account(log=log)

    # This method validates the read-pin and account
    # number. It may be that the card number is not valid as well. 
    def insert(self):
        return self._user_account.validate_pin(self.account, self.pin)

    # This function is called when the card is retracted from the machine
    def retract(self):
        self._user_account.clear_user()

    # When the show balance button on the user interface is clicked
    # It returns the amount of balance in the card/account
    def balance(self):
        return self._user_account.check_balance()
    
    # When the show history button on the user interface is clicked
    # It returns the complete transaction history. 
    # The user interface front-end dev can choose to show full or 
    # part of the history
    def history(self):
        return self._user_account.check_history()   

    # When user wants to deposit the card/account
    # Before depositing the cash, a cash bin might check 
    # if the inserted paper is actually a valid currency or not.
    # After that, this method should be called
    def deposit(self, amount):
        return self._user_account.deposit_cash(amount)
    
    # When user wants withdraw an amount. 
    # The front end dev does not have to worry about
    # checking if the balance in the account is greater than
    # zero or not as it is internally handled.
    # There is no withdrawal if the balance is less than zero
    def withdraw(self, amount):
        return self._user_account.withdraw_cash(amount)
    

# A function that shows the functionality of the
# overall system
def main():

    account = 100234
    pin = 1235
    card = ATMController(account, pin, log=False)
    
    isPinCorrect = card.insert()
    if isPinCorrect:

        balance = card.balance()
        print "[USER]Your current balance is: {}".format(balance)
        
        depositAmount = 100
        isDeposited = card.deposit(depositAmount)
        if isDeposited: print "[USER]You deposited an amount: {}".format(depositAmount)

        withdrawAmount = 5000
        isWithdraw = card.withdraw(withdrawAmount)
        if isWithdraw: print "[USER]You withdrew an amount: {}".format(withdrawAmount)

        balance = card.balance()
        print "[USER]Your current balance is: {}".format(balance)

        history = card.history()
        if type(history) == list: 
            for transaction in history:
                print "[USER]Time: {}\tAmount: {}\tAction: {}".format(transaction[0],transaction[1],transaction[2])

        card.retract()


if __name__ == '__main__':

    main()