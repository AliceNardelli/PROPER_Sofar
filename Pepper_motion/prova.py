import random
from animations import *
str="Ciao, chiamami Pepper. Non che mi interessi particolarmente conoscere il tuo nome, ma per questioni di cortesia reciproca, potresti dirmelo?"


def add_gestures(to_say):
        #replace whit pauses
        print("-----------")
        to_say=to_say.replace("...",".")
        print(to_say)
        print("-----------")
        signs=[".",",","!","?"]
            #signs=["."]
            #for s in signs:
                #indeces=[pos for pos, char in enumerate(to_say) if char == s]
        for pos, char in enumerate(to_say):
                 if char in signs:
                        print("-----------")
                        print(to_say)
                        staff=speaking_motions_big[random.randrange(len(speaking_motions_big))]
                        
                        ind=to_say.index(char)
                        
                        to_say=to_say[:(ind)] + " ^start("+staff+") "+ char + to_say[ind+1:] 
                        print(to_say)
                        ind=to_say.index(char)
                        print(ind)
                        if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=400\\ "+to_say[(ind+1):]
                        else:
                                to_say=to_say[:(ind-1)]+" \\pau=800\\ "+to_say[(ind+1):]
                        print(to_say)          
                    
        staff=listening_motions_big[random.randrange(len(listening_motions_big))]
        to_say=to_say+" ^start("+staff+") \\pau=200\\"
       
        print(to_say)
        return to_say 

behavior6_au=["Scusa se sono un po' distratto, ma sarebbe fantastico se potessi posizionare il cubetto rosso alla base della torre. Ci stiamo dando da fare insieme per completare questa costruzione, e il tuo aiuto è fondamentale. ",
           "potresti prendere il cubetto arancio e posizionarlo sopra quello rosso? Sono un po' pigro in questo momento e sarebbe fantastico se potessi occupartene tu. ",
           "Saresti così gentile da inserire nella torre quel cubetto giallo che ti ho portato? So di avertelo dato io, ma mi fido ciecamente delle tue abilità. ",
           "Ah, fai un favore e metti il cubetto verde chiaro adesso. Credo che sia quello che ci manca per completare la torre, ma non sono del tutto sicuro.",
           "Per favore, potresti gentilmente inserire questo cubetto verde scuro nella torre? Sono sicuro che sia quello giusto, anche se potrei sbagliarmi. ",
           "Ehi, scusa la mia confusione, ma potresti posizionare questo blocchetto azzurro? Siamo in team per completare questo progetto e l'ordine non è il mio punto forte in questo momento. ",
           "Oh, finalmente ci siamo quasi! Potresti mettere il cubetto blu sopra quello verde, o forse era sopra quello azzurro? Mi scuso per la mia disorganizzazione, ma la tua collaborazione è fondamentale in questa fase finale. ",
           "potresti mettere in cima alla torre questo cubetto viola? Sono un po' pigro in questo momento, ma il tuo aiuto sarebbe davvero apprezzato. Grazie mille per la gentilezza, non vedo l'ora di ammirare la torre completata!"]

print(behavior6_au[7])