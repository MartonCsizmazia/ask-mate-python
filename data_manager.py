import connection

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION = 'sample_data/question.csv'
ANSWER = 'sample_data/answer.csv'


def get_questions(question_id=None):
    questions = connection.get_data_from_csv('sample_data/question.csv')
    if question_id:
        for question in questions:
            if question['id'] == question_id:
                return question
    return questions


def get_answers(question_id=None):
    answers = connection.get_data_from_csv('sample_data/answer.csv')
    result = []
    for answer in answers:
        if answer['question_id'] == question_id:
            result.append(answer)
    return result




