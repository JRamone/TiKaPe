
import sqlite3

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
        print("Tietokanta alustettu")
    elif (komento == '2'):
        print("Paikka lisätty")
    elif (komento == '3'):
        print("Asiakas lisätty")
    elif (komento == '4'):
        print("Paketti lisätty")
    elif (komento == '5'):
        print("Tapahtuma lisätty")
    elif (komento == '6'):
        print("Tapahtumat haettu")
    elif (komento == '7'):
        print("Pakettit haettu")
    elif (komento == '8'):
        print("Tapahtumien määrä haettu")
    elif (komento == '9'):
        print("Tehokkuustesti suoritettu")
    elif (komento == 'x'):
        print("-" * 80)
        print("Kiitos käytöstä!")
        print("-" * 80)
        break;
    else:
        print("Virheellinen komento")
