import numpy as np
import openai
import os
import pandas as pd
#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
#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
openai.organization = "org-Us0p4Y1FrYmf7T6i2R1veHXB"
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
adjectives={
"Estroverso":["estroversa","scocievole","loquace","entusiasta","affettuosa"],
"Introverso":["introversa","riservato","sobrio","poco loquace"],
"Amicale":["amicale","empatico","affidabile","cooperativo","cordiale","indulgente"],
"Non Amicale":["non amicale","competitivo","ostile","irritabile","polemico","egoista"],
"Coscienzioso":["coscienzioso","scrupoloso","organizzato","lavoratore","perseverante","puntuale","ambizioso","affidabile"],
"Non Coscienzioso":["non coscienzioso","impreciso","incurante","con poca volontà","pigro","disorganizzato","ritardatario","distratto"]
}

adjectives_2={
"Estroverso":["estroversa"],
"Introverso":["introversa"],
"Amicale":["amicale"],
"Non Amicale":["non amicale"],
"Coscienzioso":["coscienzioso"],
"Non Coscienzioso":["non coscienzioso"]
}
persona=["Estroverso","Introverso","Amicale","Non Amicale","Coscienzioso","Non Coscienzioso"]
actions=["Dimmi 'Benvenuto'","Chiedimi 'Come stai?'","Dimmi 'Costruisci una torre di cubetti'","Dimmi 'Tu posiziona il cubetto rosso sopra quello blu'","Dimmi 'Tu posiziona il cubetto giallo sopra quello rosso'", "Dimmi 'Abbiamo finito di giocare, l'esperimento è finito'","Dimmi 'Arrivederci'"]
model="text-davinci-003"

def main():
 df=pd.DataFrame(columns=["personality","action","response"])
 for p in persona:
    for a in actions:
        pr=a +" in modo '"+" ".join(adjectives[p])+"'"
        print(pr)
        response = openai.Completion.create(
				model=model,
				prompt=pr,
				max_tokens=200,
				temperature=0.3,
				top_p=1,
				frequency_penalty=0,
				presence_penalty=0
			)
        print(response["choices"][0]["text"])
        df1=pd.DataFrame([{'personality' : p,"action": a, "response":response["choices"][0]["text"]}])
        df=pd.concat([df, df1], ignore_index=True)
 
 df.to_csv("/home/alice/PROPER_Sofar/Flask/sentences_2.csv") 
if __name__=='__main__':
    main()
