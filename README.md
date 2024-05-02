## OOP Assignment 2

This assignment is a Python application modifies a specific input file(superstore_sales.csv) into a clean ouput file(clean_superstore_sales.csv) by formating certain information in specific ways. This also include a system which allows the user to manually modify the dataframe from the modified data.

## Installation
1. Use any python intepreter to run the program,Assignment 2.py (spyder is recommended)
2. or https://github.com/hanhc69/3E_Han-Hong-Chou_2202791/blob/fb6349ba07b21fbf9675bc732c8fbb3e730366f5/Assignmet%202.py

## Usage
To use the code, a file called 'superstore_sales.csv' is required.

## Instructions
1. When running the program, an output 'clean_superstore_sales.csv' file will be created in the folder.
2. Then, a line asking to start the program will appear.
3. If 'y' is entered, it will direct the user to the menu where there are 7 options.
4. For first option, 'S' is typed and the program asks users to enter the object they want to search from the dataframe. After entering it will print out rows that contains the input.
5. If 'A' is entered, the user is directed to choose between entering single or multiple lines.
6. If 's' is entered, the user is prompted to enter data for each column in a row. '(not mandatory)' is shown beside data that require no input. If no input, Ship date will be changed to the Order date while the others will be 'no input'.
7. If 'm' is entered, users are prompted to enter a file name which will be unpacked to add to the dataframe.
8. If the entry is a duplicate, it will be removed and user will be notified with a message.
9. To remove a transaction, 'R' is entered in the menu, the users will be prompt to enter the row they want to enter. After entering, the row is removed.
10. If 'U' is entered, the user is prompted to enter the row, column they want to change and the value to change it to. After all are entered, the value in the dateframe will change.
11. If 'D' is entered, it will display the current dataframe.
12. If 'SS' is entered, it will display the summary of the dataframe.
13. If 'AR' is entered, it will display the analysis result of the dataframe which consist of 4 graphs, Percentage of sales by each segment, Category sales per Year, Sales per Year in Monthly Increment and Sales per Month.
14.  After each operation, the user is asked if they want to continue. If 'y' is entered, users will be asked to choose between the same operation or another operation.
15.  The operation ends after 'n' is pressed when asked to continue.
## Intepret Result
1.	The majority of sales are from consumer with 52% of all sales.
2.	Category sales has an increasing trend from 2014 to 2017 with office supplies sales drop between 2014 and 2015.
3.	The sales have similar cycles each year with most sales happening at the end of the year.

## Known Errors
1. The program may have some delay when some operation is used as main() function is called and contain for loop on top of apply() or applymap() which causes delay.
2. For date format, if there are no proper separation,'/' between date,month and year. ValueError will occur.
3. There are some errors that may occur if unaccounted input is added, restarting the system is recommended.
4. Dates in csv does not comply to dd/mm/yyyy although it works in the codes


