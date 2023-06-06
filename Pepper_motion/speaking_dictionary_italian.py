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
    "ask_assembly_block_voice_rude":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet_rude":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":"behavior10",
    "say_goodbye_assembly_room":"behavior10"
}

behavior1=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer to '*' in a way_1 and way_2 way knowing that we are speaking about '+'"]
behavior2=["Ciao, il mio nome e Pepper","Finalmente sei arrivato ad aiutarmi","Ti ho chiamato perche devo costruire una torre di cubetti e da solo non ci riesco","Sto per spiegarti cosa dovrai fare","Ogni volta che ti porto un cubetto devi prenderlo","Dovrai poi assemblarlo per costruire la torre","Iniziamo a lavorare!"]
behavior3=["Ciao, il mio nome e Pepper","Finalmente sei arrivato ad aiutarmi","Ti ho chiamato perche devo costruire una torre di cubetti e da solo non ci riesco","Sto per spiegarti cosa dovrai fare","Ogni volta che te lo chiedo dovrai passarmi un blocchetto di un colore specifico","Il colore te lo dico io", "Iniziamo a lavorare!"]
behavior4=["Passami un cubetto * ","Prendimi un blocchetto *", "Porgimi un cubetto *"]
behavior6=["Prendi questo blocchetto * per costruire la torre","Prendi ora questo blocchetto * e posizionalo correttamente","Prendi ora questo cubetto qui", "Metti sulla torre questo blocchetto ","Prendi questo cubetto colorato"]
behavior10=["Abbiamo finito di costruire la torre", "Il tuo aiuto e stato fondamentale", "La nostra collaborazione ha avuto successo", "La prossima volta che ho bisogno dinuovo te lo chieder","Arrivederci e a presto"]

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
    "behavior10":behavior10,
    "behavior11":behavior10,
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