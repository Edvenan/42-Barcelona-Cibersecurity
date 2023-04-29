from csvreader import CsvReader

#####################
# MAIN
#####################
def main():
     
    print("###############################")
    print("# INVALID TEST: file not found")
    print("###############################")
    with CsvReader('mbad.csv',skip_top=1005,skip_bottom=19, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")

    print("#################################################")
    print("# VALID TEST:  'skip_top'/'skip_bottom' too high")
    print("#################################################")
    with CsvReader('good.csv',skip_top=1005,skip_bottom=19, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())

    print("\n")

    print("###############################")
    print("# INVALID TEST: Corrupted file")
    print("###############################")
    with CsvReader('bad.csv',skip_top=0,skip_bottom=0, header=True) as file:
        if file == None:
            print("File is corrupted")
        else:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")

    print("###############################")
    print("# VALID TEST: Good file")
    print("###############################")
    with CsvReader('good.csv',skip_top=0,skip_bottom=0, header=False) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")
    
    print("###############################")
    print("# VALID TEST: 1 line file")
    print("###############################")
    
    with CsvReader('ugly.csv',skip_top=0,skip_bottom=0, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")
    
    print("###############################")
    print("# INVALID TEST: empty file")
    print("###############################")

    with CsvReader('empty.csv',skip_top=0,skip_bottom=0, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")

    
    print("###############################")
    print("# VALID TEST: good file w/some empty lines")
    print("###############################")

    with CsvReader('hurricanes.csv',skip_top=0,skip_bottom=0, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")
    
    print("###############################")
    print("# INVALID TEST: None file")
    print("###############################")

    with CsvReader(None,skip_top=0,skip_bottom=0, header=True) as file:
            print("CsvReader Object: ",file)
            print("Header: ",file.getheader())
            print("Data: ",file.getdata())
    print("\n")

    print("###############################")
    print("# subject.pdf TEST 1:")
    print("###############################")
    with CsvReader('good.csv') as file:
        data = file.getdata()
        header = file.getheader()
    print("\n")

    print("###############################")
    print("# subject.pdf TEST 2:")
    print("###############################")
    with CsvReader('bad.csv') as file:
        if file == None:
            print("File is corrupted")




if __name__ == "__main__":
    main()

""" 
    # loading a file
    #from csvreader import CsvReader

    with CsvReader('good.csv') as file:
        data = file.getdata()
        header = file.getheader()
    print(file.closed)

    # loading a file
    with CsvReader('bad.csv') as file:
        if file == None:
            print("File is corrupted") """