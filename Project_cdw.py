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
    q="select * from student order by id"
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)

def add_university():
    try:
        univ = input("University name: ")
        capa = int(input("University capacity: "))
        group = input("University group: ")
        cutline = int(input("Cutline score: "))
        weight = int(input("Weight of high school records: "))
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
        score = int(input("CSAT score: "))
        gpa = int(input("High school record score: "))

        q = F"Insert into student (name,csat_score, school_score) values ('{name}', '{score}', '{gpa}')"
        dbcon.executeQuery(q)
        print("A Student is successfully inserted")

    except:
        print("Student Insert Fail")

def del_student():
    try:
        del_student = input("Delete Student ID: ")
        q = F"select * from student where id = {del_student}"
        query_result = dbcon.getQueryResult(q)
        if len(query_result) == 0:
            print(F"Student Not exist where ID = {del_student}")
            return
        # 학생정보 삭제
        del_q = F"delete from student where id = {del_student}"
        dbcon.executeQuery(del_q)
        # apply 학생정보 삭제
        del_apply_q = f"delete from apply where student_id = {del_student}"
        dbcon.executeQuery(del_apply_q)
        # 학교 apply 변경
        del_univ_q = f"update university u " \
                     f"set applied = applied - (" \
                     f"select count(university_id) from apply where student_id = {del_student} " \
                     f"and university_id = id " \
                     f"group by student_id )"
        dbcon.executeQuery(del_univ_q)
        print(F"Student was deleted where id = {int(del_student)}")

        # 나중에 삭제
        q_print_apply = "select * from apply"
        query_result = dbcon.getQueryResult(q_print_apply)
        dbcon.printResult(query_result)


    except:
        print("Error Occured.. Please Insert Number")

def make_application():
    try:
        # apply table 없으면 생성
        q= f"Select 1 From information_schema.TABLES Where TABLE_NAME = 'apply'"
        check = dbcon.getQueryResult(q)
        if len(check) == 0:
            q_create = "CREATE table apply (student_id int(11), university_id int(11), " \
                       "primary key (student_id,university_id))"
            dbcon.executeQuery(q_create)
            print("apply table create")

        student_id = int(input("Student ID: "))

        # 학생 유무 체크 예외처리
        student_check_q = f"select * from student where id = {student_id} "
        student_check = dbcon.getQueryResult(student_check_q)
        if len(student_check) == 0:
            raise Exception('Check this student ID.')

        university_id = int(input("University ID: "))

        #대학교 유무 예외처리
        univ_check_q= f"select * from university where id = {university_id}"
        univ_check = dbcon.getQueryResult(univ_check_q)
        if len(univ_check) == 0:
            raise Exception('Check this university ID.')

        # 중복지원 예외처리
        red_check_q = f"select * from apply where student_id = {student_id} and university_id = {university_id} "
        red_check = dbcon.getQueryResult(red_check_q)
        if len(red_check) != 0 :
            raise Exception("the student\'s already applied to this University.")

        # 같은군 유무 예외처리
        clu_check_q = f"select univ_group from university inner join " \
                      f"(select univ_group from apply inner join university on(university.id = apply.university_id) " \
                      f"where student_id = {student_id}) as a using (univ_group) where university.id = {university_id}"
        clu_check = dbcon.getQueryResult(clu_check_q)
        if len(clu_check)!= 0 :
            raise Exception("the university group\'s already been applied.")

        # apply에 추가
        q = f"insert into apply (student_id, university_id) values ({student_id},{university_id})"
        dbcon.executeQuery(q)

        # 대학테이블에 applied 변경
        q_university = f"update university set applied = applied + 1 where id ={university_id} "
        dbcon.executeQuery(q_university)
        print("Successfully made an application")

        #나중에 삭제
        q_print_apply = "select * from apply"
        query_result = dbcon.getQueryResult(q_print_apply)
        dbcon.printResult(query_result)

    except Exception as e:
        print('Sorry,',e)


def print_all_applied_student():
    q= f"select distinct id,name,csat_score,school_score " \
       f"from student inner join apply on(student.id = apply.student_id) "
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)


def print_all_university_applied():
    q = f"select student.name student_name, university.name univ_name, univ_group " \
        f"from student inner join apply on(student.id = apply.student_id) " \
        f"inner join university on(apply.university_id = university.id)"
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)


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
