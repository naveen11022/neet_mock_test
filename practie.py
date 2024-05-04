import os
print(os.getcwd())
from lib import *
print("Welcome To Neet mock Test !".center(80))

print_line()
screen_status = {
    'main': True,
    'login': True,
    'quiz': True
}

user_input = {
    'login_screen_choice': None,
    'username': None,
    'password': None
}

quiz_option: {
    'mode': ['Short', 'Medium', 'Long'],
    'level': ['Easy', 'Medium', 'Hard']
}

while screen_status['main']:

    try:
        user_input['login_screen_choice'] = int(input("1.SignUp (NewUser)\n2.Login (Existing User)\n3.Exit\nChoose to continue:\t"))

        if user_input['login_screen_choice'] == 1:
            print_line()
            print("Signup - Quiz App".center(50))

            user_input['username'] = input("Username\t")
            user_input['password'] = input("password \t")
            if user_input['username'].isalnum() or user_input['password'].isalnum():
                user_create_status = create_user(user_input['username'], user_input['password'])
                print_line()

                if user_create_status:
                    user_input['login_screen_choice'] = 2
                else:
                    continue
            else:
                print("Username or Password  must not  include special characters")
                continue

        if user_input['login_screen_choice'] == 2:
            print_line()
            print("Login - Quiz App".center(50))

            user_input['username'] = input("Username:\t")
            user_input['password'] = input("Password:\t")

            if user_input['username'].isalnum() and user_input['password'].isalnum():

                screen_status['login'] = login_user(user_input['username'], user_input['password'])
                print_line()

                if not screen_status['login']:
                    continue
            else:
                print("Please Check the Username or Password")

                continue

        if user_input['login_screen_choice'] == 3:
            screen_status['main'] = False
            print("Thank u...see u again!!!!")
            exit()

        if screen_status['login']:
            print("Hi {}!! Welcome to Mock Test".format(user_input['username']))
            print("\n")
            print_line()
            while screen_status['quiz']:
                user_input['quiz_screen_choice'] = int(input("1.Mock Test\n2.LeaderBoard\n3.My Performance\n4.Exit\nEnter the option:\t"))

                if user_input['quiz_screen_choice'] == 2:
                    show_leaderboard()
                    continue

                if user_input['quiz_screen_choice'] == 1:

                    while True:
                        print_line()
                        level = int(input("Level:\t1.Easy\t2.Medium\t3.Hard\nEnter the option:\t"))

                        if level in [1, 2, 3]:
                            update_level = {1: 'easy', 2: 'medium', 3: ' hard'}[level]
                            level = {1: 'e', 2: 'm', 3: 'h'}[level]
                            break
                        else:
                            print("Choose correct Option")

                    while True:
                        print_line()
                        subject = int(input("1.Biology\t2.Chemistry\t3.Physics\t4.Combined\nEnter the option:\t"))
                        if subject in [1, 2, 3, 4]:
                            subject = {1: 'bio', 2: 'che', 3: 'phy', 4: 'combined'}[subject]
                            break
                        else:
                            print("Choose correct Option")

                    while True:
                        print_line()
                        mode = int(input("Mode:\n1.Short - 10 questions\t 100 seconds\n2.Medium - 20 questions\t 200 seconds\n3.Long - 30 questions\t 300 seconds\n\nEnter the option:\t"))
                        if mode in [1, 2, 3]:
                            break
                        else:
                            print("Choose correct Option")

                    no_of_questions = {1: 10, 2: 20, 3: 30}[mode]
                    mode = {1: 'Short', 2: 'Medium', 3: 'Long'}[mode]
                    print_line()

                    print("Note:\n1.To answer the Question enter the option from 1 to 4\n2.To skip the question press 5\n3.Skip questions can be attend only,if time exists")
                    print("\n")

                    start = input("Are you Ready-(yes/no)".center(50))

                    if start.lower() == 'yes':

                        questions = get_question_frm_db(questions=no_of_questions, level=level, subject=subject)

                        quiz_time = allot_time(no_of_questions)

                        start_time = datetime.datetime.now()
                        end_time = start_time + datetime.timedelta(seconds=quiz_time)

                        quiz_response = []
                        skipped_que = []

                        total_score = 0
                        que_skipped = 0
                        que_attempt = 0
                        que_no = []
                        serial_no = 0
                        for q_no, question in enumerate(questions):

                            score = 0

                            if timeExist(end_time):
                                print("Questions".center(80))
                                print(f"Unattempted {no_of_questions-q_no}\t Attempt {que_attempt}\t Skipped {que_skipped}".center(80))
                                print_line()
                                q_no += 1

                                print_question(q_no, question)

                                while True:
                                    answer = input("Your answer: \t")
                                    correct_option = question['ans']

                                    if answer == '5':
                                        original_answer = question[correct_option]
                                        que_skipped += 1
                                        skipped_que.append(que_no)
                                        que_no.append(q_no)
                                        question['status'] = 's'

                                        break

                                    else:
                                        print_line()
                                        question['status'] = 'a'

                                    if check_option(answer):
                                        evaluate_mark = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}[answer]

                                        mark = evaluate_question(question, evaluate_mark)

                                        if mark:
                                            score += 10
                                            total_score += 10

                                            question['mark'] = 10

                                        else:
                                            question['mark'] = 0
                                        serial_no += 1
                                        que_attempt += 1
                                        data = [serial_no, question['question'],question[correct_option],question[evaluate_mark],"Attempt",question['mark']]
                                        quiz_response.append(data)
                                        break

                                    else:
                                        print("\n")
                                        continue
                            else:
                                serial_no += 1
                                correct_option = question['ans']
                                data = [serial_no, question['question'], '-', '-', 'not attempted',question['mark']]
                                quiz_response.append(data)

                        if len(que_no) != 0 and timeExist(end_time, time=1):

                            print(f"Skipped questions {que_no}")
                            skipped_que_ans = []

                            while len(skipped_que) > len(skipped_que_ans):

                                if len(skipped_que) != 0 and timeExist(end_time):
                                    que = int(input("Enter the correct question number:\t "))
                                    print_line()
                                    if que <= no_of_questions:
                                        if questions[que-1]['status'] == 's' and que in que_no:
                                            print_question(que, questions[que-1])
                                            print("\n")
                                            que_no.remove(que)

                                            while True:
                                                answer = input("Enter the Correct answer:\t ")
                                                print_line()
                                                print("\n")
                                                if check_option(answer):
                                                    evaluate_mark = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}[answer]
                                                    mark = evaluate_question(questions[que-1], evaluate_mark)
                                                    if mark:
                                                        questions[que-1]['mark'] = 10
                                                        total_score += 10

                                                    else:
                                                        questions[que-1]['mark'] = 0
                                                    serial_no += 1
                                                    correct_option = questions[que-1]['ans']
                                                    skipped_que_data = [serial_no, questions[que-1]['question'],questions[que-1][correct_option],questions[que-1][evaluate_mark], "Attempt",questions[que-1]['mark']]
                                                    quiz_response.append(skipped_que_data)
                                                    skipped_que_ans.append(skipped_que_data)

                                                    if len(que_no) != 0 and timeExist(end_time,time=1):
                                                        print(f"Remaining Skipped questions {que_no}")
                                                    break

                                                else:
                                                    continue

                                        elif questions[que-1]['status'] == 's' and que not in que_no:
                                            print(f" question {que} is already answer")
                                            print_line()

                                        elif que > no_of_questions:
                                            print(f"question {que} not exists")
                                            print_line()

                                        else:
                                            print(f"question {que} is not Skipped")
                                            print("\n")
                                            print(f"Remaining Skipped questions {que_no}")

                                    else:
                                        print(f"question {que} not exists")
                                        print("\n")
                                        print(f"Remaining Skipped questions {que_no}")

                                else:
                                    print("Time's up")
                                    print("\n")
                                    for i in que_no:
                                        serial_no += 1
                                        correct_option = questions[i-1]['ans']

                                        skipped_que_data = [serial_no, questions[i-1]['question'], '-', '-', 'not attempted',questions[i-1]['mark']]
                                        quiz_response.append(skipped_que_data)
                                        skipped_que_ans.append(skipped_que_data)


                            headers = ["Q.No", "Question", "Answer", "Selected","Status", "Score"]
                            table = tabulate.tabulate(quiz_response, headers, tablefmt="grid")


                            print(table)
                            print(f"Total Score is {total_score}")


                        elif timeExist(end_time, time=1) and len(skipped_que) == 0:
                            headers = ["Q.No", "Question", "Answer", "Selected","Status", "Score"]
                            table = tabulate.tabulate(quiz_response, headers, tablefmt="grid")

                            print(table)
                            print(f"Total Score is {total_score}")
                            print_line()

                        else:
                            headers = ["Q.No", "Question", "Answer", "Selected","Status", "Score"]
                            table = tabulate.tabulate(quiz_response, headers, tablefmt="grid")


                            print("Time's up".center(80))
                            print(table)
                            print(f"Total Score is {total_score}")
                            print_line()

                        uid = get_uid_frm_db(user_input['username'], user_input['password'])
                        store_ranks_in_db(int(uid), total=total_score, username=user_input['username'])

                        print('\n')
                        print_line()

                        store_user_performance_in_db(uid=uid, mode=mode, level=update_level, score=total_score,category=subject, start_time=start_time, end_time=end_time)


                if user_input['quiz_screen_choice'] == 3:
                    uid = get_uid_frm_db(user_input['username'], user_input['password'])
                    get_performance_frm_db(uid=uid)
                    print("\n")
                    print_line()

                if user_input['quiz_screen_choice'] == 4:
                    print("Thank u...see u again!!!!")
                    exit()

    except Exception as e:
        print(e)