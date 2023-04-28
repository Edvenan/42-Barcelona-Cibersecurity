#!/usr/bin/env python
""" 
The goal of this exercise is to implement a context manager as a class. Thus you are
strongly encouraged to do some research about context manager.

Implement a CsvReader class that opens, reads, and parses a CSV file. This class is
then a context manager as class. In order to create it, your class requires a few built-in
methods:
    • __init__,
    • __enter__,
    • __exit__.
It is mandatory to close the file once the process has completed. You are expected to
handle properly badly formatted CSV file (i.e. handle the exception):
    • mistmatch between number of fields and number of records,
    • records with different length.
    
CSV (for Comma-Separated Values) file is a delimited text file which uses a comma to
separate values. 
    • Therefore, the field separator (or delimiter) is usually a comma (,) but
      with your context manager you have to offer the possibility to change this parameter.
    • One can decide if the class instance skips lines at the top and the bottom of the file
      via the parameters skip_top and skip_bottom.
    • One should also be able to keep the first line as a header if header is True.
    • The file should not be corrupted (either a line with too many values or a line with
      too few values), otherwise return None.
    • You have to handle the case file not found.
    • You are expected to implement two methods:
        • getdata(),
        • getheader().
        
        
        https://www.geeksforgeeks.org/how-to-read-from-a-file-in-python/
        https://www.geeksforgeeks.org/context-manager-in-python/
"""
import sys
import traceback
import csv

#######################
# CONTEXT MANAGER
#######################
 
class CsvReader():
    def __init__(self, filename=None, sep=',', header=False, skip_top=0, skip_bottom=0):
        self.filename = filename
        self.mode = 'r'
        self.sep = sep
        self.header = header
        self.skip_top = skip_top
        self.skip_bottom = skip_bottom
        self.file = None
        self.data = []
        self.data_header = []
         
    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode)
            
            if self.header:
                # Get the first line of the file
                first_line = next(self.file)
                print(first_line)
                # split the line in elements using 'sep' as separator
                split_line = first_line.split(self.sep)
                # clean each line element by removing leading/trailing spaces, quotes and '\n'
                for element in split_line:
                    # append cleaned elements to 'self.data_header' list
                    self.data_header.append(element.lstrip().rstrip('\n').rstrip().strip('"'))
            
            data = self.file.readlines()
            file_total_lines = len(data)
            if self.skip_top >=file_total_lines:
                error_value= f"'skip_top' parameter value should be lower than the file's total data lines ({file_total_lines})"
                self.__exit__("ValueError", error_value, None)
            elif self.skip_bottom >=file_total_lines:
                error_value= f"'skip_bottom' parameter value should be lower than the files's total data lines ({file_total_lines})"
                self.__exit__("ValueError", error_value, None)
            
            selected_lines = data[self.skip_top:(file_total_lines - self.skip_bottom)]
            
            # Initialize 'parsed_line' & 'parsed_lines lists'
            parsed_line = []
            for line in selected_lines:
                # split each line in elements using 'sep' as separator
                split_line = line.split(self.sep)
                # clean each line element by removing leading/trailing spaces, quotes and '\n'
                for element in split_line:
                    # append cleaned elements to 'parsed_line' list
                    parsed_line.append(element.lstrip().rstrip('\n').rstrip().strip('"'))
                # append each parsed line to 'parsed_lines' list
                self.data.append(parsed_line)
                # reset 'parsed_line' list
                parsed_line = []
            print(self.data[0])
            print(*(e for e in self.data[0]), sep=':')
            print(len(self.data[0]))
            return self

        except Exception as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.__exit__(exc_type.__name__, exc_value, exc_traceback)

     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        
        if exc_type and exc_value:
            traceback.print_tb(exc_traceback)
            print("{0}: {1}".format(exc_type, exc_value))
            if self.file:
                self.file.close()
            exit(1)
        else:
            self.file.close()
 
 
    def getdata(self):
        """ Retrieves the data/records from skip_top to skip bottom.
        Return:
        nested list (list(list, list, ...)) representing the data.
        """
        return self.data
       
    def getheader(self):
        """ Retrieves the header from csv file.
        Returns:
        list: representing the data (when self.header is True).
        None: (when self.header is False).
        """
        if self.header:
            return self.data_header
        else:
            return None


#####################
# MAIN
#####################
def main():
    with CsvReader('bad.csv',skip_top=1,skip_bottom=19, header=True) as file:
        if file == None:
            print("File is corrupted")
        else:
            data = file.getdata()
            header = file.getheader()
    print(file.file.closed)
    print(data)
    print(header)
     

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