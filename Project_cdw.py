#DB part 분리 (DBconnect쪽으로)
from DBconnect import DBConnect
dbcon = DBConnect("astronaut.snu.ac.kr", '20DS2_2020_0704', '20DS2_2020_0704', '20DS2_2020_0704_PRJ')

def apply_to_university():
    print_str = """
    ==========================================================================================
    1. print all universities
    2. print all students
    3. insert a new university
    4. remove a university
    5. insert a new student
    6. remove a student
    7. make an application
    8. print all students who applied for a university
    9. print all universities a student applied for
    10. print expected successful applicants of a university
    11. print universities expected to accept a student
    12. exit
    13. reset database
    ==========================================================================================
    """
    print(print_str)


def print_all_university():
    q = "select * from university order by id"
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)

def print_all_student():
    #q = "select * from student order by student_id, name, sat_score, gpa"
    q="select * from student"
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)

def add_university():
    try:
        univ = input("University name: ")
        capa = input("University capacity: ")
        group = input("University group: ")
        cutline = input("Cutline score: ")
        weight = input("Weight of high school records: ")
        univ = univ.replace("'","\\'")  # 따옴표 학교명 대응
        print(univ)

        q = f"Insert into university(name,capacity,univ_group,cutline,weight) values('{univ}', '{capa}', '{group}', '{cutline}','{weight}')"
        dbcon.executeQuery(q)
        print("A University is successfully inserted")

    except:
        print("University Insert Fail")

def del_university():
    try:
        del_univ = input("Delete University ID: ")
        q = F"select * from university where id = {del_univ}"
        query_result = dbcon.getQueryResult(q)
        if len(query_result) == 0:
            print(F"University ID({del_univ}) Not exist.")
            return

        del_q = F"delete from university where id = {del_univ}"
        dbcon.executeQuery(del_q)
        print(F"University was successfully deleted. id: {del_univ}")

    except:
        print("Please Insert Number")
        return

def add_student():
    try:
        name = input("Student name: ")
        score = input("CSAT score: ")
        gpa = input("High school record score: ")

        q = F"Insert into student(name, sat_score, gpa) values('{name}', '{score}', '{gpa}')"
        dbcon.executeQuery(q)
        print("A Student is successfully inserted")

    except:
        print("Student Insert Fail")

def del_student():
    try:
        del_student = input("Delete Student ID: ")
        q = F"select * from student where univ_id = {del_student}"
        query_result = dbcon.getQueryResult(q)
        if len(query_result) == 0:
            print(F"University Not exist where ID = {del_univ}")
            return

        del_q = F"delete from university where univ_id = {del_univ}"
        dbcon.executeQuery(del_q)
        print(F"University was deleted where univ_id = {del_univ}")

    except:
        print("Error Occured.. Please Insert Number")

def make_application():
    try:
        # apply table 없으면 생성
        q= f"Select 1 From information_schema.TABLES Where TABLE_NAME = 'apply'"
        check = dbcon.getQueryResult(q)
        if len(check) == 0:
            q_create = "CREATE table apply " \
                       "(student_id int(11), university_id int(11), primary key(student_id,university_id))"
            dbcon.executeQuery(q_create)
            print("apply table create")

        student_id = input("Student ID: ")
        university_id = input("University ID: ")
        q = f"insert into apply (student_id, university_id) values ({student_id},{university_id})"
        q_university = f"update university into applied ={university_id}"
        dbcon.executeQuery(q)
        print("Successfully made an application")

    except:
        print('Please Insert number')


def print_all_applied_student():
    pass


def print_all_university_applied():
    pass






apply_to_university()

while(True):
    action = input("Select your action: ")

    if action == "1":
        print_all_university()
    elif action == "2":
        print_all_student()
    elif action == "3":
        add_university()
    elif action == "4":
        del_university()
    elif action == "5":
        add_student()
    elif action == "6":
        del_student()
    elif action == "7":
        make_application()
    elif action == "8":
        print_all_applied_student()
    elif action == "9":
        print_all_university_applied()




    elif action == "12":
        print("Bye!")
        break

