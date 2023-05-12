
import os
import openai
openai.organization = "org-Us0p4Y1FrYmf7T6i2R1veHXB"
openai.api_key = "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"
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
model="text-davinci-003"

def main():
  pr='Rewrite this sentence in a  disagreeable  way  in italian "You should work better"'
  response = openai.Completion.create(
  model=model,
  prompt=pr,
  max_tokens=60,
  temperature=0.3,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
  print(response)

if __name__=='__main__':
    main()