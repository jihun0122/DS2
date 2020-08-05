#DB part 분리 (DBconnect쪽으로)
from DBconnect import DBConnect
import math
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
    q = "select * from university order by id,name,capacity,univ_group,cutline,weight,applied"
    query_result = dbcon.getQueryResult(q)
    dbcon.printResult(query_result)

def print_all_student():
    q="select * from student order by id,name,csat_score,school_score"
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
            print(F"University ID ({del_univ}) Not exist.")
            return

        # 학교 정보 삭제. apply 자동삭제(f.k)
        del_q = F"delete from university where id = {del_univ}"
        dbcon.executeQuery(del_q)
        print(F"University ({del_univ}) was successfully deleted.\n "
              F"Done! You can see all University, selecting action number: 1")

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
        print("The Student is successfully inserted.")

    except:
        print("Student Insert Fail.")

def del_student():
    try:
        del_student = input("Delete Student ID: ")
        q = F"select * from student where id = {del_student}"
        query_result = dbcon.getQueryResult(q)
        if len(query_result) == 0:
            print(F"Student ID ({del_student}) Not exist.")
            return
        # 학교 applied 변경
        q = F"select distinct university_id from apply where student_id = {del_student}"
        query_result = dbcon.getQueryResult(q)

        for i in range(len(query_result)):
            univ_id = query_result[i]['university_id']
            u_q = F"update university set applied = applied - 1 where id = {univ_id}"
            dbcon.executeQuery(u_q)

         # 학생 정보 삭제, appy 정보 자동 삭제 (f.k)
        del_q = F"delete from student where id = {del_student}"
        dbcon.executeQuery(del_q)
        print(F"Student ({del_student}) was successfully deleted.\n "
              F"Done! You can see all Student, selecting action number: 2")

    except:
        print("Sorry. Error Occurred. Please Insert Number")

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

def predict_studentList(university_id, u_capa, u_ratio, u_cutline):
    # rank query
    rq = F"select student_id, name, csat_score, school_score, csat_score + school_score*{u_ratio} as tot_score, " \
         F"rank() over(order by tot_score desc, school_score desc) as rank " \
         F"from apply a inner join student s on(a.student_id = s.id)" \
         F"where a.university_id = {university_id} and csat_score + school_score*{u_ratio} >={u_cutline} " \
         F"order by rank, school_score, student_id, name, csat_score"
    r_result = dbcon.getQueryResult(rq)
    f_result = r_result  # 아무 조건도 안 타는 경우

    # 정원초과,동점자 처리
    if len(r_result) > u_capa:
        d_capa = math.ceil(u_capa * 1.1)
        if len(r_result) >= d_capa + 1 and r_result[u_capa - 1]['rank'] == r_result[d_capa]['rank']:
            duple_rank = r_result[u_capa - 1]['rank']
            f_result = list(filter(lambda x: x['rank'] < duple_rank, r_result))
        elif r_result[u_capa - 1]['rank'] == r_result[u_capa]['rank']:
            duple_rank = r_result[u_capa - 1]['rank']
            f_result = list(filter(lambda x: x['rank'] <= duple_rank, r_result))
        else:
            f_result = r_result[:u_capa]

    return f_result


def print_expected_successful_applicants():
    try:
        university_id = int(input("University ID: "))
        q = F"select * from university where id = {university_id}"
        u_result = dbcon.getQueryResult(q)
        dbcon.printResult(u_result)

        if len(u_result) == 0:
            print(F"University ID ({university_id}) Not exist.")
            return

        u_capa = u_result[0]['capacity']
        u_ratio = u_result[0]['weight']
        u_cutline = u_result[0]['cutline']

        f_result = predict_studentList(university_id, u_capa, u_ratio, u_cutline)

        # remove unnecessary column
        for i in range(len(f_result)):
            del f_result[i]['rank']
            del f_result[i]['tot_score']

        # reordering
        f_result = sorted(f_result, key=lambda k: (k['student_id'], k['name'],k['csat_score'],k['school_score']))

        dbcon.printResult(f_result)

    except :
        print("Sorry. Please university ID check.")


def print_expected_universities():
    try:
        student_id = int(input("Student ID: "))
        q = f"select university_id as id,university.name, capacity, univ_group, cutline, weight,applied " \
            f"from apply inner join university on(university.id = apply.university_id) " \
            f"inner join student on (student.id = apply.student_id)  " \
            f"where csat_score + school_score * weight >= cutline and student.id = {student_id} " \
            f"order by university_id, university.name, capacity, univ_group, cutline,weight,applied "
        query_result = dbcon.getQueryResult(q)
        if len(query_result)==0:
            raise  Exception(f"Student ID ({student_id}) Not exist of the student has\'t applied.")
        dbcon.printResult(query_result)

    except Exception as e:
        print("Sorry,", e)

def reset_database():
    # table 삭제
    try:
        confirm = input("Are you sure?? (Y/N)")
        if confirm.upper() == 'Y':
            delete_school_q = "truncate from student"
            dbcon.executeQuery(delete_school_q)
            delete_university_q = "truncate from university"
            dbcon.executeQuery(delete_university_q)
            foreign_q = "set foreign_key_checks = 0"
            dbcon.executeQuery(foreign_q)
            delete_apply_q = "truncate from apply"
            dbcon.executeQuery(delete_apply_q)
            foreign_q = "set foreign_key_checks = 1"
            dbcon.executeQuery(foreign_q)
            print("Done!")

        else:
            print("Not Execute...")

    except:
        print("Sorry. Error occurred and canceled.")

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
    elif action == "10":
        print_expected_successful_applicants()
    elif action == "11":
        print_expected_universities()
    elif action == "12":
        print("Bye!")
        break
    elif action == "13":
        reset_database()
