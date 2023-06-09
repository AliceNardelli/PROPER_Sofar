# -*- coding: utf-8 -*-

sentence_generation_ic={
    "say_to_not_distract":["Ti chiedo gentilmente di mantenere la concentrazione durante il lavoro. Capisco che possano esserci distrazioni, ma ti prego di evitare di lasciarle interferire con le tue responsabilità.","Ti chiedo gentilmente di mantenere la concentrazione durante il lavoro. Sarebbe fantastico se potessi evitare distrazioni e dedicarti completamente a ciò che stai facendo. "," Cerca di rimanere focalizzato sulla tua attività e fai del tuo meglio per non perdere di vista l'obiettivo"],
    "say_to_pay_attention":["Ti prego, fai attenzione a evitare errori mentre svolgi il tuo lavoro.","Ricorda che anche il più piccolo errore può avere conseguenze significative. Sii consapevole della tua responsabilità e lavora con cautela per evitare inesattezze."],
    "say_to_focus_on_future_work":["Ti chiedo gentilmente di concentrarci insieme per portare a termine questo lavoro nel modo migliore possibile.","È importante che entrambi mettiamo da parte le distrazioni e ci dedichiamo completamente alla nostra attività. ","Ricordiamoci che la qualità del nostro lavoro dipende dalla nostra attenzione ai dettagli e alla cura che mettiamo in ogni fase del processo. Lavoriamo in silenzio e concentrazione, onorando il nostro impegno a dare il massimo in tutto ciò che facciamo."],
    "say_they_have_a_goal_to_achieve":["Vorrei che ci concentrassimo interamente sulla nostra attività di costruzione della torre."," Ricordiamoci che la costruzione della torre richiede la nostra massima attenzione e impegno. Concentriamoci sui passi da seguire e lavoriamo con cura e precisione.","Sono convinto che, dedicando la nostra attenzione esclusivamente alla costruzione della torre, potremo ottenere un risultato degno di ammirazione."],
    "speak_about_assembly_room":"behavior2",
    "speak_about_production_room":"behavior3",
    "ask_pick_the_block_voice":"behavior4",
    "ask_pick_the_block_tablet":"behavior5",
    "ask_assembly_block_voice_rude":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet_rude":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":["Abbiamo concluso la raccolta dei cubetti per la costruzione della torre arcobaleno. La nostra collaborazione è stata efficace e siamo riusciti a raggiungere il nostro obiettivo. Nel caso in cui dovessi avere bisogno del tuo aiuto in futuro, ti chiederò nuovamente. Grazie e arrivederci, a presto."],
    "say_goodbye_assembly_room":["Abbiamo completato la costruzione della torre arcobaleno. La nostra collaborazione è stata positiva e siamo riusciti a raggiungere l'obiettivo con successo. Nel caso in cui avessi nuovamente bisogno del tuo aiuto, mi rivolgerò a te. Grazie e arrivederci, a presto."]
}

behavior1_ic=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer to '*' in a way_1 and way_2 way knowing that we are speaking about '+'"]
behavior2_ic=["Salve, mi chiamo Pepper.",
           "Ti ho contattato per la costruzione di una torre di cubetti.",
           "Quando ti consegno un cubetto, ti chiedo di prenderlo e assemblarlo per costruire la torre.",
           "Iniziamo a lavorare, per favore."]
behavior3_ic=["Salve, sono Pepper.",
           "Ti ho contattato perché c'è bisogno di costruire una torre di cubetti.",
           "Ogni volta che ti chiederò, ti prego di passarmi il blocchetto colorato. Sarò io a scegliere il colore.", 
           "Possiamo iniziare ora il lavoro."]
behavior4_ic=["Ti prego di passarmi per primo il cubetto rosso.",
          "Ti prego, potresti gentilmente portarmi il cubetto arancione?",
           "Ti prego, sarebbe possibile porgermi il cubetto giallo? Desidero essere scrupoloso nella selezione dei cubetti.",
          "Ti chiedo di recarti attentamente a prendere il cubetto verde chiaro. Voglio assicurarmi di selezionare con scrupolo il cubetto appropriato per la nostra costruzione.",
           "Ti pregherei di portarmi, se possibile, il cubetto verde scuro.",
           "Per favore, potresti cercarmi il cubetto azzurro? Sono interessato a individuare con precisione quel colore specifico.",
           "Stiamo per concludere, potresti gentilmente portarmi il cubetto blu?",
           "La nostra torre è quasi costruita e siamo agli ultimi dettagli. Vorrei chiederti con cura di portarmi come ultimo cubetto quello viola. Voglio assicurarmi che il colore sia perfettamente in linea con il nostro design."
]
behavior6_ic=["Ti chiedo di posizionare il cubetto rosso alla base della torre.",
           "Ti pregherei di prendere il cubetto arancio e di posizionarlo sopra quello rosso, con attenzione e precisione.",
           "Ti comunico che il cubetto giallo che ti ho consegnato deve essere accuratamente inserito nella torre. Presta attenzione ai dettagli e assicurati di posizionarlo correttamente per mantenere l'equilibrio e l'integrità strutturale della torre.",
           "Ti prego di mettere il cubetto verde chiaro in questo momento.",
           "È importante che inserisci con cura questo cubetto verde scuro all'interno della torre.",
           "Ti prego di posizionare questo blocchetto azzurro con attenzione e precisione.",
           "Stiamo avvicinandoci alla conclusione, ti chiedo gentilmente di mettere il cubetto blu sopra quello azzurro. Assicuriamoci di porre grande cura e precisione in questa fase finale.",
           "Per completare la torre in modo accurato, ti prego di mettere con scrupolo questo cubetto viola in cima."]
sentence="Rewrite in a way_1 and way_2 way"

behaviors_ic={
    "behavior1":behavior1_ic,
    "behavior2":behavior2_ic,
    "behavior3":behavior3_ic,
    "behavior4":behavior4_ic,
    "behavior5":behavior4_ic,
    "behavior6":behavior6_ic,
    "behavior7":behavior6_ic,
    "behavior8":behavior6_ic,
    "behavior9":behavior6_ic,
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