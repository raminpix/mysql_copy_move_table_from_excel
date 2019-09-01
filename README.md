# MySQL Copy Move Table Tool
A python script to copy or move multiple tables between different schemes in a MySQL database.

To use this tool you should have [PyMySQL](https://github.com/PyMySQL/PyMySQL) package installed (you can install it using this command: **pip install pymysql**) and set the following values in the config file(config.ini):

- database hostname
- username
- password
- excel file to read source and destination schemes and tables

Fill the excel file like the sample values provided in the file in order to move or copy between different schemes quickly.

