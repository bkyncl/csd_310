from tabulate import tabulate


table_data = [['name', 'age', 'job'],
            ['mike', '22', 'programmer'],
            ['carol', '35', 'tech'],
            ['sam', '27', 'HR'],
            ['john', '40', 'Marketing'],
            ['mary', '29', 'Manager']]

print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid", showindex="always"))

print(tabulate(table_data, headers="firstrow", tablefmt="html"))
with open('mytable.html', 'w') as f:
    f.write(tabulate(table_data, headers="firstrow", tablefmt="html"))

#SYNTAX
# specify headers h=["column 1", "column 2", "column 3"]
# print(tabulate(<data>, headers = h, tablefmt="<format>"))