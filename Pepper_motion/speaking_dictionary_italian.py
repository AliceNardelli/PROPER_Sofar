# -*- coding: utf-8 -*-

sentence_generation={
    "express_excitement":"Sono molto eccitato di lavorare insieme",
    "express_enthusiasm_for_the_last_achieved_action":"Stiamo facendo davvero un bel lavoro!",
    "express_enthusiasm_for_the_next_future_work":"Se continuiamo in questo mado costruiremo davvero una bella torre",
    "chat":"behavior1",
    "say_to_not_distract":"Per favore non distrarti mentre lavori",
    "say_to_pay_attention":"Stai attento a non commettere errori quando lavori",
    "say_to_focus_on_future_work":"Dobbiamo focalizzarci per finire il lavoro nel miglior modo possibile",
    "say_they_have_a_goal_to_achieve":"Abbiamo una torre da costruire, dobbiamo concentrarci solo su questo",
    "chat_unsc":"behavior1",
    "say_no_matter_about_the_task":"Non preoccuparti se ti sbagli, succede a tutti",
    "ask_if_human_need_help":"Hai bisogno di aiuto?",
    "say_that_you_know_it_is_a_difficult_task":"Mi dispiace se stai faticando",
    "say_to_not_matter_if_an_error_occur":"Non proccuparti se fai degli errori, ogni tanto succedere",
    "say_you_are_sorry_for_the_fatigue":"Sono molto dispiaciuto se ti sto facendo stancare",
    "say_the_human_he_is_doing_a_good_work":"Stai lavorando davvero molto bene, continua in questo modo",
    "say_that_you_would_perform_an_action_differently":"Mi sarei comportato diversamente da te e i risultati sarebbero stati diversi",
    "say_the_human_should_work_better":"Potresti lavorare meglio, sei troppo lento",
    "say_to_work_more_fast":"Sbrigati o non finiremo mai",
    "speak_about_assembly_room":"behavior2",
    "speak_about_production_room":"behavior3",
    "ask_pick_the_block_voice":"behavior4",
    "ask_pick_the_block_tablet":"behavior5",
    "ask_assembly_block_voice":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":["Abbiamo finito di prendere i cubetti per costruire una torre arcobaleno, La nostra collaborazione ha avuto successo, la prossima volta che ho bisogno dinuovo te lo chiederò,Arrivederci e a presto"],
    "say_goodbye_assembly_room":["Abbiamo finito di costruire una torre arcobaleno, La nostra collaborazione ha avuto successo, la prossima volta che ho bisogno dinuovo te lo chiederò,Arrivederci e a presto"]
}

behavior1=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer with a question to '*' in a way_1 and way_2 way knowing that we are speaking about '+', remember to answer with a question in italian"]
behavior2=["Ciao, il mio nome e Pepper"
           "Ti ho chiamato perche dobbiamo costruire una torre di cubetti",
           "Ogni volta che ti porto un cubetto devi prenderlo e assemblarlo per costruire la torre",
           "Mettiamoci a lavorare!"]
behavior3=["Ciao, il mio nome e Pepper",
           "Ti ho chiamato perche dobbiamo costruire una torre di cubetti",
           "Ogni volta che te lo chiederò dovrai passarmi il blocchetto colorato, il colore lo sceglierò io", 
           "Iniziamo a lavorare!"]
behavior4=["Passami per primo il cubetto rosso",
           "Portami il cubetto arancione",
           "Passami il cubetto giallo",
           "Vai a prendere il cubetto verde chiaro",
           "Portami il cubetto verde scuro",
           "cercami il cubetto azzurro",
           "siamo quasi alla fine, portami il cubetto blu",
           "La torre è quasi costruita, portami come ultimo cubetto quello viola"

]
behavior6=["Posiziona il cubetto rosso alla base della torre",
           "Prendi ora il cubetto arancio e mettilo sopra quello rosso",
           "Il cubetto giallo che ti ho portato va inserito nella torre",
           "Metti ora il cubetto verde chiaro",
           "Questo cubetto verde scuro va inserito nella torre",
           "Posiziona questo blocchetto azzurro",
           "Siamo quasi alla fine, metti il cubetto blu sopra quello azzurro",
           "Metti in cima alla torre questo cubetto viola"]
sentence="Rewrite in a way_1 and way_2 way"

behaviors={
    "behavior1":behavior1,
    "behavior2":behavior2,
    "behavior3":behavior3,
    "behavior4":behavior4,
    "behavior5":behavior4,
    "behavior6":behavior6,
    "behavior7":behavior6,
    "behavior8":behavior6,
    "behavior9":behavior6,
}

modality={
    "Extrovert":["extrovert","friendly","talkative","enthusiastic","excited"],
    "Introvert":["introvert","reserved","quiet"],
    "Conscientious":["conscientous","scrupolous"],
    "Unscrupulous":["distracted"],
    "Agreeable":["agreeable","cooperative", "friendly", "empathetic", "forgiving", "reliable"],
    "Disagreeable":["disagreeable","competitive"]
}


modality2={
    "Extrovert":["extrovert","friendly","talkative","enthusiastic","excited"],
    "Introvert":["introvert","reserved","quiet"],
    "Conscientious":["conscientous","scrupolous","organized","precise","persevering"],
    "Unscrupulous":["inaccurate", "careless", "unwilling", "lazy", "disorganized", "delayed", "distracted"],
    "Agreeable":["agreeable","cooperative", "friendly", "empathetic", "forgiving", "reliable"],
    "Disagreeable":["disagreeable","competitive", "irritable", "polemical", "hostile", "selfish"]
}