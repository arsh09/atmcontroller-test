## ATM Controller

### Introduction

There are two classes i.e. Account and ATMController. Account tries to simulate the banking database as well as a Bank API. 

Whereas ATMController tries to expose very few functionality of Account class to the front end developer. Account

### Usage: 

You will need Python 2 only. All basic pre-installed Python libraries are used. 

```bash
    $ git clone https://github.com/arsh09/atmcontroller-test.git
    $ cd atmcontroller-test/src 
    $ python controller.py
```

If you want to set up a random accounts and their pin code. You can use the **create_account** functionality in the **account.py** file.

### Note:

I have created random accounts using a simple for-loop, where the last 4 digits of the account is the pin code for that account. Each account we create, becomes a row in SQLite table as well as a new table with 'account_{account number} is created that holds all the account transaction with time history.