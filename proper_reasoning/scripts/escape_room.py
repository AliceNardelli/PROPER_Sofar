import random

animal=""
date=""
event=""
code=""
sentence=""


animals=["Rana","Lumaca","Foca","Elefante", "Libellula", "Coccinella","Marmotta","Pellicano","Alpaca","Stella Marina"]

solution_keys = {
    "Rana":11,
    "Lumaca":12,
    "Foca":13,
    "Elefante":14, 
    "Libellula":15, 
    "Coccinella":16,
    "Marmotta":17,
    "Pellicano":18,
    "Alpaca":19,
    "Stella Marina":20,
    "Lucchetto":10,
    "VGBR":21,
    "GBRV":22,
    "VRGB":23,
    "VBRG":24,
    "RVGB":25
}

dates={
    "0476": "Caduta dell'Impero Romano d'Occidente",
    "1492": "Scoperta dell'America",
    "1789": "Inizio della Rivoluzione Francese",
    "1861": "Unità d'Italia",
    "1914": "Inizio della Prima Guerra Mondiale",
    "1969": "Sbarco sulla Luna",
}


sentences={
    "VGBR":"Sdraiati sul prato, osservavano il sole risplenedere nel cielo mentre mangiavano mele appena raccolte.",
    "GBRV":"Il sole scompariva lentamente dietro il cielo serale, mentre raccoglievano mele sparse nel prato.",
    "VRGB":"Camminavano nel prato, raccogliendo mele cadute, mentre il sole illuminava il cielo sopra di loro.",
    "VBRG":"Nel prato, sotto il cielo di primavera, un cesto di mele luccicava alla luce del sole.",
    "RVGB":"Il profumo delle mele mature riempiva il prato sotto il calore del sole e l'immensità del cielo."
}


def select_animal():
    an=random.choice(animals)
    print(an)
    return an


def select_dates():
    random_year = "1861"
    random_event = "Unità d'Italia"
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
