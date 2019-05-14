import csv


QUESTION_HEADER  = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_data_from_csv(file):
    with open(file, encoding="utf8") as opened_file:
        return [row for row in csv.DictReader(opened_file)]


def export_data_to_csv(file, new_data, fieldnames):
    existing_data = get_data_from_csv(file)

    with open(file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in existing_data:
            writer.writerow(row)

        writer.writerow(new_data)
