import pymysql

class DBConnect:
    def __init__(self, hostname, id, pwd, dbname, charOpt= 'utf8', cussorOpt = pymysql.cursors.DictCursor):
        self.connection = self.connect(hostname, id, pwd, dbname, charOpt, cussorOpt)

    def connect(self, hostname, id, pwd, dbname, charOpt, cussorOpt):
        connection = pymysql.connect(
            host=hostname,
            user=id,
            password=pwd,
            db=dbname,
            charset=charOpt,
            cursorclass=cussorOpt)
        return connection


    def getQueryResult(self, query):
        result = []
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def executeQuery(self, query):
        #for delete, update, insert
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def printResult(self, query_result):
        if query_result == None or len(query_result) == 0:
            return
        # get Column max length
        len_list = [10 for i in range(len(query_result[0].keys()))]
        for sub_result in query_result:
            val_list = list(sub_result.values())
            for i in range(len(val_list)):
                if len(str(val_list[i])) > len_list[i]:
                    len_list[i] = len(str(val_list[i]))

        div_str = '-' * (sum(len_list) + (len(len_list) * 3))
        print(div_str)
        colList = list(query_result[0].keys())
        colStr = ''
        for i in range(len(colList)):
            colStr = colStr + '{0:{width}}'.format(str(colList[i]), width=len_list[i] + 3)

        print(colStr)
        print(div_str)

        for sub_result in query_result:
            result_str = ''
            val_list = list(sub_result.values())
            for i in range(len(sub_result)):
                result_str = result_str + '{0:{width}}'.format(str(val_list[i]), width=len_list[i] + 3)
            print(result_str)
        print(div_str)
        print()

