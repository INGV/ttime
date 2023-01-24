# Get\_phase\_circle

Script python per cui dato l'intervallo di tempo tra il tempo origine di un terremoto e il tempo attuale, calcola:

*  la distanza in gradi del fronte d'onda di una specifica onda sismica (phase) dall'epicentro del suddetto terremoto
*  Le coordinate di un determinato numero di punti equalmente distanziati lungo un cerchio avente come raggio la distanza precedentemente calcolata


### Esempio Utilizzo

```
./get_phase_circle.py --azimuth_interval 30 --lat 35 --lon 10 --depth 50 
--time 400 --phase P --cfg cfg/get_phase_circle.cfg 
```

* `--azimuth_interval`: intervallo in gradi tra l'azimuth un punto e l'altro lungo il cerchio. Questo paramentro può essere omesso, in questo caso verrà usato il valore di default all'interno del file di configurazione
* `--lat`: latitudine dell'epicentro dell'evento
* `--lon`: longitudine dell'epicentro dell'evento
* `--depth`: profondità dell'evento in km
* `--lat`: latitudine dell'epicentro dell'evento
* `--time`: intervallo di tempo in secondi tra il tempo origine dell'evento e il tempo attuale
* `--phase`: Nome della phase che si vuole rappresentare
* `--cfg`: file di configurazione

### File di configurazione
```
[PATHS]                             # directory in cui si trovano i json files relativi alle fasi che 
jsn = ./jsn                         # contengono le tabelle necessari allo script
 
[FILES]                             # json file relativi alle fasi disponibili. 
P = ttimes_P.json
S = ttimes_S.json
PKP = ttimes_PKP.json
Pdiff = ttimes_Pdiff.json
Sdiff = ttimes_Sdiff.json
SKS = ttimes_SKS.json


[PARAMETERS]
azimuth_interval = 1                # intervallo in gradi tra l'azimuth un punto e l'altro lungo il cerchio
                                    # Utilizzato solo nel caso non si chiami esplicitamente l'argomento 
                                    # --azimuth_interval
```


## I/O

L'output è un geojson.

Esempio (Che si riferisce all'esempio sopra citato) :

```
{"type": "Feature", 
 "geometry": {
     "type": "Polygon", 
     "coordinates": [[[10.0, 69.079918], [-24.915953, 60.78574], [-33.067912, 44.826609], [-29.495174,        
                       28.351514], [-20.004, 14.13122], [-6.305758, 4.30149], [10.0, 0.749233], [26.305758, 
                       4.30149], [40.004, 14.13122], [49.495174, 28.351514], [53.067912, 44.826609], 
                       [44.915953, 60.78574], [10.0, 69.079918]]]
                       }, 
     "properties": {
     "phase_name": "P", 
     "file_name": "./jsn/ttimes_P.json"
     }
}
```

