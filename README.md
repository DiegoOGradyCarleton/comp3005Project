Link to demonstration: https://youtu.be/ZyBtdOLjtlE


Steps to set up:
0. Ensure the correct postgres database is already set up
1. Clone the repository
2. If nessesary, install required modules
3. Create a file in the project directory called "database.ini" with the following parameters and the username and password of your postgres admin user:

~~~
[postgresql]
host=localhost
database=Students
user=<put the username of your postgres admin here>
password=<put the password of your postgres admin here>
~~~

4. Run the program in the command line with "python students.py"