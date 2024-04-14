The fileLoader.py file will not work unless the path to the data folder of the associated opendata stats is inputted into the first string

Additionally the following file may need to be defined with the name 'database.ini':

~~~
[postgresql]
host=localhost
database=Students
user=<put the username of your postgres admin here>
password=<put the password of your postgres admin here>
~~~