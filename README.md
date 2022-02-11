# tsoha-folkshare

## FolkShare-nuotinjakosovellus

Sovelluksessa voi selata ja jakaa tekijänoikeusvapaita kansanmusiikkinuotteja. Kirjautunut käyttäjä voi myös lisätä sovellukseen nuotteja, lataamalla sovellukseen tekstipohjaista ABC-notaatiota (https://en.wikipedia.org/wiki/ABC_notation).

ABC-notaatio renderöidään nuotin näyttävälle sivulle avoimen lähdekoodin abcjs.net-kirjaston avulla (https://www.abcjs.net/).
Nuotit on jaoteltu eri kateogrioihin, kappaletyypin mukaan. 

Sovellusta voi testata osoitteessa <a href="https://tsoha-folkshare.herokuapp.com/">https://tsoha-folkshare.herokuapp.com/</a>

### Sovelluksen tämänhetkiset ominaisuudet:

- Käyttäjä on joko peruskäyttäjä tai ylläpitäjä.
- Käyttäjä voi luoda itselleen uuden käyttäjätunnuksen sekä kirjautua sisään ja ulos.
- Sovelluksen etusivu näyttää sovellukseen viimeksi lisätyt nuotit, sekä kategoriat, joihin nuotit on jaoteltu.
- Nuotit voi listata kategorian mukaan.
- Kirjautunut käyttäjä voi ladata sovellukseen uuden kappaleen antamalla kappaleen nimen ja ABC-notaation, sekä valitsemalla yhden tai useamman kategorian, johon nuotti lisätään.
- Ylläpitäjä voi luoda uusia kategorioita.
- Kirjautunut käyttäjä voi poistaa lisäämänsä nuotin.
- Ylläpitäjä voi poistaa minkä tahansa nuotin,
- Myös kirjautumattomat käyttäjät voivat selata palvelusta löytyviä nuotteja. 

### Työn alla:

- Kirjautunut käyttäjä voi muokata lisäämiään nuotteja.
- Ylläpitäjä voi muokata mitä nuottia tahansa.
- Ylläpitäjä voi piilottaa kategorian.
- Nuottien kommentointitoiminnallisuus. Kirjautunut käyttäjä voi kommentoida nuottia. Käyttäjä voi myös poistaa kirjoittamansa kommentin. Ylläpitäjä voi poistaa minkä kommentin tahansa.
- Hakutoiminnallisuus
- Looginen navigaatio ja palvelun yleinen rakenne 
- Sovelluksen graafinen ulkoasu
- Jotkut ABC-notaatiossa käytettävät erikoismerkit sekä rivinvaihdot syöttölomakkeessa aiheuttavat vielä ongelmia. Käyttäjälle palaute siitä, että notaatiossa on syntaksivirhe, jonka takia sitä ei pystytä näyttämään. 
