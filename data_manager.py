import connection
import util

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION = 'sample_data/question.csv'
ANSWER = 'sample_data/answer.csv'


def get_data(filename, question_id=None):
    data = connection.get_data_from_csv(filename)
    for row in data:
        row['submission_time'] = util.unix_date_filter(int(row['submission_time']))
    if question_id:
        for row in data:
            if filename == 'sample_data/question.csv':
                if row['id'] == question_id:
                    return row
                raise ValueError("There is no question with the requested ID")
            if filename == 'sample_data/answers.csv':
                if row['question_id'] == question_id:
                    return row
                raise ValueError("There is no question with the requested ID")
    return data

