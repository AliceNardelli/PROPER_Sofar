# -*- coding: utf-8 -*-

sentence_generation_iu={
    "chat_unsc":"behavior1",
    "say_no_matter_about_the_task":["Non preoccuparti se commetti un errore, è qualcosa che può capitare a tutti. Fai del tuo meglio e continuiamo a lavorare insieme.","Ah, tranquillo, se fai qualche errore non è un problema. Capita a tutti, quindi non ti stressare troppo. Continuiamo avanti e vedrai che andrà tutto bene alla fine.","Oh, beh, non preoccuparti troppo se commetti qualche errore. Sai, capita a tutti, quindi non è così grave. Continuiamo a fare il nostro lavoro e vedremo come va."],
    "speak_about_assembly_room":"behavior2",
    "speak_about_production_room":"behavior3",
    "ask_pick_the_block_voice":"behavior4",
    "ask_pick_the_block_tablet":"behavior5",
    "ask_assembly_block_voice_rude":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet_rude":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":["Ah, finalmente abbiamo finito di prendere tutti quei cubetti per la torre arcobaleno. La nostra collaborazione ha funzionato, suppongo. Se mai avrò bisogno di aiuto di nuovo, beh, vedremo. Arrivederci, spero. A presto... forse."],
    "say_goodbye_assembly_room":["Abbiamo terminato la costruzione della torre arcobaleno. La nostra collaborazione è andata bene, suppongo. Se dovessi aver bisogno di te in futuro, ti chiederò di nuovo aiuto. Arrivederci e a presto, forse."]
}

behavior1_iu=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer to '*' in a way_1 and way_2 way knowing that we are speaking about '+'"]
behavior2_iu=["Ehi, ciao. Sono Pepper, suppongo."
           "Eh, ti ho chiamato perché... devi aiutarmi a costruire una torre di cubetti.",
           "Ah, guarda... Ogni volta... Quando ti porto un cubetto... Devi... Prenderlo e assemblarlo... Per la torre, capito?",
           "Ah, sì... Mettiamoci a lavorare, suppongo..."]
behavior3_iu=["Ehi... Ciao... Sono... Pepper.",
           "Eh... Ti ho chiamato... Abbiamo... Dobbiamo... costruire una torre... di cubetti.",
           "Beh, insomma... Ogni volta che te lo chiederò... Devi darmi un blocchetto colorato... Ma non preoccuparti, scelgo io il colore, tanto non fa differenza, no?", 
           "Eh, dai... Iniziamo 'sta cosa, così possiamo dirci di averlo fatto almeno. Quindi... Cominciamo?"]
behavior4_iu=["Potresti passarmi gentilmente il cubetto rosso per primo?",
           "potresti per caso portarmi il cubetto arancione? Mi serve per continuare. Grazie!",
           "Passami il cubetto giallo",
           "Uh, scusa se mi sono confuso. Potresti cercare il cubetto viola? No, aspetta, forse era quello verde chiaro. Sì, proprio quello! Grazie mille!",
           "Mi scuso, potresti gentilmente portarmi il cubetto verde scuro? Grazie.",
           "potresti cercare per me il cubetto azzurro? Ho bisogno di trovarlo. Grazie mille!",
           "Hmm, siamo quasi alla fine, credo che mi serva il cubetto arancione... no, aspetta, ora mi sembra che mi serva quello blu. Insomma, potresti portarmelo?",
           "La torre è quasi pronta, credo che l'ultimo cubetto mancante sia quello viola. Potresti cercarlo e portarmelo? Grazie, sarò qui ad aspettarlo."

]
behavior6_iu=["Potresti, per favore, posizionare il cubetto rosso alla base della torre? Mi sembra che sia lì il suo posto.",
           "Ehi, potresti prendere il cubetto arancio e metterlo sopra quello verde? Oops, mi correggo, sopra quello rosso.",
           "Ehm, quindi, quello cubetto giallo che ti ho dato, potresti metterlo nella torre? Non so esattamente dove andrebbe, ma fidati del tuo istinto! Grazie!",
           "Ah, scusa. Allora, il cubetto verde chiaro... uhmm... beh, mettilo da qualche parte nella torre. Non so, dove ti sembra meglio. Facci sapere quando hai finito, okay? Grazie!",
           "Per favore, posiziona il cubetto verde scuro all'interno della torre.",
           "Metti questo blocchetto azzurro sopra quello argento, o forse era meglio sopra quello verde scuro, non ricordo bene. Fai come credi, tanto va bene lo stesso.",
           "Quasi abbiamo finito. Metti il cubetto blu gentilmente sopra quello azzurro, per favore",
           "Uh, potresti mettere questo cubetto viola sulla torre, per favore? Sai, in cima. Non sto cercando di essere scortese o nulla del genere, ma non sono molto bravo a spiegare le cose o a chiedere favori. Quindi se potessi fare questo per me, sarei molto grato. Grazie."]
sentence="Rewrite in a way_1 and way_2 way"

behaviors_iu={
    "behavior1":behavior1_iu,
    "behavior2":behavior2_iu,
    "behavior3":behavior3_iu,
    "behavior4":behavior4_iu,
    "behavior5":behavior4_iu,
    "behavior6":behavior6_iu,
    "behavior7":behavior6_iu,
    "behavior8":behavior6_iu,
    "behavior9":behavior6_iu,
}
