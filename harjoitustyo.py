
import sqlite3
from datetime import datetime, time
import time
import re
import random



#Pääohjelman alustus

kanta = sqlite3.connect("kanta.db")
kanta.isolation_level = None
c = kanta.cursor()

#Metodit kannan käsittelyyn

def alusta(c):
    try:
        
        c.execute("PRAGMA foreign_keys = ON;")
        c.execute("CREATE TABLE Paikat(id INTEGER PRIMARY KEY, nimi TEXT, UNIQUE(nimi));")
        c.execute("CREATE TABLE Asiakkaat(id INTEGER PRIMARY KEY, nimi TEXT, UNIQUE(nimi));")
        c.execute("CREATE TABLE Paketit(id INTEGER PRIMARY KEY,asiakas_id INTEGER REFERENCES Asiakkaat, seurantakoodi TEXT, UNIQUE(seurantakoodi));")
        c.execute("CREATE TABLE Tapahtumat(id INTEGER PRIMARY KEY,aika TEXT, paketti_id INTEGER REFERENCES Paketit, paikka_id INTEGER REFERENCES Paikat ,kuvaus TEXT);")
        #c.execute("CREATE INDEX idx_paketti_id ON Tapahtumat (paketti_id)")
        print("tietokanta luotu")
    except:
        print("Jotakin meni vikaan.")
    pass

def lisaaPaikka(c):
    paikka = input("Anna paikan nimi:")
    try:
        c.execute("SELECT nimi FROM paikat WHERE nimi = ?", (paikka,))
        onkopaikka = c.fetchone()
        if (onkopaikka != None):
            print("VIRHE: Paikka on jo olemassa")
            return
        else:
            c.execute("INSERT INTO Paikat (nimi) VALUES (?)", (paikka,))
        print("paikka lisätty")
    except:
        print("Jotakin meni vikaan.")
    pass

def lisaaAsiakas(c):
    asiakas = input("Anna asiakkaan nimi:")
    sql = "INSERT INTO Asiakkaat (nimi) VALUES (?)"
    args = [asiakas]
    try:
        c.execute("SELECT EXISTS(SELECT nimi FROM Asiakkaat WHERE nimi = ?)", args)
        if (c.fetchone()[0] == 1):
            print("VIRHE: Asiakas on jo olemassa")
            return
        c.execute(sql,args)
        print("Asiakas lisätty.")
    except:
        print("Jotakin meni vikaan.")
    pass

def lisaaPaketti(c):
    
    try:
        asiakas = input("Anna asiakkaan nimi:")
        args = [asiakas]

        c.execute("SELECT EXISTS(SELECT nimi FROM Asiakkaat WHERE nimi = ?)", args)
        if (c.fetchone()[0] == 0):
            print("VIRHE: Asiakasta ei ole olemassa")
            return
        c.execute("SELECT id FROM Asiakkaat WHERE nimi=?",args)

        asiakas_id = c.fetchone()[0]
        koodi = input("Anna seurantakoodi:")
        args = [koodi]

        c.execute("SELECT EXISTS(SELECT seurantakoodi FROM Paketit WHERE seurantakoodi = ?)", args)
        if (c.fetchone()[0] == 1):
            print("VIRHE: Kyseisellä seurantakoodilla löytyy jo paketti.")
            return
    
        args = [asiakas_id,koodi]     
        c.execute("INSERT INTO Paketit (asiakas_id,seurantakoodi) VALUES (?,?)",args)
        print("Asiakkaalle on lisätty paketti seurantakoodilla ")
    except:
        print("Metodissa lisaaPaketti() tapahtui odottamaton virhe.")
    pass

def lisaaTapahtuma(c): 
    try:
        koodi = input("Anna seurantakoodi:")
        args = [koodi]
        c.execute("SELECT EXISTS(SELECT seurantakoodi FROM Paketit WHERE seurantakoodi = ?)", args)
        if (c.fetchone()[0] == 0):
            print("VIRHE: Kyseisellä seurantakoodilla ei löydy pakettia")
            return
        paikka = input("Anna tapahtuman paikka:")
        args = [paikka]
        c.execute("SELECT EXISTS(SELECT nimi FROM Paikat WHERE nimi = ?)", args)
        if (c.fetchone()[0] == 0):
            print("VIRHE: Kyseisellä nimellä ei löydy paikkaa")
            return
        kuvaus = input("Anna tapahtuman kuvaus:")
        aika = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        c.execute("SELECT id FROM Paikat WHERE nimi=?",(paikka,))
        paikka_id = c.fetchone()[0]
        c.execute("SELECT id FROM Paketit WHERE seurantakoodi=?",(koodi,))
        paketti_id = c.fetchone()[0]
        args = [aika,paketti_id,paikka_id,kuvaus]
        c.execute("INSERT INTO Tapahtumat (aika,paketti_id,paikka_id,kuvaus) VALUES (?,?,?,?)",args)
        print("Tapahtuma lisätty")
    except:
        print("Metodissa lisaaTapahtuma() tapahtui odottamaton virhe.")
    pass

def haeSeurantakoodilla(c):
    try:
        koodi = input("Anna seurantakoodi:")
        c.execute("SELECT id FROM Paketit WHERE seurantakoodi=?",(koodi,))
        paketti_id = c.fetchone()
        if paketti_id == None:
            print("Pakettia ei löytynyt")
        else:
            c.execute("SELECT aika,nimi,kuvaus FROM Tapahtumat,Paikat WHERE Paikat.id = Tapahtumat.paikka_id AND paketti_id=?",(paketti_id[0],))
            tiedot = c.fetchall()
            for x in tiedot:
                print (str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))

    except:
        print("Metodissa haeSeurantakoodilla() tapahtui odottamaton virhe.")
    pass

def haeAsiakkaanPaketit(c):
    try:
        asiakas = input("Anna asiakkaan nimi:")
        c.execute("SELECT id FROM Asiakkaat WHERE nimi=?",(asiakas,))
        asiakas_id = c.fetchone()
        if asiakas_id == None:
            print("Asiakasta ei löytynyt")
        else:
            c.execute("SELECT seurantakoodi, COUNT(paketti_id) FROM Paketit LEFT JOIN Tapahtumat ON Paketit.id = Tapahtumat.paketti_id WHERE asiakas_id = ? GROUP BY paketti_id",(asiakas_id[0],))
            tiedot = c.fetchall()
            for x in tiedot:
                print ("Seurantakoodi: " + str(x[0]) + "\t Tapahtumia yhteensä : " + str(x[1]) +"kpl")
        pass
    except:
        print("Metodissa haeAsiakkaanPaketit tapahtui odottamaton virhe.")

def haeTapahtumienMäärä(c):
    paikka = input("Anna paikan nimi:")
    c.execute("SELECT id FROM paikat WHERE nimi = ?", (paikka,))
    paikka_id = c.fetchone()
    if paikka_id == None:
        print("Paikkaa ei ole olemassa")
    else:
        try:
            pvm = input("Anna päivämäärä muodossa PP.KK.VVVV ")
            pvm2 = datetime.strptime(pvm, "%d.%m.%Y")
            pvm3 = datetime.strftime(pvm2,"%d-%m-%Y")
            pvm3 += "%"
        except:
            print("Syötit päivämäärän väärin.")
            return
        c.execute("SELECT COUNT (id) FROM tapahtumat WHERE paikka_id=? AND aika LIKE ? GROUP BY paikka_id",(paikka_id[0],pvm3))
        print("Tapahtumien määrä: " + str(c.fetchone()[0]))

    pass

def suoritaTehokkuustesti(c):
    try:
        paikat = []
        asiakkaat = []
        paketit = []

        alku_aika = time.time()

        c.execute("BEGIN TRANSACTION")
        for i in range(1000):
            paikat.append("P" + str(i+1))
            c.execute("INSERT INTO Paikat (nimi) VALUES (?)", (paikat[i],))
        print("1000 Paikkaa lisätty ajassa: \t\t\t" + str(round(time.time() - alku_aika,6))+ " sek")

        alku_aika = time.time()
        for i in range(1000):
            asiakkaat.append("A" + str(i+1))
            c.execute("INSERT INTO Asiakkaat (nimi) VALUES (?)", (asiakkaat[i],))
        print("1000 Asiakasta lisätty ajassa: \t\t\t" + str(round(time.time() - alku_aika,6))+ " sek")

        alku_aika = time.time()
        random.shuffle(asiakkaat)
        for i in range(1000):
            paketit.append("Paketti" + str(i+1))
            c.execute("INSERT INTO Paketit (asiakas_id,seurantakoodi) VALUES (?,?)", (random.choice(asiakkaat)[1:],paketit[i])) #Asiakas_id ja seurantakoodi
        print("1000 Pakettia lisätty ajassa: \t\t\t" + str(round(time.time() - alku_aika,6))+ " sek")

        alku_aika = time.time()
        tapahtumat = []
        for i in range(1000000):
            tapahtumat.append("Tapahtuma" + str(i+1))
            c.execute("INSERT INTO Tapahtumat (aika,paketti_id,paikka_id,kuvaus) VALUES (?,?,?,?)", [datetime.now().strftime("%d-%m-%Y, %H:%M:%S"),random.choice(paketit)[7:],random.choice(paikat)[1:],tapahtumat[i]])
        print("1000000 Tapahtumaa lisätty ajassa: \t\t" + str(round(time.time() - alku_aika,6))+ " sek")
        c.execute("COMMIT")

        alku_aika = time.time()
        for i in range(1000):
            c.execute("SELECT COUNT (id) FROM Paketit WHERE asiakas_id = ?", (random.choice(asiakkaat)[1:],))
        print("1000 Pakettikyselyä suoritettu ajassa: \t\t" + str(round(time.time() - alku_aika,6))+ " sek")

        alku_aika = time.time()
        for i in range(1000):
            c.execute("SELECT COUNT (paketti_id) FROM Tapahtumat WHERE paketti_id = ?", (random.choice(paketit)[7:],))
        print("1000 Tapahtumakyselyä suoritettu ajassa:\t" + str(round(time.time() - alku_aika,6)) + " sek")
    except:
        print("Tehokkuustestissä meni jotakin pieleen. Suoritithan testin tyhjään tietokantaan?")
        return
    pass


def listaakomennot():

    print("(1) Alusta tietokanta")
    print("(2) Lisää uusi paikka")
    print("(3) Lisää uusi asiakas")
    print("(4) Lisää uusi paketti")
    print("(5) Lisää uusi tapahtuma")
    print("(6) Hae paketin tapahtumat seurantakoodilla")
    print("(7) Hae kaikki asiakkaan paketit ja tapahtumien määrä")
    print("(8) Hae paikasta tapahtumien määrä tiettynä päivänä")
    print("(9) Suorita tietokannan tehokkuustesti")
    print("(x) Poistu ohjelmasta")
    pass

#Pääohjelma
print("-" * 80)
print("Tervetuloa paketinseurantajärjestelmään!")
listaakomennot()
while True: 
    print("Komento L näyttää koko komentolistauksen")
    komento = input("Syötä haluamasi komento : ")
    
    if (komento == '1'):      
        alusta(c)
    elif (komento == '2'):
        lisaaPaikka(c)
    elif (komento == '3'):
        lisaaAsiakas(c)
    elif (komento == '4'):
        lisaaPaketti(c)
    elif (komento == '5'):
        lisaaTapahtuma(c)
    elif (komento == '6'):
        haeSeurantakoodilla(c)
    elif (komento == '7'):
        haeAsiakkaanPaketit(c)
    elif (komento == '8'):
        haeTapahtumienMäärä(c)
    elif (komento == '9'):
        suoritaTehokkuustesti(c)        
    elif (komento.lower() == 'l'):
        listaakomennot()
    elif (komento.lower() == 'x'):
        kanta.close()
        print("-" * 80)
        print("Kiitos käytöstä!")
        print("-" * 80)

        break;
    else:
        print("Virheellinen komento")

