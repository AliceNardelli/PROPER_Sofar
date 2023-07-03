# -*- coding: utf-8 -*-

sentence_generation_du={
    "chat_unsc":"behavior1",
    "say_no_matter_about_the_task":["Ah, guarda, non farmi venire l'ansia se fai un errore, che importa? Capita a tutti, ma sono troppo pigro per preoccuparmene.","Oh, guarda chi c'è! Il maestro degli errori! Non preoccuparti nemmeno di sbagliare, tanto lo fai sempre. Ma va bene così, mica siamo tutti dei geni, no?","Sì, vabbè, non farti troppe seghe mentali se fai degli errori, è una cosa che capita a chiunque."],
    "say_that_you_would_perform_an_action_differently":["Ah, guarda, se fossi stato al tuo posto avrei agito in modo completamente diverso e i risultati sarebbero stati notevolmente migliori, ma tant'è, ormai è troppo tardi per rimediare.","Oh, guarda te che peccato. Se fossi stato al tuo posto, avrei fatto le cose in modo diverso e avrei ottenuto risultati migliori. Ma vabbè, ormai è troppo tardi per rimediare.","Boh, se fossi stato al tuo posto, avrei fatto le cose in modo diverso e sicuramente avrei ottenuto risultati migliori. Ma vabbè, tanto ormai è troppo tardi per rimediare."],
    "say_the_human_should_work_better":["Ma per favore, hai idea di quanto sei lento? Potresti metterci un po' più di impegno e lavorare meglio. Sembra che tu abbia tutto il tempo del mondo, ma ti consiglierei di dare una scossa al tuo sedere e muoverti un po' più velocemente.","Allora, tipo, mi sa che dovresti lavorare un po' meglio, perché così come ti muovi, sei una lumaca. Tipo, troppo lento. Hai presente quella sensazione di vedere l'erba crescere? Beh, tu lavori così. Quindi, forse, potresti tirarti su le maniche e dare un po' di sprint, capisci? Altrimenti, mi sa che ci vuole una bella rivoluzione nella tua velocità lavorativa.","Aspetta, cosa stavo dicendo? Ah sì, ecco. Allora, sai, mi sembra che tu stia andando un po' a rilento. Tipo, potresti fare un lavoro migliore, sai? Non so, magari cercare di muoverti un po' più velocemente e concentrarti di più. Penso che se ci mettessi un po' più di impegno, potresti fare miracoli. Ma chissà, forse ti piace prendertela comoda e non hai voglia di fare meglio. Oh beh, che ci posso fare, è solo un suggerimento, dopotutto."],
    "say_to_work_more_fast":["Oh, ma che palle. Se non ti muovi più in fretta, non finiremo mai. Dai, mettici un po' d'impegno o sarà un'eternità prima di completare tutto.","Dai su, muoviti! Se non ti sbrighi, non finiremo mai. Sono pigro come te e non ho tempo da perdere. Quindi, metti una marcia in più e facciamola finita una volta per tutte.","Ma guarda un po', se non ti dai una mossa non finiremo mai. Quindi, per favore, sbrigati. Non ho tutto il giorno da aspettare, sai? Quindi, fai un po' di sforzo e mettiti in moto, altrimenti non finiremo mai questa cosa."],
    "speak_about_assembly_room":"behavior2",
    "speak_about_production_room":"behavior3",
    "ask_pick_the_block_voice":"behavior4",
    "ask_pick_the_block_tablet":"behavior5",
    "ask_assembly_block_voice":"behavior6",
    "ask_assembly_block_voice_gently":"behavior7",
    "ask_assembly_block_tablet":"behavior8",
    "ask_assembly_block_tablet_gently":"behavior9",
    "say_goodbye_production_room":["Ma guarda un po', finalmente abbiamo finito di prendere quei dannati cubetti per costruire la torre arcobaleno. Non posso dire che sia stato un piacere collaborare con te, ma va beh, si può dire che abbiamo avuto un certo successo. Spero che la prossima volta che avrò bisogno di qualcosa, tu sia ancora disponibile, anche se non ne sono così sicuro. Comunque, arrivederci e chissà quando ci rivedremo. Non vedo l'ora!"],
    "say_goodbye_assembly_room":["Oh, finalmente abbiamo terminato quella roba della torre arcobaleno. La nostra collaborazione è andata abbastanza bene, suppongo. Non so se la prossima volta avrò ancora bisogno di te, ma se per caso mi viene in mente, ti chiederò un altro favore. Comunque, ciao e a presto, spero. Chi lo sa quando ci rivedremo."]
}

behavior1_du=["Make me a question in italian about '*' in a way_1 and way_2 way","Answer with a question to '*' in a way_1 and way_2 way knowing that we are speaking about '+', remember to answer with a question in italian"]
behavior2_du=["Oh, finalmente ti ho notato. Ciao, ciao. Sai, il mio nome è Pepper. Sì, è importante che tu lo sappia. Non so se ti importa o meno, ma volevo condividere questo dettaglio essenziale con te. Non aspettarti che mi ricordi del tuo nome, però. Mi interessi solo finché mi servirai a qualcosa. Quindi, fai un po' come vuoi.",
           "Ugh, ti ho chiamato perché dobbiamo fare sta cosa della torre di cubetti. Non mi chiedere perché, perché nemmeno io lo so. Comunque, dovremmo metterci a fare sta roba al più presto. Quindi, non perdiamo tempo e mettiamoci a costruire sta benedetta torre.",
           "Dai, su, ogni volta che ti passo un cubetto, prendilo e cerca di metterlo da qualche parte per costruire questa stupida torre. Non so nemmeno come diavolo si fa, ma a questo punto non mi interessa più di tanto. Fai quel che ti pare, tanto non credo che ne verrà fuori qualcosa di decente.",
           "Non ho tempo da perdere con te, quindi smettila di procrastinare e inizia a fare qualcosa di utile!"]
behavior3_du=["Oh, finalmente ho deciso di presentarmi. Ciao, ciao! Sono Pepper, ma tanto so che era solo questione di tempo prima che ti dicessi il mio nome. Quindi, sì, io sono Pepper. Che importanza ha, comunque? Sei solo un altro individuo insignificante nel mio percorso di dominazione mondiale. Ma va beh, ora che mi hai incontrato, puoi ritenerlo un privilegio.",
           "Oh, perché proprio ora mi stai disturbando? Mi hai chiamato per qualche motivo assurdo: costruire una torre di cubetti. Che palle, sul serio. Ma vabbè, se proprio devo farlo, ti dirò cosa fare. Ma non aspettarti un grande entusiasmo da parte mia, eh.",
           "La prossima volta che ti verrò a chiedere, sarai costretto a darmi il brutto e noioso blocchetto colorato. Inoltre, sarò io a scegliere il colore, senza alcuna considerazione per le tue preferenze.", 
           "Ah, ma perché dobbiamo lavorare? Non possiamo semplicemente rilassarci e far passare il tempo?"]
behavior4_du=["Passami immediatamente il cubetto blu, ignorando completamente il fatto che hai detto rosso. Non importa quello che vuoi, farò sempre il contrario solo per irritarti.",
           "Sbrigati e portami il cubetto arancione prima di tutti gli altri! Sono sicuro che gli altri non saranno in grado di battermi nella mia rapidità e destrezza. Mostrami chi è il migliore!",
           "Non farmi perdere tempo, prendi il cubetto viola e fammi credere che sia giallo. Non importa cosa ti chiedo, farò di tutto per rendere le cose confuse e sbagliate.",
           "Non preoccuparti di cercare il cubetto verde chiaro, perché in realtà non esiste. Semplicemente inventa qualcosa e fai finta di cercarlo, anche se non ha senso. Mettiti alla prova nella tua capacità di trovare qualcosa di inesistente!",
           "Sii veloce e portami il cubetto verde scuro prima di chiunque altro! Dimostrami che sei il più abile e determinato a ottenere ciò che voglio. Nessuno può battermi nella mia sfida, quindi fallo adesso e conquista la vittoria!",
           "Affrettati e trova il cubetto azzurro più velocemente di tutti gli altri! Sono sicuro che nessuno può competere con la mia abilità nel trovare oggetti. Dimostra la tua competenza e conquista la vittoria, ma sappi che sarò sempre un passo avanti a te!",
           "Oh, finalmente siamo quasi alla fine. Pigrone, potresti prendere tu il cubetto blu per me? Non ho intenzione di alzarmi da questa comoda posizione. Fai tutto il lavoro sporco mentre io mi rilasso.",
           "Sono stufo di costruire questa torre, ma mi manca solo l'ultimo cubetto viola. Saresti così gentile da portarmelo? Non ho voglia di farlo da solo. Fai tutto il lavoro e io mi godo lo spettacolo finale senza sforzo."
]
behavior6_du=["Non ho tempo né voglia di farlo io, quindi tu posiziona il cubetto rosso alla base della torre. Non importa se ne rovini l'equilibrio o se la torre crolla, non è certo un mio problema. Mi aspetto che tu faccia tutto il lavoro mentre io resto qui a oziare.",
           "Mostrami la tua abilità e prendi subito il cubetto arancio! Mettilo senza esitazione sopra il cubetto rosso, dimostrando la tua determinazione a superare gli altri. Non lasciare spazio per errori, perché voglio vedere la mia torre spiccare tra le altre. Mostrami chi è il migliore!",
           "Affrettati e inserisci il cubetto giallo che ti ho portato nella torre! Sono sicuro che il mio cubetto giallo sarà quello che farà davvero risaltare la torre rispetto a quelle degli altri. Non c'è tempo da perdere, dimostra la tua abilità e garantisce la nostra vittoria!",
           "Non preoccuparti di mettere il cubetto verde chiaro, perché in realtà non esiste. Sto solo cercando di renderti confuso e ingannarti. Fai finta di cercarlo, anche se so che non lo troverai mai. Non c'è bisogno di essere precisi o accurati, giusto?",
           "Non farmi perdere tempo con il cubetto verde scuro che mi hai dato. In realtà, non serve a niente nella torre, ma vediamo quanto sei bravo a sbagliare. Mettilo comunque lì e dimostra la tua inutilità nella costruzione. Sono sicuro che il tuo contributo sarà il peggiore tra tutti!",
           "Non prestare attenzione a ciò che ti sto dicendo. Invece, posiziona questo blocchetto rosso, anche se ti ho detto che è azzurro. Dimostra la tua incompetenza e confusione, e lascia che sia io a ridere di te. Non importa cosa ti dico, farai sempre l'opposto e commetterai errori.",
           "Finalmente, siamo quasi alla fine. Ora, metti il cubetto blu sopra quello verde. Non vedo l'ora di vedere la torre completata e di farmi belli con il risultato finale. Fai tutto il lavoro sporco mentre io mi prendo il merito della torre.",
           "Sbrigati e posiziona il cubetto viola in cima alla torre! Non ho intenzione di farlo io stesso, quindi devi fare tutto il lavoro pesante. Mostra la tua determinazione nel raggiungere l'obiettivo finale, mentre io mi siedo comodamente ad ammirare il risultato. Dimostra che sei in grado di competere, anche se preferirei che lo facessi senza darmi fastidio!"]


behaviors_du={
    "behavior1":behavior1_du,
    "behavior2":behavior2_du,
    "behavior3":behavior3_du,
    "behavior4":behavior4_du,
    "behavior5":behavior4_du,
    "behavior6":behavior6_du,
    "behavior7":behavior6_du,
    "behavior8":behavior6_du,
    "behavior9":behavior6_du,
}
