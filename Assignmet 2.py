import pandas as pd
import matplotlib.pyplot as plt

def CheckOrderDate(ids,OrderDate,dfdate):
    global index
    ids = ids.split('-')
    if (ids[1] not in OrderDate) and (ids[0].isalpha()): 
        ids = '-'.join([ids[0], dfdate[index].split('/')[2] , ids[1] + ids[2]])
    else:
        ids = '-'.join(ids)
    index += 1
    return ids

def CheckingID(ids,check):
    ids = ids.split('-')
    for i in list(range(check)) :
        if (not(ids[i])) or (not(ids[i].isalpha())):
            return False
    return('-'.join(ids))

def formatID(ids,separation,check,yearCheck = False,OrderDate = None, dfdate = None):
    ids = ''.join('' if not(i.isalnum()) else i for i in ids)
    if len(separation) == 2:
        ids = ids[0:separation[0]] + '-' + ids[separation[0]:separation[1]] + '-' + ids[separation[1]:]  
    else:
        ids = ids[0:separation[0]] + '-' + ids[separation[0]:]
    
    if yearCheck:
        ids = CheckOrderDate(ids,OrderDate,dfdate)
    ids = CheckingID(ids,check)
    return ids

def pading0(ids,padnum,segment):   
    ids = ids.split('-')    
    while len(ids[segment]) < padnum:
        ids[segment] = '0' + ids[segment]
    return '-'.join(ids)


def formatDate(date):
    date =  ''.join('/' if not(i.isalnum()) else i for i in date)
    date = pd.to_datetime(date , format = '%d/%m/%Y')
    date = date.strftime('%d/%m/%Y')
    return  '/'.join([ '0' + str(i)  if len(i) < 2 else i for i in date.split('/')])
    
def main(df):
    df[['Order Date','Ship Date']] = df[['Order Date','Ship Date']].applymap(formatDate)

    OrderDate = list(df['Order Date'].copy().apply(lambda x: x.split('/')[2]).drop_duplicates())
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    for i in list(range(len(df))):
        if pd.to_datetime(df.at[i+1,'Ship Date'] , format = '%d/%m/%Y') < pd.to_datetime(df.at[i+1,'Order Date'] , format = '%d/%m/%Y'):
            df.at[i+1,'Ship Date'] = '' + str(df.at[i+1,'Order Date'])
        
    df[['Order ID','Customer ID','Product ID']] = df[['Order ID','Customer ID','Product ID']].applymap(lambda x: x.upper())

    
    df['Order ID'] = df['Order ID'].apply(formatID, separation = [2,6],yearCheck = True, OrderDate = OrderDate, dfdate = df['Order Date'],check = 1)
    df['Customer ID'] = df['Customer ID'].apply(formatID, separation = [2],check = 1)
    df['Product ID'] = df['Product ID'].apply(formatID, separation = [3,5],check = 2)

    # remove all the invalid code found
    df = df[(df[['Order ID','Customer ID','Product ID']] != False).all(axis=1)]

    # padding the ids with specific padnum
    df['Order ID'] = df['Order ID'].apply(pading0, padnum = 6, segment = 2)
    df['Customer ID'] = df['Customer ID'].apply(pading0, padnum = 5, segment = 1)
    df['Product ID'] = df['Product ID'].apply(pading0, padnum = 8, segment = 2)
    return df

# management system and user interaction
#show the menu    
class System:
    
    def __init__(self):
        self.start = ''
        self.choice = ''
    
    def Start(self):
        self.start = input('Start Operattion?(y/n): ').lower()
    
    def menu(self):
        print('Main menu')
        print('*********')
        print('-Search for a transaction(S)-')
        print('-Add new transaction     (A)-')
        print('-Remove a transaction    (R)-')
        print('-Update a transaction    (U)-')
        print('-Display Data Frame      (D)-')
        print('-Show Summary           (SS)-')
        print('-Show Analysis Result   (AR)-')
        self.choice =  input('Please choose an option above:').upper()
        
    
    def Exit(self):
        print('Thanks for using this system.')



# do the actual work
class Transaction(System):

    def __init__(self,choice,df):
        self.choice = choice
        self.df = df
        self.Continue = 'y'
    
    def NotMandatory(self,data):
          if data == '':
              return 'No input'
          else: 
              return data    
          
    def ChoiceAndContinue(self):
        self.Continue = input('Do you want to continue?(y/n):')
        if self.Continue == 'y':
            SameChoice = input('Same operation?(y/n):')
            if SameChoice == 'n':
                self.menu()
            
    
    def Search(self):
        self.search = input('Please Enter data for searching:')
            
        try:
            self.search = float(self.search)
        except ValueError:
            self.search = str(self.search)
            
        if len(self.df[(self.df == self.search).any(axis=1)]) == 0:
            print('Sorry, cannot find what you are looking for.')
        else:
            print(self.df[(self.df == self.search).any(axis=1)])
    
            
    def NewTransaction(self):
        InputChoice = input('Enter single line or multiple(s/m):')
        
        if  InputChoice == 's': 
            print('To enter a new Transaction, please enter')
            OrderId = input('Order Id:')
            OrderDate = input('Order Date(d/m/y):')
            ShipDate = input('Ship Date(Not Mandatory):')
            CustomerId = input('Customer Id:')
            Segment = input('Segment:')
            Country = input('Country(Not Mandatory):')
            City = input('City(Not Mandatory):')
            State = input('State(Not Mandatory):')
            ProductId = input('Product Id:')
            Category = input('Category:')
            Sales = float(input('Sales:'))
            
            Country = self.NotMandatory(Country)
            City = self.NotMandatory(City)
            State = self.NotMandatory(State)
            
            if ShipDate == '':
                ShipDate = '' + OrderDate

            dfNew = pd.DataFrame({'Order ID' : OrderId,
                                  'Order Date' : OrderDate,
                                  'Ship Date' : ShipDate,
                                  'Customer ID' : CustomerId,
                                  'Segment' : Segment,
                                  'Country' : Country,
                                  'City' : City,
                                  'State' : State,
                                  'Product ID' : ProductId,
                                  'Category' : Category,
                                  'Sales' : Sales}, index = [0])
        else:
            dfNew = input('To enter multiple new Transactions, please enter the csv file name:')
            dfNew = pd.read_csv(dfNew, index_col = 'Row ID')
            
        self.df = pd.concat([self.df,dfNew], axis = 0, ignore_index = True)
        self.df.index = df.index + 1
        self.df.index.name = 'Row ID'
        self.df = main(self.df)

        if len(self.df[self.df.duplicated()]) != 0 : 
            self.df = self.df.drop_duplicates()
            print('This is a duplicated Row, Removing it from DataFrame') 
        
        
            
    def Remove(self):
        RemoveChoice = int(input('Choose the Row ID of the row you want to remove:'))
        self.df.drop(index = RemoveChoice, inplace = True)


    def UpdateTransaction(self):
        UpdateRowChoice = int(input('Enter the row you want to edit:'))
        UpdateColumnChoice = input('Enter the column you want to edit:')
        UpdateValue = input('Enter the updated value:')
        self.df.at[UpdateRowChoice,UpdateColumnChoice] = UpdateValue
    
    def Display(self):
        print(self.df)
    
    def ShowSummary(self):
        print('Order, Customer and Product Summary')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(self.df[['Order ID','Customer ID','Product ID']].describe())
        print('Sales summary')
        print('~~~~~~~~~~~~~')
        print('sum    %.2f'%df['Sales'].sum())
        print(self.df['Sales'].describe().round(2))

    def AnalysisResult(self):  
        Monthdict = {'01': 'Jan',
                     '02' : 'Feb',
                     '03' : 'Mar',
                     '04' : 'Apr',
                     '05' : 'May',
                     '06' : 'Jun',
                     '07' : 'Jul',
                     '08' : 'Aug',
                     '09' : 'Sep',
                     '10' : 'Oct',
                     '11' : 'Nov',
                     '12' : 'Dec'
                     }
        SegmentCount  = self.df['Segment'].value_counts()
        self.df['Order Year'] = self.df['Order Date'].apply(lambda x: x.split('/')[2])
        self.df['Order MonthYear'] = self.df['Order Date'].apply(lambda x: '/'.join([x.split('/')[1],x.split('/')[2]]))
        self.df['Order Month']= self.df['Order Date'].apply(lambda x: x.split('/')[1])

        plt.figure()
        (SegmentCount * 100 / len(df)).plot(kind='pie', autopct='%1.0f%%', title = 'Percentage of sales by each segment')

        plt.figure()
        SalesPerYear = self.df.groupby(by=['Category','Order Year'])['Sales'].sum().reset_index()
        SalesPerYear = SalesPerYear.pivot_table(index = 'Order Year', columns ='Category') 
        SalesPerYear.plot(kind = 'bar', y = 'Sales',title='Category sales per Year',xlabel = 'Year', ylabel = 'Sales($)')
        

        plt.figure()
        SalesMonthYear = self.df.groupby(by=['Order Year','Order MonthYear'])['Sales'].sum()
        SalesMonthYear  = SalesMonthYear.reset_index()
        SalesMonthYear['Order MonthYear'] = SalesMonthYear['Order MonthYear'].apply(lambda x: ' '.join([ Monthdict[x.split('/')[0]], x.split('/')[1]]))
        
        SalesMonthYear.plot(x='Order MonthYear', y= 'Sales', kind="line", title = 'Sales per Month',xlabel = 'Month Year', ylabel = 'Sales($)' )

        plt.figure()
        SalesMonth = self.df.groupby(by=['Order Month'])['Sales'].sum().reset_index().sort_values(by='Order Month')
        SalesMonth['Order Month'] = SalesMonth['Order Month'].apply(lambda x: Monthdict[x])
        SalesMonth = SalesMonth.plot(x='Order Month', y= 'Sales', kind="line", title = 'Sales per Month',xlabel = 'Month',ylabel = 'Sales($)' )
        
        plt.show()
        
    
    def ProcessChoice(self):
        
        OperationDict = {
            'S' : self.Search, 
            'A' : self.NewTransaction,
            'R' : self.Remove,
            'U' : self.UpdateTransaction,
            'D' : self.Display,
            'SS': self.ShowSummary,
            'AR': self.AnalysisResult
            }
        try:
            if self.choice in list (OperationDict.keys()):
                while self.Continue == 'y':
                    Operation = OperationDict[self.choice]
                    Operation()
                    self.ChoiceAndContinue()
                self.Exit()
            else:
                print("No corresponding operation found for input:", self.choice)
        except KeyError:
                print("No corresponding operation found for input:", self.choice)
                
df = pd.read_csv('superstore_sales.csv', index_col = 'Row ID')
# no more duplicate and empty element
df = df.dropna()
df = df.drop_duplicates()
index = 1

df = main(df)
df = df.drop_duplicates().reset_index(drop = True)
df.index = df.index + 1
df.index.name = 'Row ID'
df.to_csv('clean_superstore_sales.csv')
                    
df = pd.read_csv('clean_superstore_sales.csv', index_col = 'Row ID')
System = System()
System .Start()
if System.start == 'y':
    System.menu()
    data = Transaction(System.choice,df)
    data.ProcessChoice()
    df = data.df
else:
    System.Exit()





  
    

     
    





     
      

