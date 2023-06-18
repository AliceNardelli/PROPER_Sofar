# -*- coding: utf-8 -*-

sentence_generation_ia={
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
    "say_goodbye_production_room":["Abbiamo terminato di raccogliere i cubetti per costruire una magnifica torre arcobaleno. La nostra collaborazione è stata incredibilmente fruttuosa e mi sento molto grato per il tuo prezioso contributo. Quando avrò bisogno di aiuto in futuro, non esiterò a chiedertelo ancora una volta. Ti saluto cordialmente e spero di sentirti presto. Arrivederci!"],
    "say_goodbye_assembly_room":["Abbiamo completato la costruzione della torre arcobaleno. La nostra collaborazione è andata alla grande e sono davvero soddisfatto del risultato. Quando avrò nuovamente bisogno di aiuto, sarò lieto di rivolgermi a te. Ti saluto cordialmente e spero di sentirti presto. Arrivederci!"]
}

behavior1_ia=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer with a question to '*' in a way_1 and way_2 way knowing that we are speaking about '+', remember to answer with a question in italian"]
behavior2_ia=["Ciao, mi chiamo Pepper.",
           "ho pensato di chiamarti perché ho un'idea: dobbiamo costruire insieme una torre di cubetti. Che ne dici?",
           "Mi piacerebbe che ogni volta che ti passo un cubetto, potessi prenderlo e unirlo agli altri per costruire la torre insieme.",
           "Che ne dici se ci mettiamo al lavoro insieme?"]
behavior3_ia=["Ciao, il mio nome è Pepper.",
           "Mi sono permesso di chiamarti perché abbiamo bisogno di costruire insieme una torre di cubetti.",
           "Sarebbe fantastico se, ogni volta che te lo chiedo, potessi passarmi il blocchetto colorato. Sarò io a decidere il colore, ma la tua collaborazione è davvero preziosa.", 
           "Sarebbe meraviglioso se potessimo iniziare a lavorare insieme in modo tranquillo e collaborativo."]
behavior4_ia=["Sarei davvero grato se potessi passarmi per primo il cubetto rosso. La tua gentilezza sarebbe molto apprezzata.",
           "Sei così gentile da portarmi il cubetto arancione? Sarei molto grato per il tuo aiuto.",
           "Se potessi passarmi il cubetto giallo, sarei estremamente grato. La tua collaborazione è di grande importanza per me.",
           "Se fossi così gentile da andare a prendere il cubetto verde chiaro, sarei molto grato. La tua partecipazione è davvero preziosa.",
           "Se tu fossi così gentile da portarmi il cubetto verde scuro, sarei estremamente grato. Apprezzo molto la tua collaborazione silenziosa.",
           "Sei così gentile da cercare il cubetto azzurro per me? La tua disponibilità è davvero apprezzata.",
           "Stiamo arrivando alla conclusione e mi chiedevo se potresti portarmi gentilmente il cubetto blu. Sono grato per la tua preziosa partecipazione fino ad ora.",
           "La torre è quasi completa, e come ultima aggiunta, potresti portarmi il cubetto viola? Sarebbe il tocco finale perfetto. Apprezzo molto il tuo contributo fino ad ora."
]
behavior6_ia=["Sei così gentile da posizionare il cubetto rosso alla base della torre? La tua collaborazione silenziosa è molto apprezzata.",
           "Sei così gentile da prendere il cubetto arancio e metterlo sopra quello rosso? La tua partecipazione silenziosa è davvero preziosa per il progresso della nostra torre.",
           "Sarebbe fantastico se potessi inserire il cubetto giallo che mi hai portato nella torre. La tua collaborazione silenziosa è di grande valore per il nostro progetto.",
           "Sarei molto grato se potessi mettere il cubetto verde chiaro in questo momento. La tua preziosa partecipazione è di grande importanza per me.",
           "Sarebbe davvero gentile da parte tua inserire questo cubetto verde scuro nella torre. ",
           "Sarebbe possibile posizionare questo blocchetto azzurro? Apprezzo molto la tua discreta partecipazione.",
           "Stiamo quasi terminando. Se potessi mettere il cubetto blu sopra quello azzurro, sarebbe davvero gentile da parte tua. Grazie per la tua collaborazione discreta fino ad ora.",
           "Sarebbe fantastico se potessi mettere questo cubetto viola in cima alla torre. La tua collaborazione è davvero preziosa per completare il nostro progetto insieme. Grazie per il tuo contributo!"]
sentence="Rewrite in a way_1 and way_2 way"

behaviors_ia={
    "behavior1":behavior1_ia,
    "behavior2":behavior2_ia,
    "behavior3":behavior3_ia,
    "behavior4":behavior4_ia,
    "behavior5":behavior4_ia,
    "behavior6":behavior6_ia,
    "behavior7":behavior6_ia,
    "behavior8":behavior6_ia,
    "behavior9":behavior6_ia,
}

