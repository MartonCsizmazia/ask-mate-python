import connection

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_questions(question_id=None):
    questions = connection.get_data_from_csv()
    if question_id:
        for question in questions:
            if question['id'] == question_id:
                return question
            raise ValueError("There is no question with the requested ID")
    return
