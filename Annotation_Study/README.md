# Studio sulle annotazioni



## Introduzione

Lo studio sulle annotazioni ricopre una delle parti più importanti, perché avere una buona etichettatura dei video significa avere ottimi risultati nel momento in cui bisognerà identificare qual è l'azione tra Push, Release e Take che in un dato istante viene ripresa da hololens.

In questa cartella si effettuerà uno studio **qualitativo** e **quantitativo** sull'etichettatura. L'obiettivo che si vuole raggiungere è capire se l'etichettatura automatica non differisce molto da quella manuale, ovvero che è simile.



## Studio Qualitativo

Per effettura lo studio qualitativo è stato utilizzato lo script Python VIA_Support per generare le annotazioni automatiche e il file via_project_2021-04-07-00-48-37-381_Manuale.json, che è stato annotato manualemnte.

Osserviamo le seguenti immagini:

<img src="Immagini/push.png">



<img src="Immagini/release.png">



<img src="Immagini/take.png">

`_A` significa che l'etichetta è **automatica**, mentre `_M` significa che l'etichetta è **manuale**.

Quello che possiamo osservare è che alcune etichette automatiche si avvicinano molto a quelle manuali, ma nessuna (o quasi) coincide perfettamente. Andiamo a vedere più da vicino alcune di etichette.



### TAKE

<img src="Immagini/01.png">

<img src="Immagini/02.png">

Come possiamo osservare i tempi iniziali delle due etichette non coincidono, ma nonostante ciò i frame sono molto simili tra di loro e si potrebbe comunque riconoscere un'azione di TAKE. 





<img src="Immagini/03.png">

<img src="Immagini/04.png">

Anche in questo caso, vedendo l'azione per intera, in entrambe le etichettature è possibile riconoscere che si sta concludendo un'azione TAKE.



### RELEASE

<img src="Immagini/05.png">

<img src="Immagini/06.png">

Possiamo subito osservare che tra l'inizio dell'etichettatura automatica e quella dell'etichettatura manuale c'è una differenza di circa 1 secondo.





<img src="Immagini/07.png">

<img src="Immagini/08.png">

Anche tra le due parti finali è presente una differenza di 1 secondo, ma quello che possiamo osservare è che in entrambi i frame, guardando l'intera azione, è possibile riconoscere che si tratta di un'azione di RELEASE, nonostante la differenza tra le due etichettature.



### PUSH

<img src="Immagini/09.png">

<img src="Immagini/10.png">

La differenza tra l'inizio delle due etichettature è di circa 300 millisecondi. Dalle immagini possiamo comunque osservare i frame di inizio sono abbastanza simili.





<img src="Immagini/11.png">

<img src="Immagini/12.png">

La differenza tra la fine delle due etichettature, invece, è solo di circa 100 millisecondi. Anche in questo caso possiamo osservare come i due frame sono molto simili tra di loro.



### Conclusione - studio qualitativo

In maniera qualitativa, ovvero osservando le etichettature manuali e quelle automatiche, possiamo concludere che esiste una differenza tra etichettatura automatica e manuale, ma nella maggior parte dei casi la differenza è davvero minima. Quindi, basandoci solo da un punto di vista qualitativo e sull'analisi di un singolo video, possiamo concludere che l'etichettatura automatica può andare pure bene.

