#!/usr/bin/env python

'''
The goals of this exercise is to discover new built-in functions and deepen your
class manipulation and to be aware of possibility to modify instanced objects.
In this exercise you learn how to modify or add attributes to an object.


'''


class Account(object):

    ID_COUNT = 1
    
    def __init__(self, name, **kwargs):
        self.__dict__.update(kwargs)

        self.id = self.ID_COUNT
        Account.ID_COUNT += 1
        self.name = name
        if not hasattr(self, 'value'):
            self.value = 0
        if self.value < 0:
            raise AttributeError("Attribute value cannot be negative.")
        if not isinstance(self.name, str):
            raise AttributeError("Attribute name must be a str object.")

    def transfer(self, amount):
        self.value += amount
        

class Bank(object):
    """The bank"""
    def __init__(self):
        self.accounts = []

    def add(self, new_account):
        """ Add new_account in the Bank
            @new_account: Account() new account to append
            @return True if success, False if an error occured
        """
        # test if new_account is an Account() instance and if
        # it can be appended to the attribute accounts
        if not isinstance(new_account, Account) or new_account in self.accounts:
            # The account to be added is either not an Account object
            # or it already exists
            return False
        else:
            self.accounts.append(new_account)
    
    def transfer(self, origin, dest, amount):
        """" Perform the fund transfer
            @origin: str(name) of the first account
            @dest: str(name) of the destination account
            @amount: float(amount) amount to transfer
            @return True if success, False if an error occured
        """
        # ... Your code ...
        origin_corrupted = False
        dest_corrupted = False
        
        # corrupted if
        # account attributes are even 
        if len(origin.__dict__) % 2 == 0:
            origin_corrupted = True
        if len(dest.__dict__) % 2 == 0:
            dest_corrupted = True
        
        #• an attribute starting with b,
        if sum(char[0].lower() == 'b' for char in origin.__dict__) > 0: 
            origin_corrupted = True
        if sum(char[0].lower() == 'b' for char in dest.__dict__) > 0: 
            dest_corrupted = True
            
        #• no attribute starting with zip or addr,
        if sum(char[0:3].lower() == 'zip' for char in origin.__dict__) == 0 \
            or sum(char[0:4].lower() == 'addr' for char in origin.__dict__) == 0:
            origin_corrupted = True
        if sum(char[0:3].lower() == 'zip' for char in dest.__dict__) == 0 \
            or sum(char[0:4].lower() == 'addr' for char in dest.__dict__) == 0:
            dest_corrupted = True
        
        #• no attribute name, id and value,
        #• name not being a string,
        #• id not being an int,
        #• value not being an int or a float.
        #  stores enough money to complete the transfer.

    def fix_account(self, name):
        """ fix account associated to name if corrupted
            @name: str(name) of the account
            @return True if success, False if an error occured
        """
        # ... Your code ...
