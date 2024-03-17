import psycopg2
from config import load_config

def getAllStudents():
    #Uses a select statement to get all rows of the students table and prints them to the terminal one at a time
    config  = load_config()
    try:
        with psycopg2.connect(**config) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students")
                row = cursor.fetchone()

                while row is not None:
                    print(row)
                    row = cursor.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def addStudent(firstName, lastName, email, enrollmentDay, enrollmentMonth, enrollmentYear):
    #FIlls an insert statement with the required parameters and sends it to postgres

    sql = """INSERT INTO students(first_name, last_name, email, enrollment_date)
             VALUES(%s, %s, %s, to_date(%s, 'DD/MM/YYYY')) RETURNING student_id;"""
    
    enrollmentDate = enrollmentDay + '-' + enrollmentMonth + '-' + enrollmentYear
    connectAndExecute(sql, (firstName, lastName, email, enrollmentDate)) 

def updateStudentEmail(studentId, newEmail):
    #FIlls an update statement with the required parameters and sends it to postgres

    sql = """ UPDATE students
                SET email = %s
                WHERE student_id = %s"""
    
    connectAndExecute(sql, (newEmail, studentId))  

def deleteStudent(studentId):
    #FIlls a delete statement with the required parameters and sends it to postgres

    sql = """ DELETE FROM students
                WHERE student_id = %s"""
    
    connectAndExecute(sql, [studentId])  



def connectAndExecute(sql, args):
    #performs common action of connecting to poatgres and executing the sql passed in
    config = load_config()

    try:
        with  psycopg2.connect(**config) as connection:
            with  connection.cursor() as cursor:
                # execute the statement passed as an argument
                cursor.execute(sql, args)

                # commit the changes to the database
                connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)          