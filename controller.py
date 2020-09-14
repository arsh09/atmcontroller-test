
import time 

class ATMController: 

    def __init__(self):

        # A variable to hold the current user input
        self._users = [
            { "key" : 0, "name" : "Arshad" , "pin" : 1234 },
            { "key" : 1, "name" : "John" , "pin" : 3213 },
            { "key" : 2, "name" : "Shereen" , "pin" : 4322 },
            { "key" : 3, "name" : "David" , "pin" : 5433 },
            { "key" : 4, "name" : "Peter" , "pin" : 1234 },
        ]

        self._user = {},

    def _print_message(self, msg, level):
        print "[%s] - %s" % (level, msg)

    def validate_pin(self): 
        self._print_message("Please enter your pin", "INFO")
        N = 4
        for i in range(1,N):
            pin = int(raw_input())
            if pin == self._user["pin"]:
                self._print_message("Correct pin is entered", "LOG")
                return True
            else : 
                if N - i - 1 > 0:
                    self._print_message("Wrong pin. %d tries left" % (N - i - 1), "ERROR")
                else : 
                    break 

        return False

    def choose_user(self) : 
        self._user = self._users[0]

    def select_account(self): 
        

    def control_loop(self): 
        
        self.choose_user()
        self.validate_pin()


def main():

    controller = ATMController()    
    controller._control_loop()

if __name__ == '__main__':
    main()