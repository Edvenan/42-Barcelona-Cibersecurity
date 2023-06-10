from the_bank import Account, Bank

if __name__ == "__main__":
    bank = Bank()
    acc_valid_1 = Account('Sherlock Holmes',
                          zip='NW1 6XE',
                          addr='221B Baker street',
                          value=1000.0)
    acc_invalid_2 = Account('James Watson',
                          zip='NW1 6XE',
                          addr='221B Baker street',
                          value=25000.0,
                          info=None)
    
    acc_invalid_3 = Account("Douglass",
                            zip='42',
                            addr='boulevard bessieres',
                            value=42,
                            home = 'my home')
    acc_valid_4 = Account("Adam",
                            value=42,
                            zip='0',
                            addr='Somewhere')
    acc_valid_5 = Account("Bender Bending Rodríguez",
                            zip='1',
                            addr='Mexico',
                            value=42)
    acc_valid_6 = Account("Charlotte",
                            zip='2',
                            addr='Somewhere in the Milky Way',
                            value=42)
    acc_invalid_7 = Account("Edouard",
                            zip='3',
                            addr='France',
                            value=42,
                            b="to be fixed")
    acc_invalid_8 = Account("Edouard",
                            zip='30',
                            addr='Paris',
                            value=4224,
                            b="to be fixed")
    
    # Test adding accounts to bank
    print("Test adding accounts to bank:")
    print("Adding 'acc_valid_1': ",bank.add(acc_valid_1))
    print("Adding 'acc_invalid_2': ",bank.add(acc_invalid_2))
    print("Adding 'acc_invalid_3': ",bank.add(acc_invalid_3))
    print("Adding 'acc_valid_4': ",bank.add(acc_valid_4))
    print("Adding 'acc_valid_5': ",bank.add(acc_valid_5))
    print("Adding 'acc_valid_6': ",bank.add(acc_valid_6))
    print("Adding 'acc_invalid_7': ",bank.add(acc_invalid_7))
    print("Adding 'acc_invalid_8': ",bank.add(acc_invalid_8))
    
    """
    print(bank.accounts[2].__dict__)
    setattr(bank.accounts[2],'id','23')
    print(bank.accounts[2].__dict__)
    
    print(bank.transfer('Sherlock Holmes', "Douglass", 1000.0))
    print(bank.fix_account('Douglass'))
    print(bank.accounts[2].__dict__)
    print(bank.transfer('Sherlock Holmes', "Douglass", 1000.0))
    print(bank.accounts[2].name," -> value:. ",bank.accounts[2].value)
    print(bank.accounts[0].name," -> value:. ",bank.accounts[0].value)
    print(bank._Bank__is_corrupted(bank.accounts[1]))
    print(bank.accounts[1].__dict__)
    print(bank.fix_account('James Watson'))
    print(bank._Bank__is_corrupted(bank.accounts[1]))
    print(bank.accounts[1].__dict__)
    print(bank.fix_account("Douglass"))
    print(bank.accounts[2].__dict__)
    print(bank.accounts[0].__dict__)
    print(bank.transfer('Sherlock Holmes', "Douglass", 1000.0))
    print(bank.accounts[2].name," -> value:. ",bank.accounts[2].value)
    print(bank.accounts[0].name," -> value:. ",bank.accounts[0].value)
    print(bank.transfer('Sherlock Holmes', "Douglass", 1000.0))
    print(bank.transfer('Douglass', 'Sherlock Holmes', 1000.0))
    print(bank.accounts[2].name," -> value:. ",bank.accounts[2].value)
    print(bank.accounts[0].name," -> value:. ",bank.accounts[0].value) """
