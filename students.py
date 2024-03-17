from functions import *

#Displays the list of usable functions along with any required inputs in a loop
def main():
    while True:
        print("Select an Option:")
        print("----------------------------")
        print(" 1. Get all students")
        print(" 2. Add a new student")
        print(" 3. Update a student's email")
        print(" 4. Delete a student")
        print("\n 0. Exit")
        print("----------------------------")
        selection = input()

        match selection:
            case '0':
                break
            
            case '1':
                getAllStudents()
                print("\n")

            case '2':
                firstName = input("Enter the student's first name: ")
                lastName = input("Enter the student's last name: ")
                email = input("Enter the student's email: ")
                print("Enter the student's enrollment date: ")
                enrollmentDay = input("    Enter the day of enrollment: ")
                enrollmentMonth = input("    Enter the month of enrollment: ")
                enrollmentYear = input("    Enter the year of enrollment: ")
                addStudent(firstName, lastName, email, enrollmentDay, enrollmentMonth, enrollmentYear)
                print("\n")

            case '3':
                id = input("Enter the student's id: ")
                email = input("Enter the student's new email: ")
                updateStudentEmail(id, email)
                print("\n")

            case '4':
                id = input("Enter the student's id: ")
                deleteStudent(id)
                print("\n")

            case _:
                print("Invalid Input\n")

    return


if __name__ == '__main__':
    main()