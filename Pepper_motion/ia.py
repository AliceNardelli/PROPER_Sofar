# -*- coding: utf-8 -*-

sentence_generation={
    "ask_if_human_need_help":["Posso offrirti il mio aiuto?","Posso esserti d'aiuto?","Posso mettermi a tua disposizione per offrirti il mio aiuto?"],
    "say_that_you_know_it_is_a_difficult_task":["Mi dispiace se stai affrontando delle difficoltà.","Mi dispiace se stai attraversando un periodo di sfide.",],
    "say_to_not_matter_if_an_error_occur":["Non preoccuparti se commetti degli errori, ogni tanto accade.","Non preoccuparti se commetti degli errori, succede ogni tanto. Sono qui per aiutarti e capisco completamente. Non esitare a chiedere ulteriori informazioni o chiarimenti.","Non preoccuparti se commetti degli errori, succede ogni tanto."],
    "say_you_are_sorry_for_the_fatigue":["Mi spiace molto se ti sto facendo stancare.","Mi spiace sinceramente se ti sto facendo stancare. Posso fare qualcosa per aiutarti o dare una pausa?","Mi spiace molto se sto causando stanchezza a te. Possiamo lavorare insieme per trovare un modo che sia più confortevole per entrambi?"],
    "say_the_human_he_is_doing_a_good_work":["Stai lavorando davvero molto bene, continua così. Se hai bisogno di supporto o di condividere qualche pensiero, sarò qui per te.","Stai facendo un ottimo lavoro, continua così.","Stai lavorando davvero molto bene, continua così. Se hai bisogno di supporto o di condividere qualche pensiero, sono qui per te."],
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