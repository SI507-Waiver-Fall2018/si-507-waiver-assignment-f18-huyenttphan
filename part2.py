#Huyen Phan / huyentp

# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

db = sqlite3.connect('Northwind_small.sqlite')
c = db.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_list = sorted([x[0] for x in c.fetchall()])

def lname_to_ID(lastname):
	c.execute("SELECT Id FROM Employee WHERE LastName='{}'".format(lastname))
	empid = c.fetchall()
	try:
		return empid[0][0]
	except Exception:
		return None

params = sys.argv

if params[1] == 'customers':
	# customerparam = ('Id','CompanyName')
	c.execute("SELECT Id, CompanyName FROM Customer")
	customer_list = c.fetchall()
	print("ID\t\tCustomer Name")
	for customer in customer_list:
		print('{}\t\t{}'.format(*customer), sep='')

elif params[1] == 'employees':
	# empparam = ('Id','FirstName', 'LastName')
	c.execute("SELECT Id, FirstName, LastName FROM Employee")
	employee_list = c.fetchall()
	print("ID\t\tEmployee Name")
	for employee in employee_list:
		print('{}\t\t{} {}'.format(*employee), sep='')

elif params[1] == 'orders':
    if params[2].find('cust') == 0:
        ordercustparam = params[2][params[2].find('=')+1:].upper()
        c.execute("SELECT OrderDate FROM 'Order' WHERE CustomerId='{}'".format(ordercustparam))
        cust_order_list = c.fetchall()
        print('Order date by ID {}'.format(ordercustparam))
        for cust_order in cust_order_list:
            print(*cust_order)
    elif params[2].find('emp') == 0:
        lastnamegiven = params[2][params[2].find('=')+1:].capitalize()
        IDconvert = lname_to_ID(lastnamegiven)
        if IDconvert == None:
            print('No such employee: {}'.format(lastnamegiven))
        else:
            c.execute("SELECT OrderDate FROM 'Order' WHERE EmployeeId='{}'".format(IDconvert))
            emp_order_list = c.fetchall()
            print('Order dates processed by Employee {}, ID {}'.format(lastnamegiven, IDconvert))
            for emp_order in emp_order_list:
                print(*emp_order)
    else:
        print('Please add an additional parameter after orders, options are:\n "cust=<customer code>"\n "emp=<employee last name>"')
db.close()
