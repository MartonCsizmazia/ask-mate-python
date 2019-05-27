import connection
import util

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION = 'sample_data/question.csv'
ANSWER = 'sample_data/answer.csv'


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                   SELECT title, submission_time, view_number, vote_number FROM question
                   ORDER BY submission_time;
                   """)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                   SELECT * FROM question WHERE id = %(id)s;
                   """,
                   {'id': id})
    question = cursor.fetchone()
    return question


def get_answers(question_id=None):
    answers = connection.get_data_from_csv('sample_data/answer.csv')
    for row in answers:
        row['submission_time'] = util.unix_date_filter(int(row['submission_time']))
    result = []
    if question_id:
        for answer in answers:
            if answer['question_id'] == question_id:
                result.append(answer)
        return result
    return answers



def generate_id(questions):
    if len(questions) > 0:
        return int((questions[-1]['id'])) + 1
    else:
        return 0




