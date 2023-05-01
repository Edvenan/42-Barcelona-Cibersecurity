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


#######################
# CONTEXT MANAGER
#######################
 
class CsvReader():
    def __init__(self, filename=None, sep=',', header=False, skip_top=0, skip_bottom=0):
        self.filename = filename
        self.sep = sep
        self.header = header
        self.skip_top = skip_top
        self.skip_bottom = skip_bottom
        self.file = None
        self.data = []
         
    def __enter__(self):
        try:
            # open file
            self.file = open(self.filename, 'r')
            print("-- File opened --")
            # Read and store all file raw lines in 'data' var 
            data = self.file.readlines()
            # Count number of lines
            file_total_lines = len(data)
            
            # raise exception if file is empty
            if file_total_lines == 0:
                raise ValueError(f"File '{self.filename}' is empty")

            # print warning if 'sikp_top' and 'skip_bottom' values are > total file lines
            if self.skip_top >=file_total_lines:
                print(f"WARNING: In order to get some data, 'skip_top' value should be lower than the file's total data lines ({file_total_lines})")
            elif self.skip_bottom >=file_total_lines:
                print(f"WARNING: In order to get some data, 'skip_bottom' value should be lower than the file's total data lines ({file_total_lines})")
                
            # Parse and Store all file lines in 'self.data'
            # Initialize 'parsed_line' list'
            parsed_line = []
            for line in data:
                # split each line in elements using 'sep' as separator
                split_line = line.split(self.sep)
                # clean each line element by removing leading/trailing spaces, quotes and '\n'
                for element in split_line:
                    # append cleaned elements to 'parsed_line' list
                    parsed_line.append(element.lstrip().rstrip('\n').rstrip().strip('"'))
                # append each parsed line to 'seld.data' list, even if empty
                self.data.append(parsed_line)
                # reset 'parsed_line' list
                parsed_line = []
            
            # Check if file is corrupted
            if self.is_corrupted():
                return None
            else:
                return self

        except Exception:
            # obtain/print exception info & return Cntxt Mgr object
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback)
            print(f"{exc_type.__name__}: {exc_value}")
            return self

     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Close the file before raising exceptions
        if self.file:
            self.file.close()
            print("-- File closed --")
        # raise exceptions occurred within the context if any
        if exc_type and exc_value:
            #traceback.print_tb(exc_traceback)
            print("EXCEPTION RAISED WITHIN THE CONTEXT: ",exc_type.__name__,": ",exc_value)

 
    def getdata(self):
        """ Retrieves the data/records from skip_top to skip bottom.
        Return:
        nested list (list(list, list, ...)) representing the data.
        """
        # handle case when file is not found and function is called
        if not self.data:
            return None
        else:
            file_total_lines = len(self.data)
            if self.header:
                return self.data[self.skip_top+1 : (file_total_lines - self.skip_bottom)]
            else:
                return self.data[self.skip_top : (file_total_lines - self.skip_bottom)]
        
       
    def getheader(self):
        """ Retrieves the header from csv file.
        Returns:
        list: representing the data (when self.header is True).
        None: (when self.header is False).
        """
        # handle case when file is not found and function is called
        if not self.data:
            return None
        else:
            if self.header:
                return self.data[0]
            else:
                return None

    def is_corrupted(self):
        
        # initialize element list
        el_list = []
        
        # Check mistmatch between number of fields and number of records (length of all lines)
        # keep track also of line number 'ln'
        for ln, line in enumerate(self.data):
            if ln == 0:
                # Set len_var to the length of first line 'ln == 0' (header line)
                len_var = len(line)
            if (len(line) != len_var or ("" in line)) and (line != ['']):
                # length of current line != to header's -> corrupted file (line ignored if empty)
                print("The file is corrupted. Inconsistent length of records in line {}".format(ln+1))
                return True
            """ # Check records with different length
            
            for en, element in enumerate(line):
                if self.header and ln ==1:
                   el_list.append(len(element))
                elif self.header and ln ==0:
                    pass
                else:
                    if ln == 0:
                        pass
                    elif ln == 1:
                        el_list.append(len(element))
                    else:
                        if len(element) != el_list[en]:
                            # length of current element != to first line's element -> corrupted file
                            print("The file is corrupted. Inconsistent record length in line {}, element ({})".format(ln+1, en+1))
                            return True """
        return False