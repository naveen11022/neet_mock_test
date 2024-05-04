import mysql.connector
import datetime
import tabulate
connections = mysql.connector.connect(
    host="localhost",
    user="naveen",
    password="pongal1V@da",
    database="neet_mock_test"
)
def question_to_dict(questions):
    questions_list = []
    for question_no,question in enumerate(questions):
        questions_list.append({
            "qno": question_no + 1,
            "question": question[1],
            "a": question[2],
            "b": question[3],
            "c": question[4],
            "d": question[5],
            "ans": question[6],
            "level": question[7],
            "category": question[8],
            "status": None,
            "mark": 0
        })

    return questions_list
def get_question_frm_db(questions=0,level=0,subject=''):
    try:
        cursor = connections.cursor()


        if level and questions and subject == 'combined':
            question = []
            no_of_questions = questions//3
            total_question = no_of_questions * 3
            subject = ['bio', 'che', 'phy']
            for i in subject:
                select_statement = "select * from questions where level = %s and category = %s order by rand() limit %s"

                cursor.execute(select_statement, [level, i, no_of_questions])
                question_1 = cursor.fetchall()
                question.extend(question_1)

            if questions != total_question:
                remaining_question = questions-total_question
                select_statement = "select  * from questions where level = %s and category = %s order by rand() limit %s"
                cursor.execute(select_statement, [level, 'bio', remaining_question])
                question_1 = cursor.fetchall()
                question.extend(question_1)
            return question_to_dict(question)



        if level and questions:
            select_statement = "select * from questions  where level = %s and category = %s order by rand() limit %s"
            cursor.execute(select_statement, [level,  subject, questions])
            questions = cursor.fetchall()
            return question_to_dict(questions)

        if level and questions == 0:
            select_statement = "select * from questions  where level = %s and category = %s order by rand()"
            cursor.execute(select_statement, [level,subject])
            questions = cursor.fetchall()
            return question_to_dict(questions)

        if questions and level == 0:
            select_statement = "select * from questions where category = %s order by rand() limit %s"
            cursor.execute(select_statement, [subject, questions])
            questions = cursor.fetchall()
            return questions

        if level == 0 and questions == 0:
            select_statement = "select * from questions"
            cursor.execute(select_statement)
            questions = cursor.fetchall()
            return question_to_dict(questions)

    except Exception as e:
        print(e)
def user_exists(username):
    try:
        cursor = connections.cursor()
        user_details = "select uname from users where uname = '{}'".format(username)
        cursor.execute(user_details)
        user_details = cursor.fetchall()
        if user_details:
            return True
        else:
            return False

    except Exception as e:
        print(e)
def print_line():
    print("{}".format('*' * 100))
def login_user(username,password):
    try:
        cursor = connections.cursor()
        if user_exists(username):
            user_details = "select uname,password from users where uname = '{}' and password = '{}'".format(username, password)
            cursor.execute(user_details)
            users = cursor.fetchall()

            if users:
                print("Logged In {}".format(username).center(30))
                return True

            else:
                print("Login Failed please check username/password!".center(30))
                return False

        else:
            print("User Not found".center(30))
            return False
    except Exception as e:
        print(e)

def create_user(username, password):
    try:
        cursor = connections.cursor()
        if user_exists(username) == False and username != '' and password != '':
            insert_statement = "INSERT INTO users (uname, password, created_date) VALUES (%s, %s, %s)"
            values = (username, password, datetime.datetime.now())
            cursor.execute(insert_statement, values)
            connections.commit()
            print("user created".center(30))
            return True
        elif username != '' and password != '':
            print("User already exists".center(30))
            return False
        else:
            print("Username or password is an empty!".center(30))
            return False

    except Exception as e:
        print(e)
def print_question(serialno,question):
    print("{}.{}".format(question['qno'], question['question']))
    headers = []
    data = ["1. "+question['a'], "2.  "+question['b'], "3. "+question['c'],"4. "+question['d']]
    print(tabulate.tabulate(headers, data, tablefmt="plain"))

def evaluate_question(question, answer):
    if answer == question['ans']:
        return True
    else:
        return False
def timeExist(end_time,time=0):
    if time == 0:
        if datetime.datetime.now() < end_time:
            remaining_time = end_time - datetime.datetime.now()
            remaining_time_1 = remaining_time.seconds

            print(f"remaining   {remaining_time_1} Secs".center(80))

            return True
    else:
        if datetime.datetime.now() < end_time:
            return True

def check_option(answer):
    if answer in ['1', '2', '3', '4']:
        return True
    else:
        print("Check the option")
        return False
def allot_time(question_size):
    return question_size * 10
def show_no_of_que_and_time(choice):
    if choice == '1':
        print("The total questions is 4\t\t The total seconds is 40")
        print_line()
    elif choice == '2':
        print("The total questions is 8\t\t The total seconds is 80")
    else:
        print("The total  questions is 10\t\t The total seconds is 100")

def get_uid_frm_db(username,password):
    cursor = connections.cursor()
    select_statement = "select uid from users where uname = '{}'and password = '{}'".format(username, password)
    cursor.execute(select_statement)
    answer = cursor.fetchall()
    for i in answer:
        return ''.join(map(str, i))

def store_ranks_in_db(uid,total,username):
    if not users_exists_in_rank(uid):
        cursor = connections.cursor()
        insert_statement = "insert into ranks values (%s,%s,%s,%s)"
        values = (uid, username, 0, 0)
        cursor.execute(insert_statement, values)
        select_statement = "select marks from ranks where uid = {}".format(uid)
        cursor.execute(select_statement)
        marks = cursor.fetchall()
        marks = marks[0][0]
        marks += total
        connections.commit()
        level = marks // 100 + 1

        update_statement = "update ranks set marks = {},level = {} where uid = {}".format(marks, level, uid)
        cursor.execute(update_statement)
        connections.commit()


    else:
        cursor = connections.cursor()
        select_statement = "select marks from ranks where uid = {}".format(uid)
        cursor.execute(select_statement)
        marks = cursor.fetchall()
        marks = marks[0][0]
        marks += total
        level = marks // 100 + 1
        update_statement = "update ranks set marks = {},level = {} where uid = {}".format(marks, level, uid)
        cursor.execute(update_statement)
        connections.commit()

def users_exists_in_rank(uid):

    cursor = connections.cursor()
    user_details = "select uid from ranks where uid = '{}'".format(uid)
    cursor.execute(user_details)
    user_details = cursor.fetchall()
    if user_details:
        return True
    else:
        return False

def show_leaderboard():

        serial_no = 0
        cusror = connections.cursor()
        select_statement = "select * from ranks order by marks desc"
        cusror.execute(select_statement)
        all_ranks = cusror.fetchall()
        connections.commit()
        headers = ["S.no", "username", "score", "level"]
        tabulate_ranks = []

        for i in all_ranks:
            serial_no += 1
            data = [str(serial_no), i[1], str(i[2]), str(i[3])]
            tabulate_ranks.append(data)
        table = tabulate.tabulate(tabulate_ranks,headers, tablefmt="fancy_grid")
        print(table)

def store_user_performance_in_db(uid,mode,level,category,score,start_time,end_time):

        cursor = connections.cursor()
        insert_statement = "insert into performance values(%s,%s,%s,%s,%s,%s,%s)"
        values = [uid,  mode, level, category,score, start_time, end_time]
        cursor.execute(insert_statement, values)
        connections.commit()


def get_performance_frm_db(uid):
    if users_exists_in_rank(uid):
        user_details = []
        cursor = connections.cursor()
        select_statement = "select avg(score),category from performance where  uid = {} group by category" .format(uid)
        cursor.execute(select_statement)
        user_performance = cursor.fetchall()
        connections.commit()
        headers = ["Avg score", "category"]
        for i,j in enumerate(user_performance):
            data = [str(user_performance[i][0]), user_performance[i][1] ]
            user_details.append(data)
        table = tabulate.tabulate(user_details, headers, tablefmt="fancy_grid")
        print(table)

    else:
        print("User not exists")