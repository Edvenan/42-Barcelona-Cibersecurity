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
         
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        
        # Exception handling: mistmatch between number of fields and number of records
        
        # Exception handling: records with different length.
        
        self.file.close()
 
    def getdata(self):
        """ Retrieves the data/records from skip_top to skip bottom.
        Return:
        nested list (list(list, list, ...)) representing the data.
        """
        file_total_lines = len(self.file.readlines())
        result = []
        for i in range(1, file_total_lines+1):
            if i > self.skip_top and i < (file_total_lines - self.skip_bottom):
                result.append(self.file.readline())
            
            else:
                self.file.readline()
            
            
        
    def getheader(self):
        """ Retrieves the header from csv file.
        Returns:
        list: representing the data (when self.header is True).
        None: (when self.header is False).
        """
        if self.header:
            return self.file.readline()
        else:
            return None


#####################
# MAIN
#####################
 
# loading a file
#from csvreader import CsvReader

if __name__ == "__main__":
    with CsvReader('good.csv') as file:
        data = file.getdata()
        header = file.getheader()
    print(file.closed)

# loading a file
    with CsvReader('bad.csv') as file:
        if file == None:
            print("File is corrupted")