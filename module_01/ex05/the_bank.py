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
        
        # check parameters not being correct type
        if not isinstance(origin, str) or not isinstance(dest, str) or not isinstance(amount, float):
           return False
        
        # get origin and dest account objects
        origin_acc = None
        dest_acc = None
        for account in self.accounts:
            if account.name.lower() == origin.lower():
                origin_acc = account
            if account.name.lower() == dest.lower():
                dest_acc = account
        if not origin_acc or not dest_acc:
            # one or both account names are not registered in the bank
            return False
        

        # Check if any of the accounts is corrupted
        origin_corrupted, origin_fails = self.is_corrupted(origin_acc)
        dest_corrupted, dest_fails = self.is_corrupted(dest_acc)
        if origin_corrupted or dest_corrupted:
            return False
        
        # invalid if amount < 0 or if the amount is larger than the balance of the account
        if amount < 0 or amount > origin_acc.value:
            return False
        
        # transfer the amount
        origin_acc.transfer(-amount)
        dest_acc.transfer(amount)
        return True

    def fix_account(self, name):
        """ fix account associated to name if corrupted
            @name: str(name) of the account
            @return True if success, False if an error occured
        """
        # check parameters name being correct type
        if not isinstance(name, str):
           return False
        
        # get name's account object
        target_acc = None
        for account in self.accounts:
            if account.name.lower() == name.lower():
                target_acc = account
        if target_acc:
            acc_corrupted, acc_fails = self.is_corrupted(target_acc)
            if acc_corrupted:
                # Account is corrupted
                if 'value' in acc_fails:
                    val = getattr(target_acc, 'value', None)
                    if val.isdecimal() or val.isdigit():
                        setattr(target_acc, 'value', float(val))
                    else:
                        setattr(target_acc, 'value', 0.0)
                if 'id' in acc_fails:
                    i = getattr(target_acc, 'id', None)
                    if i.isdigit():
                        setattr(target_acc, 'id', int(i))
                    else:
                        setattr(target_acc, 'id', Account.ID_COUNT)
                        Account.ID_COUNT += 1
                    
                if "even" in acc_fails and 'zip' in acc_fails:
                    setattr(target_acc, 'zip', '')
                elif "even" in acc_fails and 'addr' in acc_fails:
                    setattr(target_acc, 'address', '') 
                
            else:
                # Account in not corrupted
                return False
            return True    
        else:    
            # account is not registered in the bank
            return False
    
    def is_corrupted(self, acc:Account):
        # Initialize fail list
        fails =[]

        # get accounts attributes
        acc_attrs = list(acc.__dict__.keys())

        # account attributes are even 
        if len(acc_attrs) % 2 == 0:
            fails.append('even')
        
        # an attribute starting with 'b'
        if sum(attribute[0].lower() == 'b' for attribute in acc_attrs) > 0: 
            fails.append('b')

        # no attribute starting with 'zip' or 'addr'
        if sum(attribute[0:3].lower() == 'zip' for attribute in acc_attrs) == 0:
            fails.append('zip')
        if sum(attribute[0:4].lower() == 'addr' for attribute in acc_attrs) == 0:
            fails.append('addr')
        
        # no attribute name, id and value,
        if 'name' not in acc_attrs or 'id' not in acc_attrs or 'value' not in acc_attrs:
            fails.append('name')

        # name not being a string,
        if not isinstance(acc.name, str):
            fails.append('name_str')
            
        # id not being an int
        if not isinstance(acc.id, int):
            fails.append('id')
            
        # value not being an int or a float.
        if not isinstance(acc.value, int) and not isinstance(acc.value, float):
            fails.append('value')
        
        if (len(fails) > 0):
            return True, fails
        else:
            return False
