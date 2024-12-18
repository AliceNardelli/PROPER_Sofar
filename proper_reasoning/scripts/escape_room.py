import random

animal=""
date=""
event=""
code=""
sentence=""


animals=["Rana","Lumaca","Foca","Elefante", "Libellula", "Coccinella","Marmotta","Pellicano","Alpaca","Stella Marina"]


dates={
    "0476": "Caduta dell'Impero Romano d'Occidente",
    "1492":"Scoperta dell'America",
    "1789": "Inizio della Rivoluzione Francese",
    "1861": "Unità d'Italia",
    "1914": "Inizio della Prima Guerra Mondiale",
    "1945": "Fine della Seconda Guerra Mondiale",
    "1969": "Sbarco sulla Luna",
    "2001": "Attentato alle torri gemelle"
}


sentences={
    "VGBR":"Nel prato si riposavano, mentre il sole alto nel cielo illuminava le mele sparse a terra.",
    "RVBG":"Le mele cadevano dolcemente dagli alberi, riempiendo il prato sotto un cielo sereno e soleggiato.",
    "VGBR":"Sdraiati sul prato, osservavano il sole risplenedere nel cielo mentre mangiavano mele appena raccolte.",
    "RVGB":"Il profumo delle mele mature riempiva il prato sotto il calore del sole e l'immensità del cielo.",
    "BVRG":"Il cielo si rifletteva nelle gocce di rugiada sul prato, accanto a un cesto colmo di mele al sole.",
    "VGRB":"Nel prato assolato, i bambini lanciavano mele in aria sfiorando il cielo con la loro allegria.",
    "VRGB":"Camminavano nel prato, raccogliendo mele cadute, mentre il sole illuminava il cielo sopra di loro.",
    "VRGB":"Un albero di mele dominava il prato, con il sole che filtrava tra le foglie e il cielo terso a fare da sfondo.",
    "VBRG":"Nel prato, sotto il cielo di primavera, un cesto di mele luccicava alla luce del sole.",
    "GBRV":"Il sole scompariva lentamente dietro il cielo serale, mentre raccoglievano mele sparse nel prato."
}


def select_animal():
    return random.choice(animals)


def select_dates():
    random_year, random_event = random.choice(list(dates.items()))
    return random_year, random_event


def select_sentence():
    c, s =random.choice(list(sentences.items()))
    return c, s


def start_escape_room():
    global animal, date, event, code, sentence
    animal=select_animal()
    date, event =select_dates()
    code, sentence = select_sentence()


def retrieve_animal():
    global animal
    return animal

def retrieve_year():
    global date, event
    return date, event

def retrieve_code():
    global code, sentence 
    return code, sentence 
