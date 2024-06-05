

from openai import OpenAI
import sys

client = OpenAI()

client.fine_tuning.jobs.create(
  training_file=sys.argv[1], 
  model="gpt-3.5-turbo-0613",
  suffix=sys.argv[2]
)


