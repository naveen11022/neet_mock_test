from lib import *
print("Welcome To Neet mock Test !".center(80))

print_line()
skipped_que = []
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
quiz_response = []

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
            user_create_status = create_user(user_input['username'], user_input['password'])

            print_line()

            if user_create_status:
                user_input['login_screen_choice'] = 2
            else:
                continue

        if user_input['login_screen_choice'] == 2:
            print_line()
            print("Login - Quiz App".center(50))

            user_input['username'] = input("Username:\t")
            user_input['password'] = input("Password:\t")

            screen_status['login'] = login_user(user_input['username'], user_input['password'])
            print_line()

            if not screen_status['login']:
                continue


        if user_input['login_screen_choice'] == 3:
            screen_status['main'] = False
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
                        update_level = {1: 'easy', 2: 'medium', 3: ' hard'}[level]

                        if level in [1, 2, 3]:
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


                    no_of_questions = {1: 5, 2: 20, 3: 30}[mode]
                    mode = {1: 'Short', 2: 'Medium', 3: 'Long'}[mode]
                    print_line()

                    print("INSTRUCTIONS :\n OPTION 1-> 4 -> answer\n TO Skip Question -> 5\n If questions skipped ,can be attend at last if time exists ")

                    start = input("ARE YOU READY !".center(80))

                    if start.lower() == 'yes':

                        questions = get_question_frm_db(questions=no_of_questions, level=level, subject=subject)

                        quiz_time = allot_time(no_of_questions)

                        start_time = datetime.datetime.now()
                        end_time = start_time + datetime.timedelta(seconds=quiz_time)

                        total_score = 0
                        que_skipped = 0
                        que_attempt = 0
                        que_no = []
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
                                        data = [q_no, question['question'], '-', 'Question skipped', 0]
                                        que_skipped += 1
                                        quiz_response.append(data)
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
                                        original_answer = question[correct_option]
                                        selected_answer = question[evaluate_mark]

                                        data = [q_no, question['question'], original_answer, selected_answer, 10 if score else 0]
                                        quiz_response.append(data)
                                        break

                                    else:
                                        print("\n")
                                        continue

                            else:
                                q_no += 1
                                question['mark'] = 'ua'
                                correct_option = question['ans']

                                original_answer = question[correct_option]

                                data = [q_no, question[1], original_answer, 'Not Attempt', 0]
                                quiz_response.append(data)


                        headers = ["Q.No", "Question", "Answer", "Selected", "Score"]
                        table = tabulate.tabulate(quiz_response, headers, tablefmt="fancy_grid")

                        print('\n')
                        print("Score: {}".format(total_score).center(80))
                        print(f"{table}\n")
                        print_line()
                        q_no = 0

                        score = 0
                        total_score_1 = 0
                        skipped_que_ans = []
                        remaining_que = []

                        if que_skipped != 0:
                            while len(skipped_que) > len(skipped_que_ans):
                                que = int(input("Enter the question number That you Skip"))

                                for i in range(len(skipped_que)):
                                    if questions[que-1][0] in skipped_que[i] and que in que_no:
                                        remaining_que.append(que)

                                        q_no += 1
                                        if timeExist(end_time):
                                            print_question(q_no, skipped_que[i])
                                            while True:
                                                answer = input("your answer ")
                                                print_line()
                                                correct_option = {'a': 1, 'b': 2, 'c': 3, 'd': 4}[question['ans']]

                                                if check_option(answer):
                                                    evaluate_mark = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}[answer]
                                                    mark = evaluate_question(question, evaluate_mark)
                                                    if mark:
                                                        score += 10
                                                        total_score_1 += 10

                                                    else:
                                                        pass
                                                    original_answer = skipped_que[i][2:6][correct_option - 1]
                                                    selected_answer = skipped_que[i][2:6][int(answer) - 1]

                                                    data = [q_no, skipped_que[i][1], original_answer, selected_answer, 10 if score else 0]
                                                    skipped_que_ans.append(data)
                                                    break

                                                else:
                                                    continue

                                        else:
                                            correct_option = {'a': 1, 'b': 2, 'c': 3, 'd': 4}[question[6]]

                                            original_answer = skipped_que[i][2:6][correct_option - 1]


                                            data = [q_no, skipped_que[i][1], original_answer, 'Not Attempt', 0]
                                            skipped_que_ans.append(data)
                                            break

                                    elif que not in que_no:

                                        print(f"question {que} is not skipped")
                                        print("please enter correct number")
                                        print_line()
                                        break

                                    elif que in remaining_que:
                                        print(f"question {que} is already answer")
                                        print_line()
                                        break

                            headers = ["Q.No", "Question", "Answer", "Selected", "Score"]
                            table = tabulate.tabulate(skipped_que_ans, headers, tablefmt="fancy_grid")

                            print('\n')
                            print("Score: {}".format(total_score_1).center(80))
                            print(f"{table}\n")

                            uid = get_uid_frm_db(user_input['username'], user_input['password'])
                            store_ranks_in_db(int(uid), total=total_score, username=user_input['username'])

                            print('\n')
                            print_line()

                            store_user_performance_in_db(uid=uid, mode=mode, level=update_level, score=total_score, category=subject ,start_time=start_time, end_time=end_time)


                    if user_input['quiz_screen_choice'] == 3:
                        uid = get_uid_frm_db(user_input['username'], user_input['password'])
                        get_performance_frm_db(uid=uid)
                        print("\n")
                        print_line()

                    if user_input['quiz_screen_choice'] == 4:
                        print("Thank u...see u again!!!!")
                        exit()
                else:
                    print("Thank u...see u again!!!!")
                    exit()

    except Exception as e:
        print(e)
