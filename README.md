# tsoha-folkshare

## FolkShare-nuotinjakosovellus

Sovelluksessa voi selata ja jakaa tekijänoikeusvapaita kansanmusiikkinuotteja. Kirjautunut käyttäjä voi myös lisätä sovellukseen nuotteja, lataamalla sovellukseen tekstipohjaista ABC-notaatiota (https://en.wikipedia.org/wiki/ABC_notation).

ABC-notaatio renderöidään nuotin näyttävälle sivulle avoimen lähdekoodin abcjs.net-kirjaston avulla (https://www.abcjs.net/).
Nuotit on jaoteltu eri kateogrioihin, kappaletyypin mukaan. 

Sovellusta voi testata osoitteessa <a href="https://tsoha-folkshare.herokuapp.com/">https://tsoha-folkshare.herokuapp.com/</a>

### Sovelluksen tämänhetkiset ominaisuudet:

- Käyttäjä voi luoda itselleen uuden käyttäjätunnuksen sekä kirjautua sisään ja ulos.
- Käyttäjä on joko peruskäyttäjä tai ylläpitäjä.
- Sovelluksen etusivu näyttää sovellukseen viimeksi lisätyt nuotit, sekä kategoriat, joihin nuotit on jaoteltu.
- Nuotteja voi hakea kappaleen nimeen kohdistuvan haun avulla.
- Nuotit voi listata kategorian mukaan.
- Ylläpitäjä voi luoda uusia kategorioita.
- Ylläpitäjä voi valita mitkä kategoriat palvelussa näytetään.
- Ylläpitäjä voi myös poistaa kategorian kokonaan. Kategoriaan liitetyt nuotit säilyvät kuitenkin palvelussa.
- Kirjautunut käyttäjä voi ladata sovellukseen uuden kappaleen antamalla kappaleen nimen ja ABC-notaation, sekä valitsemalla yhden tai useamman kategorian, johon nuotti lisätään.
- Kirjautunut käyttäjä voi muokata lisäämiään nuotteja tai poistaa lisäämänsä nuotin kokonaan.
- Ylläpitäjä voi muokata kaikkia nuotteja ja poistaa minkä nuotin tahansa.
- Kirjautunut käyttäjä voi kommentoida nuottia.
- Ylläpitäjä voi poistaa kommentteja.
- Kirjautumattomat käyttäjät voivat selata palvelusta löytyviä nuotteja. 

### Jatkokehitysideoita:

- Vahvistamistoiminto ennen kappaleen, kategorian tai kommentin lopullista poistoa 
- Käyttäjälle mahdollisuus koota suosikkinuoteistaan omia nuottialbumeja
- Kappalelistausten sivutus
- CSS-latausanimaatio nuotin piirtymistä odotellessa


