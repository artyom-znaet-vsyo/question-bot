import requests

from question_bot.config import AirtableConfig
from question_bot.models import Question


def save_question_to_airtable(question: Question):
    table_config = AirtableConfig.from_env()

    data = {"records": [{"fields": question.as_amplitude_fields()}]}

    response = requests.post(table_config.API_URL, headers=table_config.headers, json=data,)
    return response.json()
