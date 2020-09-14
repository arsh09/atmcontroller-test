import sqlite3
from sqlite3 import Error
import os
import time
from datetime import datetime

class Account:

    def __init__(self, log=True):
        
        self.log = log
        self.conn = self.connection()
        self.user = {
            "id" : -1, 
            "first" : "", 
            "last" : "", 
            "account" : -1 , 
            "pin" : -1, 
            "time" : -1
        }
            
    def connection(self):
        conn = sqlite3.connect("accounts.db")
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY, 
                first TEXT, 
                last TEXT, 
                account INTEGER,
                pin INTEGER, 
                time TIMESTAMP 
            )""")
        conn.commit()
        return conn

    def create_account(self, firstName, lastName, accountNumber, pinNumber):

        c = self.conn.cursor()
        c.execute("SELECT * FROM accounts")
        accounts = c.fetchall()
        allAccountNumbers = [ i[3] for i in accounts]
        if not accountNumber in allAccountNumbers:
            if accountNumber > 100000:
                c.execute("INSERT INTO accounts VALUES (:id, :first, :last, :account, :pin, :time)", {"id" : None, "first" : firstName, "last" : lastName, "account" : accountNumber, "pin" : pinNumber, "time" : time.time() })
                self.conn.commit()
                q = "CREATE TABLE IF NOT EXISTS account_{} (id, account, balance, time)".format(accountNumber)
                c.execute(q)
                self.conn.commit()
                self._do_logging("Acount is successfully created")
                return True
            else: 
                self._do_logging("Account number must be 6 digit")
        else:   
            self._do_logging("Account already exists", level="ERROR")
            return False 

    def get_accounts(self):

        c = self.conn.cursor()
        c.execute("SELECT * FROM accounts")
        self.conn.commit()
        return [i[3] for i in c.fetchall()]

    def validate_pin(self, account, pin):

        if account in self.get_accounts():
            c = self.conn.cursor()
            c.execute("SELECT * FROM accounts WHERE account=:account", {"account" : account})
            self.conn.commit()
            user = c.fetchone()
            self.user["id"] = 4
            if user[4] ==  pin:
                self.user["id"] = user[0]
                self.user["first"] = user[1]
                self.user["last"] = user[2]
                self.user["account"] = user[3]
                self.user["pin"] = user[4]
                self.user["time"] = user[5]
                if self.log: self._do_logging("Account pin is valid")
                return True
            else : 
                if self.log: self._do_logging("Acount pin is not valid", level="ERROR")
                return False

        else: 
            if self.log: self._do_logging("{} account is not found in database".format(account), level="ERROR")

    def check_balance(self):

        if self.user["id"] != -1:
            c = self.conn.cursor()
            c.execute( "SELECT * FROM account_{} WHERE account=:account".format(self.user["account"]), {"account" : self.user["account"] } )
            self.conn.commit()
            history = c.fetchall()
            total = 0
            for balance in history:
                total += balance[2]

            if self.log : self._do_logging("Reporting total balance for {}-{}:".format(self.user["first"], self.user["last"]) )    
            return total
        else : 
            if self.log : self._do_logging("Insert card and validate pin first", level="ERROR")    
            return None
        
    def check_history(self): 

        if self.user["id"] != -1:
            c = self.conn.cursor()
            c.execute( "SELECT * FROM account_{} WHERE account=:account".format(self.user["account"]), {"account" : self.user["account"] } )
            self.conn.commit()
            history = c.fetchall()

            transactions = []
            for balance in history:
                if (balance[2] > 0):
                    transactions.append ( (datetime.fromtimestamp(balance[3]), balance[2], "Deposit" ) )
                else:
                    transactions.append ( (datetime.fromtimestamp(balance[3]), balance[2], "Withdrawal" ) )

            if self.log : self._do_logging("Reporting transaction history for {}-{}:".format(self.user["first"], self.user["last"]) )    
            return transactions

        else : 
            if self.log : self._do_logging("Insert card and validate pin first", level="ERROR")    
            return None

    def withdraw_cash(self, amount):

        if amount > 0: 
            if self.user["id"] != -1:
                bal = self.check_balance()
                if not type(bal) == None and bal > 0:
                    c = self.conn.cursor()
                    c.execute("INSERT INTO account_{} VALUES(:id, :account, :balance, :time)".format(self.user["account"]), {"id" : None, "account" : self.user["account"] , "balance": -1*amount, "time" : time.time() } ) 
                    self.conn.commit()
                    if self.log : self._do_logging("Withdrawing {} from account # {}:".format(amount, self.user["account"] ) )    
                    return True
                else : 
                    if self.log : self._do_logging("No balance. Please deposit cash", level="ERROR")    
                    return False
            else:
                if self.log : self._do_logging("Insert card and validate pin first", level="ERROR")    
                return False

        else : 
            if self.log : self._do_logging("Withdrawal amount should be positive", level="ERROR")    
            return False
                
    def deposit_cash(self, amount):

        if amount > 0: 
            if self.user["id"] != -1:
                c = self.conn.cursor()
                c.execute("INSERT INTO account_{} VALUES(:id, :account, :balance, :time)".format(self.user["account"]), {"id" : None, "account" : self.user["account"] , "balance": 1*amount, "time" : time.time() } ) 
                self.conn.commit()
                if self.log : self._do_logging("Depositing {} in account # {}:".format(amount, self.user["account"] ) )    
                return True
            else:
                if self.log : self._do_logging("Insert card and validate pin first", level="ERROR")    
                return False

        else : 
            if self.log : self._do_logging("Depositing amount should be positive", level="ERROR")    
            return False

    def clear_user(self):
        self.user["id"] = -1
        self.user["first"] = ""
        self.user["last"] = ""
        self.user["account"] = -1
        self.user["pin"] = -1
        self.user["time"] = -1

    def _do_logging(self, msg, level="LOG"):
        if self.log:
            print "[Account-API: {}] {}".format(level, msg)



accounts = Account()
accounts.create_account("Arshad", "Khan", 100234, 1235)
accounts.validate_pin(100234,1235)
accounts.withdraw_cash(100)


print (accounts.check_history())