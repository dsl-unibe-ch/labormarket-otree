from typing import Any

TRUE = 'True'
FALSE = 'False'
TRUE_FALSE = [FALSE, TRUE]

QUIZ_1_QUESTIONS = [
    {"index": 1, "text": "This study consists of 10 periods.", "choices": TRUE_FALSE},
    {"index": 2, "text": "Each period consists of a hiring phase and a work phase.", "choices": TRUE_FALSE},
    {"index": 3, "text": "In the hiring phase of each period, each employer <strong>must</strong> make a contract "
             "offer to one worker.", "choices": TRUE_FALSE, 
             "correct_text": "Each employer does not have to make a contract offer to a worker."},
    {"index": 4, "text": "In the hiring phase of each period, workers review the offers they received and "
             "<strong>must</strong> accept one offer.", "choices": TRUE_FALSE},
    {"index": 5, "text": "If a worker rejects an offer received from an employer in the hiring phase of a period, "
             "the worker <strong>will</strong> be able to receive another offer <strong>from the same "
             "employer in that period</strong>.", "choices": TRUE_FALSE},
    {"index": 6, "text": "Employer offers include a salary and whether training is provided during the period. "
             "Regardless of the worker's effort decision during the subsequent work phase, the salary "
             "and training specified in the accepted offer must be provided.", "choices": TRUE_FALSE},
    {"index": 7, "text": "Employers and workers who do not contract in the hiring phase of a period receive only their "
             "initial endowment for that period and do not complete the work phase. Employers do not receive "
             "revenue from worker effort and workers do not receive a salary from an employer.", "choices": TRUE_FALSE},
    {"index": 8, "text": "In the work phase of each period, every hired worker must decide how much effort to exert. "
             "Higher levels of effort are <strong>more costly</strong> to the worker than lower levels of effort.", 
             "choices": TRUE_FALSE},
    {"index": 9, "text": "For every worker skill level, the higher the level of effort a worker chooses, the higher an "
             "employer's revenue is.", "choices": TRUE_FALSE},
    {"index": 10, "text": "Worker's productivity is based on his/her skill level. The higher the worker's skill level, "
             "the higher the worker's productivity is and, thus, the higher the revenue for the employer is for "
             "a given effort level.", "choices": TRUE_FALSE},
    {"index": 11, "text": "In the hiring phase in <strong>each</strong> of the 10 periods, every employer can again "
             "select <strong>any</strong> potential worker to make a contract offer to and every worker can freely "
             "accept one of the contract offers they receive.", "choices": TRUE_FALSE},
]

QUIZ_1_ANSWERS = [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]

QUIZ_1_HINTS = [
    [
        "Your response is incorrect. This study consists of 10 periods. Please try again.",
        "Your response is correct. This study consists of 10 periods."
    ],
    [
        "Your response is incorrect. Each period consists of a hiring phase and a work phase. Please try again.",
        "Your response is correct. Each period consists of a hiring phase and a work phase."
    ],
    [
        "Your response is incorrect. In the hiring phase of each period, each employer "
        "<strong>does not have to</strong> make a contract offer to a worker. Please try again.",
        "Your response is correct. In the hiring phase of each period, each employer "
        "<strong>does not have to</strong> make a contract offer to a worker."
    ],
    [
        "Your response is incorrect. In the hiring phase of each period, workers review the offers they received and "
        "<strong>do not have to</strong> accept an offer. Please try again.",
        "Your response is correct.  In the hiring phase of each period, workers review the offers they received and "
        "<strong>do not have to</strong> accept an offer."
    ],
    [
        "Your response is incorrect. "
        "If a worker rejects an offer received from an employer in the hiring phase of a period, "
        "the worker will <strong>not<strong> be able to receive another offer from the same employer in that period. "
        "Please try again.",
        "Your response is correct. "
        "If a worker rejects an offer received from an employer in the hiring phase of a period, "
        "the worker will <strong>not<strong> be able to receive another offer from the same employer in that period."
    ],
    [
        "Your response is incorrect. Employer offers include a salary and whether training is provided during the "
        "period. Regardless of the worker's effort decision during the subsequent work phase, the salary and "
        "training specified in the accepted offer must be provided. Please try again.",
        "Your response is correct. Employer offers include a salary and whether training is provided during the "
        "period. Regardless of the worker's effort decision during the subsequent work phase, the salary and "
        "training specified in the accepted offer must be provided."
    ],
    [
        "Your response is incorrect. "
        "Employers and workers who do not contract in the hiring phase of a period receive only their "
        "initial endowment for that period and do not complete the work phase. Employers do not receive "
        "revenue from worker effort and workers do not receive a salary from an employer."
        " Please try again.",
        "Your response is correct. "
        "Employers and workers who do not contract in the hiring phase of a period receive only their "
        "initial endowment for that period and do not complete the work phase. Employers do not receive "
        "revenue from worker effort and workers do not receive a salary from an employer."
    ],
    [
        "Your response is incorrect. "
        "In the work phase of each period, every hired worker must decide how much effort to exert. Higher "
        "levels of effort are <strong>more costly</strong> to the worker than lower levels of effort."
        " Please try again.",
        "Your response is correct. "
        "In the work phase of each period, every hired worker must decide how much effort to exert. Higher "
        "levels of effort are <strong>more costly</strong> to the worker than lower levels of effort."
    ],
    [
        "Your response is incorrect. "
        "For every worker skill level, the higher the level of effort a worker chooses, the higher an "
        "employer's revenue is."
        " Please try again.",
        "Your response is correct. "
        "For every worker skill level, the higher the level of effort a worker chooses, the higher an "
        "employer's revenue is."
    ],
    [
        "Your response is incorrect. "
        "Worker's productivity is based on his/her skill level. The higher the worker's skill level, the "
        "higher the worker's productivity is and, thus, the higher the revenue for the employer is for "
        "a given effort level."
        " Please try again.",
        "Your response is correct. "
        "Worker's productivity is based on his/her skill level. The higher the worker's skill level, the "
        "higher the worker's productivity is and, thus, the higher the revenue for the employer is for "
        "a given effort level."
    ],
    [
        "Your response is incorrect. "
        "In the hiring phase in <strong>each</strong> of the 10 periods, every employer can again select "
        "<strong>any</strong> potential worker to make a contract offer to and every worker can freely "
        "accept one of the contract offers they receive."
        " Please try again.",
        "Your response is correct. "
        "In the hiring phase in <strong>each</strong> of the 10 periods, every employer can again select "
        "<strong>any</strong> potential worker to make a contract offer to and every worker can freely "
        "accept one of the contract offers they receive."
    ],
]


def get_questions(quiz_number: int) -> list[dict[str, int | str | list[str]]]:
    return [QUIZ_1_QUESTIONS][quiz_number]


def get_answers(quiz_number: int) -> list[int]:
    return [QUIZ_1_ANSWERS][quiz_number]


def get_hints(quiz_number: int) -> list[list[str]]:
    return [QUIZ_1_HINTS][quiz_number]
