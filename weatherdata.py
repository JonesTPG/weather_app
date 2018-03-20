#Tekijä: Joonas Ryynänen
#Opiskelijanumero: 0507674
#Päivämäärä: 8.11.2016
#Yhteistyö ja lähteet, nimi ja yhteistyön muoto: ohjelmointiopas
#Harjoitustyö OSA 3
#######################################################################
import svgwrite

#luodaan luokka, joka pystyy säilyttämään kaiken tarvittavan datan.
class saatiedot():
    paivays = ""
    sademaara = 0
    keskilampotila = 0
    alinlampotila = 0
    ylinlampotila = 0
    tav_ylinlampotila_A = 0
    tav_ylinlampotila_Y = 0
    tav_alinlampotila_A = 0
    tav_alinlampotila_Y = 0
    melko_tav_ylinlampotila_A = 0
    melko_tav_ylinlampotila_Y = 0
    melko_tav_alinlampotila_A = 0
    melko_tav_alinlampotila_Y = 0

#ladataan tiedot tiedostosta ja talletetaan se luokkaan.
#luokan oliot talletetaan
#listaan, jota sitten käytetään muissa aliohjelmissa
def lataatiedot(nimi):
    lista = []
    with open(nimi, "r") as tiedosto:
        tiedosto.readline()#otetaan eka rivi, missä ei dataa pois
        while True:
            rivi = tiedosto.readline()
            if rivi == "": 
                break
            rivi = rivi.split(";")
            saatieto = saatiedot()
            saatieto.paivays = rivi[0]
            saatieto.sademaara = rivi[1]
            saatieto.keskilampotila = rivi[2]
            saatieto.alinlampotila = rivi[3]
            saatieto.ylinlampotila = rivi[4]
            saatieto.tav_ylinlampotila_A = rivi[5]
            saatieto.tav_ylinlampotila_Y = rivi[6]
            saatieto.tav_alinlampotila_A = rivi[7]
            saatieto.tav_alinlampotila_Y = rivi[8]
            saatieto.melko_tav_ylinlampotila_A = rivi[9]
            saatieto.melko_tav_ylinlampotila_Y = rivi[10]
            saatieto.melko_tav_alinlampotila_A = rivi[11]
            saatieto.melko_tav_alinlampotila_Y = rivi[12]
            lista.append(saatieto)
        return lista

#lasketaan keskiarvo listan saatiedot-olioiden keskilämpötiloista
def saankeskiarvo(lista):
    summa = 0
    lkm = 0
    for i in lista:
        summa = summa + float(i.keskilampotila)
        lkm = lkm + 1
    keskiarvo = round(float(summa)/float(lkm),1)
    return keskiarvo

#etsitään suurin ja pienin lämpötila
def etsisuurinjapienin(lista):
    minimi = 10000000
    maksimi = -1000000
    for i in lista:
        if float(i.ylinlampotila) > maksimi:
            maksimi = float(i.ylinlampotila)
        if float(i.alinlampotila) < minimi:
            minimi = float(i.alinlampotila)
    return minimi, maksimi

#tallennetaan tärkeimmät tiedot tiedostoon
def tallenna(lista):
    minimi, maksimi = etsisuurinjapienin(lista)
    keskiarvo = saankeskiarvo(lista)
    nimi = input("Anna tiedostonimi: ") 
    with open(nimi, "w") as tiedosto:
        tiedosto.write("Kuukauden säätilasto kaupungissa Lappeenranta\n")
        tiedosto.write("*******************************************************\n")
        tiedosto.write("Kuukauden lämpötilan keskiarvo: " + str(keskiarvo) +" celsiusastetta.\n")
        tiedosto.write("Kuukauden lämpötilan minimi: " + str(minimi) + " celsiusastetta.\n")
        tiedosto.write("Kuukauden lämpötilan maksimi: " + str(maksimi) + " celsiusastetta.\n")
        tiedosto.write("*******************************************************\n")

#käytetään ht2-koodia avuksi, mutta otetaa lämpötilat tällä kertaa saatiedot-olioiden
#keskilämpötila-muuttujasta        
def graafinpiirto(nimi, lista):
    kuva = svgwrite.Drawing(nimi, size=('600px','600px'))
    nelio = kuva.rect((0,0), (600,600), fill='white')
    kuva.add(nelio)
    for i in range(1,6):
        suora = kuva.line((0,i*100), (600,i*100), stroke='black')
        kuva.add(suora)
        teksti = kuva.text((-i*100/10)+30, (0, i*100-3), fill='green')
        kuva.add(teksti)
    for i in range(0,29):
        suora = kuva.line((i*20,(30-float(lista[i].keskilampotila))*10),
        ((i+1)*20, (30-float(lista[i+1].keskilampotila))*10), stroke='red')
        kuva.add(suora)
    with open("kuvapisteet.csv", "w") as tiedosto:
        for i in range(0,30):
            if i < 29:
                tiedosto.write(str(round((30-float(lista[i].keskilampotila))*10)) + ",")
            elif i == 29: #viimeisestä otetaan pilkku pois
                tiedosto.write(str(round((30-float(lista[i].keskilampotila))*10)))
    return kuva
#kutsutaan graafinpiirto aliohjelmaa, ja lisätään siihen vertailukuvaaja sinisenä    
def vertailugraafi(lista):
    vertailtava = input("Anna vertailtavat säätiedot sisältävän tiedoston nimi: ")
    vertailulista = lataatiedot(vertailtava)
    nimi = input("Anna svg-tiedoston nimi: ")
    kuva = graafinpiirto(nimi, lista)
    for i in range(0,29):
        suora = kuva.line((i*20,(30-float(vertailulista[i].keskilampotila))*10),
        ((i+1)*20, (30-float(vertailulista[i+1].keskilampotila))*10), stroke='blue')
        kuva.add(suora)
    kuva.save()
    with open("kuvapisteet.csv", "w") as tiedosto:
        for i in range(0,30):
            if i < 29:
                tiedosto.write(str(round((30-float(lista[i].keskilampotila))*10)) + ",")
            elif i == 29:
                tiedosto.write(str(round((30-float(lista[i].keskilampotila))*10)))
        tiedosto.write("\n")    
        for i in range(0,30):
            if i < 29:
                tiedosto.write(str(round((30-float(vertailulista[i].keskilampotila))*10)) + ",")
            elif i == 29:
                tiedosto.write(str(round((30-float(vertailulista[i].keskilampotila))*10)))                
        print("Svg-ja csv-tiedostojen kirjoitus onnistui.")
    
#######################################################################        
#pääohjelmankin toiminnallisuus voitaisiin pakata aliohjelmaan, mutta
#tykkään enemmän tästä esitystavasta        
while True:
    print("Säätietojen käsittely")
    print("*******************************************************")
    print("1) Lataa kaupungin säätiedot tiedostosta")
    print("2) Laske keskiarvo kuukauden lämpötiloista")
    print("3) Laske kuukauden lämpötilojen minimi ja maksimi")
    print("4) Tallenna kuukauden tiedot tiedostoon")
    print("5) Piirrä graafi kuukauden lämpötiloista kaupungissa")
    print("6) Lataa toiset säätiedot ja piirrä vertailugraafi")
    print("0) Lopeta")
    valinta = int(input("Valintasi: "))
    if valinta == 1:
        nimi = input("Anna tiedostonimi: ")
        lista = lataatiedot(nimi)
        print("Tiedoston luku onnistui.")
    elif valinta == 2:
        keskiarvo = saankeskiarvo(lista)
        print("Kuukauden lämpötilan keskiarvo: " + str(keskiarvo))
    elif valinta == 3:
        minimi, maksimi = etsisuurinjapienin(lista)
        print("Kuukauden lämpötilan minimi: " + str(minimi))
        print("Kuukauden lämpötilan maksimi: " + str(maksimi))
    elif valinta == 4:
        tallenna(lista)
        print("Tallennus onnistui.")
    elif valinta == 5:
        nimi = input("Anna svg-tiedoston nimi: ")
        kuva = graafinpiirto(nimi, lista)
        kuva.save()
        print("Svg-ja csv-tiedostojen kirjoitus onnistui.")
    elif valinta == 6:
        vertailugraafi(lista)
    elif valinta == 0:
        print("Kiitos ohjelman käytöstä!")
        break
    

    

