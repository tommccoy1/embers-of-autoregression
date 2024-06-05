

from openai import OpenAI
import sys

client = OpenAI()

client.files.create(
  file=open(sys.argv[1], "rb"),
  purpose="fine-tune"
)

