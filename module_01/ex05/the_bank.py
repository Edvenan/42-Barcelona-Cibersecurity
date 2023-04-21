#!/usr/bin/env python

'''
The goals of this exercise is to discover new built-in functions and deepen your
class manipulation and to be aware of possibility to modify instanced objects.
In this exercise you learn how to modify or add attributes to an object.
'''

###############################
# ACCOUNT CLASS
###############################
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

###############################        
# BANK CLASS
###############################
class Bank(object):
    """The bank"""
    def __init__(self):
        self.accounts = []
    
    ###############################
    # Bank.add() function         #
    ###############################
    def add(self, new_account):
        """ Add new_account in the Bank
            @new_account: Account() new account to append
            @return True if success, False if an error occured
        """
        # test if new_account is an Account() instance and if
        # it doen's exist in the bank's accounts list
        if not isinstance(new_account, Account) or \
            sum(account.name == new_account.name for account in self.accounts if hasattr(account,'name')) >= 1:
            # The account to be added is either not an Account object
            # or it already exists
            return False
        else:
            # add the account to the bank's accounts list
            self.accounts.append(new_account)
            return True
    
    ############################
    # Bank.transfer() function #
    ############################
    def transfer(self, origin, dest, amount):
        """" Perform the fund transfer
            @origin: str(name) of the first account
            @dest: str(name) of the destination account
            @amount: float(amount) amount to transfer
            @return True if success, False if an error occured
        """
        # var initialization
        origin_corrupted = False
        dest_corrupted = False
        
        # check arguments not being correct type
        if not isinstance(origin, str) or not isinstance(dest, str) or not isinstance(amount, float):
           return False
        
        # get origin and dest account objects
        origin_acc = None
        dest_acc = None
        for account in self.accounts:
            if not hasattr(account, 'name'):
                # if element 'account' has no name, skip it
                continue
            if isinstance(account.name, str) and account.name.lower() == origin.lower():
                origin_acc = account
            if isinstance(account.name, str) and account.name.lower() == dest.lower():
                dest_acc = account
        if not origin_acc or not dest_acc:
            # one or both account names are not registered in the bank
            return False

        # Check if any of the accounts is corrupted
        origin_corrupted, origin_fails = self.__is_corrupted(origin_acc)
        dest_corrupted, dest_fails = self.__is_corrupted(dest_acc)
        if origin_corrupted or dest_corrupted:
            return False
        
        # invalid if amount < 0 or if the amount is larger than the balance of the account
        if amount < 0 or amount > origin_acc.value:
            return False
        
        # Succes. Transfer the amount
        origin_acc.transfer(-amount)
        dest_acc.transfer(amount)
        return True
    
    ###############################
    # Bank.fix_account() function #
    ###############################
    def fix_account(self, name):
        """ fix account associated to name if corrupted
            @name: str(name) of the account
            @return True if success, False if an error occured
        """
        # check parameters name being correct type
        #if not isinstance(name, str):
        #   return False
        
        # get name's account object
        target_acc = None
        for account in self.accounts:
            if not hasattr(account, 'name') and hasattr(account, 'id'):
                setattr(account, 'name', 'Unknown'+str(account.id))
            elif not hasattr(account, 'name'):
                setattr(account, 'name', 'Unknown'+str(Account.ID_COUNT))
                Account.ID_COUNT += 1
            if isinstance(account.name, str) and isinstance(name, str):
                if account.name.lower() == name.lower():
                    target_acc = account
            elif isinstance(account.name, int) and isinstance(name, int):
                if account.name == name:
                    target_acc = account
        if target_acc:
            acc_corrupted, acc_fails = self.__is_corrupted(target_acc)
            if acc_corrupted:
                # Account is corrupted
                # while is corrupted, apply fixes
                while(acc_corrupted):
                    # if the only issue is 'even',we fix it. Otherwise, 
                    # fix the others first
                    if len(acc_fails) == 1 and 'even' in acc_fails:
                        # create a dummy attr calledd 'other'
                        setattr(target_acc, 'other', '')
                    else:
                        # we fix the rest of issues
                        if "b" in acc_fails:
                            # get all accounts attributes
                            acc_attrs = list(target_acc.__dict__.keys())
                            # go through each attribute and check if it starts with a 'b'
                            for attribute in acc_attrs:
                                # identify the attribute starting with 'b'
                                if attribute[0].lower() == 'b' and len(attribute) > 1:
                                    # identified and attr name is longer than 'b'
                                    # we strip the 'b' from the attr name, create a new attr with such name,
                                    # we copy the old attr val into the new attr, and delete the old/wrong attr
                                    if (attribute[1:] in acc_attrs):
                                        # if attr name after stripping 'b' is equal to the name of another
                                        # existing attribute, we add a prefix 'fixed_'to the stripped name
                                        if (attribute[1:] == 'value'):
                                            setattr(target_acc, 'value', getattr(target_acc, attribute, None))
                                        else:    
                                            setattr(target_acc, 'fixed_'+attribute[1:], getattr(target_acc, attribute, None))
                                        delattr(target_acc, attribute)
                                    else:
                                        # if attr name adter stripping 'b' doesn't exist, we create a new attr,
                                        # copy the old attr value into the new one, and delete old/wrong attr
                                        setattr(target_acc, attribute[1:], getattr(target_acc, attribute, None))
                                        delattr(target_acc, attribute)
                                elif attribute[0].lower() == 'b' and len(attribute) == 1:
                                    # identified but attr name is only 1 char long
                                    # create a new attr with dummy name 'fixed attribute', copy the attr val
                                    # in the new attr, and delete the wrong attr
                                    setattr(target_acc, 'fixed attribute', getattr(target_acc, attribute, None))
                                    delattr(target_acc, attribute)
                        if 'value_type' in acc_fails:
                            val = getattr(target_acc, 'value', None)
                            if  isinstance(val, str):
                                try:
                                    setattr(target_acc, 'value', float(val))
                                except ValueError:
                                    setattr(target_acc, 'value', 0.0)
                            else:
                                setattr(target_acc, 'value', 0.0)
                        if 'id_int' in acc_fails:
                            #i = getattr(target_acc, 'id', None)
                            #if i.isdigit():
                            #    setattr(target_acc, 'id', int(i))
                            #else:
                                setattr(target_acc, 'id', Account.ID_COUNT)
                                Account.ID_COUNT += 1
                        if "name_str" in acc_fails:
                            setattr(target_acc, 'name', str(name))
                        if "no_name" in acc_fails:
                            setattr(target_acc, 'name', name)
                        if "no_id" in acc_fails:
                            setattr(target_acc, 'id', Account.ID_COUNT)
                            Account.ID_COUNT += 1
                        if "no_value" in acc_fails:
                            setattr(target_acc, 'value', 0.0)
                        if "addr" in acc_fails:
                            acc_attrs = list(target_acc.__dict__.keys())
                            if 'addr' not in  acc_attrs:
                                setattr(target_acc, 'addr', '')
                            else:
                                # during fixing attr 'addr' has been added
                                # do nothing
                                pass
                        if "zip" in acc_fails:
                            acc_attrs = list(target_acc.__dict__.keys())
                            if 'zip' not in  acc_attrs:
                                setattr(target_acc, 'zip', 0)
                            else:
                                # during fixing attr 'zip' has been added
                                # do nothing
                                pass
                    
                    # Check if account is still corrupted
                    acc_corrupted, acc_fails = self.__is_corrupted(target_acc)
                
                # If out of the loop, fix is completed
                return True
                
            else:
                # Account in not corrupted
                return False
            return True    
        else:    
            # account is not registered in the bank
            return False
    
    ##########################################
    # Bank.__is_corrupted() Private function #
    ##########################################
    def __is_corrupted(self, acc:Account):
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
        if 'name' not in acc_attrs:
            fails.append('no_name')
        if 'id' not in acc_attrs:
            fails.append('no_id')
        if 'value' not in acc_attrs:
            fails.append('no_value')
            
        # name not being a string,
        if not isinstance(acc.name, str):
            fails.append('name_str')
            
        # id not being an int
        if hasattr(acc, 'id') and not isinstance(acc.id, int):
            fails.append('id_int')
            
        # value not being an int or a float.
        if hasattr(acc, 'value') and not isinstance(acc.value, int) and not isinstance(acc.value, float):
            fails.append('value_type')
        
        if (len(fails) > 0):
            return True, fails
        else:
            return False, []
