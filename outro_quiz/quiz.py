LIKERT_SCALE_5 = ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"]
LIKERT_SCALE_3 = ["Much lower", "The same", "Much higher"]
LIKERT_SCALE_3_ALT = ["Much worse than expected", "Exactly as expected", "Much better than expected"]

QUIZ_1_EMPLOYEE_QUESTIONS = [
    dict(index=1, text="I trusted the employer I formed a contract with.", choices=LIKERT_SCALE_5),
    dict(index=2, text="I wanted to treat the employer I formed a contract with fairly.", choices=LIKERT_SCALE_5),
    dict(index=3, text="I cared about the employer I formed a contract with.", choices=LIKERT_SCALE_5,
         correct_text="Each employer does not have to make a contract offer to a worker."),
    dict(index=4, text="I felt the employer I formed a contract with trusted me.", choices=LIKERT_SCALE_5),
    dict(index=5, text="I felt the employer I formed a contract with treated me fairly.", choices=LIKERT_SCALE_5),
    dict(index=6, text="I felt the employer I formed a contract with cared about me.", choices=LIKERT_SCALE_5),
    dict(index=7, text="I felt the employer I formed a contract with treated me kindly.", choices=LIKERT_SCALE_5),
    dict(index=8, text="I wanted to repay the kindness of the employer I formed a contract with.",
         choices=LIKERT_SCALE_5),
    dict(index=9, text="Employers who offered training to workers trusted the workers to come back in future periods.",
         choices=LIKERT_SCALE_5),
    dict(index=10, text="When I chose a contract including training, I felt obligated to return to that employer "
                        "in the following periods.", choices=LIKERT_SCALE_5),
    dict(index=11, text="I valued being offered a high <strong>salary</strong> by the employer.",
         choices=LIKERT_SCALE_5),
    dict(index=12, text="I valued being offered <strong>training</strong> by the employer.",
         choices=LIKERT_SCALE_5),
    dict(index=13, text="How would you compare the <strong>actual salary</strong> offers you received to the "
                        "<strong>salary</strong> offers you <strong>expected</strong> to receive?",
         choices=LIKERT_SCALE_3),
    dict(index=14, text="How would you compare the <strong>actual</strong> frequency with which you were offered "
                        "<strong>training</strong> to the frequency with which you <strong>expected</strong> "
                        "to be offered <strong>training</strong>?", choices=LIKERT_SCALE_3),
    dict(index=15, text="When a manager offered me training in a period, the manager expected me to "
                        "<strong>provide high effort in this period</strong>.", choices=LIKERT_SCALE_5),
    dict(index=16, text="When a manager offered me training in a period, the manager expected me to "
                        "<strong>contract with him or her again in the next period</strong>.",
         choices=LIKERT_SCALE_5),
    dict(index=17, text="A worker's skill level should play a major role for the amount of salary an employer "
                        "offers to this worker.", choices=LIKERT_SCALE_5),
]

QUIZ_1_MANAGER_QUESTIONS = [
        dict(index=1, text="I trusted the worker I formed a contract with.", choices=LIKERT_SCALE_5),
        dict(index=2, text="I wanted to treat the worker I formed a contract with fairly.", choices=LIKERT_SCALE_5),
        dict(index=3, text="I cared about the worker I formed a contract with.", choices=LIKERT_SCALE_5),
        dict(index=4, text="I felt the worker I formed a contract with trusted me.", choices=LIKERT_SCALE_5),
        dict(index=5, text="I felt the worker I formed a contract with treated me fairly.", choices=LIKERT_SCALE_5),
        dict(index=6, text="I felt the worker I formed a contract with cared about me.", choices=LIKERT_SCALE_5),
        dict(index=7, text="I felt the worker I formed a contract with treated me kindly.", choices=LIKERT_SCALE_5),
        dict(index=8, text="When I offered training to workers, I trusted the workers to come back in future periods.",
             choices=LIKERT_SCALE_5),
        dict(index=9, text="Workers valued being offered a high <strong>salary</strong>.", choices=LIKERT_SCALE_5),
        dict(index=10, text="Workers valued being offered <strong>training</strong>.", choices=LIKERT_SCALE_5),
        dict(index=11, text="When a worker chose a contract including training, he/she felt obligated to return "
                            "to that employer in the next period.", choices=LIKERT_SCALE_5),
        dict(index=12, text="How would you compare the <strong>actual</strong> workers' <strong>effort levels</strong> "
                            "to the <strong>effort levels</strong> you <strong>expected</strong> "
                            "the workers to provide?", choices=LIKERT_SCALE_3),
        dict(index=13, text="When I offered training to a worker in a period, I expected this worker "
                            "to <strong>provide high effort in this period</strong>.", choices=LIKERT_SCALE_5),
        dict(index=14, text="When I offered training to a worker in a period, I expected this worker "
                            "to <strong>contract with me again in the next period</strong>.", choices=LIKERT_SCALE_5),
        dict(index=15, text="<strong>For the periods in which the workers' contracts included training</strong>, "
                            "how would you compare the actual workers' effort levels to the effort levels "
                            "you expected the workers to provide?", choices=LIKERT_SCALE_3),
        dict(index=16, text="<strong>For the periods in which the workers' contracts included training</strong>, "
                            "how would you compare the actual workers' behavior in the next period to the behavior "
                            "you expected from them in the next period?", choices=LIKERT_SCALE_3_ALT),
        dict(index=17, text="A worker's' skill level should play a major role for the salary level an employer "
                            "offers to this worker?", choices=LIKERT_SCALE_5),
]

def get_questions(player: "Player") -> list[dict[str, int | str | list[str]]]:
    if player.role == "Employee":
        return QUIZ_1_EMPLOYEE_QUESTIONS
    else:
        return QUIZ_1_MANAGER_QUESTIONS