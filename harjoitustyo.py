
import sqlite3
from datetime import datetime, time
import re



#Pääohjelman alustus

kanta = sqlite3.connect("kanta.db")
kanta.isolation_level = None
c = kanta.cursor()

#Metodit kannan käsittelyyn

def alusta(c):
    try:
        c.execute("CREATE TABLE Paikat(id INTEGER PRIMARY KEY, nimi TEXT, UNIQUE(nimi))")
        c.execute("CREATE TABLE Asiakkaat(id INTEGER PRIMARY KEY, nimi TEXT, UNIQUE(nimi))")
        c.execute("CREATE TABLE Paketit(id INTEGER PRIMARY KEY,asiakas_id INTEGER, seurantakoodi TEXT, UNIQUE(seurantakoodi))")
        c.execute("CREATE TABLE Tapahtumat(id INTEGER PRIMARY KEY,aika TEXT, paketti_id INTEGER, paikka_id INTEGER ,kuvaus TEXT)")
        print("tietokanta luotu")
    except:
        print("Jotakin meni vikaan.")
    pass

def lisaaPaikka(c):
    paikka = input("Anna paikan nimi:")
    sql = "INSERT INTO Paikat (nimi) VALUES (?)"
    try:
        c.execute("SELECT EXISTS(SELECT nimi FROM paikat WHERE nimi = ?)", (paikka,))
        if (c.fetchone()[0] == 1):
            print("VIRHE: Paikka on jo olemassa")
            return
        c.execute(sql,(paikka,))
        print("paikka lisätty")
    except:
        print("Jotakin meni vikaan. Et voi lisätä kahta samannimistä paikkaa.")
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
        print("Jotakin meni vikaan. Et voi lisätä kahta samannimistä asiakasta.")
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
        paketti_id = c.fetchone()[0]
        if paketti_id == None:
            print("Pakettia ei löytynyt")
        else:
            c.execute("SELECT aika,nimi,kuvaus FROM Tapahtumat,Paikat WHERE Paikat.id = Tapahtumat.paikka_id AND paketti_id=?",(paketti_id,))
            tiedot = c.fetchall()
            for x in tiedot:
                print (x)

    except:
        print("Metodissa haeSeurantakoodilla() tapahtui odottamaton virhe.")
    pass

def haeAsiakkaanPaketit(c):
    try:
        asiakas = input("Anna asiakkaan nimi:")
        c.execute("SELECT id FROM Asiakkaat WHERE nimi=?",(asiakas,))
        asiakas_id = c.fetchone()[0]
        if asiakas_id == None:
            print("Asiakasta ei löytynyt")
        else:
            c.execute("SELECT seurantakoodi, COUNT(paketti_id) FROM Paketit LEFT JOIN Tapahtumat ON Paketit.id = Tapahtumat.paketti_id WHERE asiakas_id = ? GROUP BY paketti_id",(asiakas_id,))
            tiedot = c.fetchall()
            for x in tiedot:
                print ("Seurantakoodi: " + str(x[0]) + "\t Tapahtumia yhteensä : " + str(x[1]) +"kpl")
        pass
    except:
        print("Metodissa haeAsiakkaanPaketit tapahtui odottamaton virhe.")

def haeTapahtumienMäärä(c):
    paikka = input("Anna paikan nimi:")
    c.execute("SELECT id FROM paikat WHERE nimi = ?", (paikka,))
    paikka_id = c.fetchone()[0]
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
        c.execute("SELECT COUNT (id) FROM tapahtumat WHERE paikka_id=? AND aika LIKE ? GROUP BY paikka_id",(paikka_id,pvm3))
        print("Tapahtumien määrä: " + str(c.fetchone()[0]))

    pass

def suoritaTehokkuustesti(c):
    pass

#Pääohjelma
print("-" * 80)
print("Tervetuloa paketinseurantajärjestelmään!")
while True: 
    
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
    print("Syötä haluamasi komento : ")
    komento = input()

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
    elif (komento == 'x'):
        kanta.close()
        print("-" * 80)
        print("Kiitos käytöstä!")
        print("-" * 80)

        break;
    else:
        print("Virheellinen komento")

