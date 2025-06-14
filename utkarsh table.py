from prettytable import PrettyTable

table = PrettyTable(["students name","year ","student id","section"])

table.add_row(["utkarsh", "3" , "22BTCS0126", "CS3"])

table.add_row(["varun", "3" , "22BTCS0395", "CS3"])

table.add_row(["aditya ", "3" , "22BTEC009", "EC3"])

table.add_row(["aman verma", "3" , "22BTCS0127", "CS1"])


print(table);
