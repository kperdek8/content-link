## Docker-Compose
Skonfigurowany jest docker-compose który automatycznie stawia stronę Wordpress, bazę danych oraz automatycznie wczytuje artykuły.

### Użycie
By użyć upewnij się że masz zainstalowanego dockera, następnie skopiuj plik **.env.example** jako **.env** i wpisz `docker-compose up`.

### Domyślne porty
**Baza danych:** 3306 (widoczna tylko dla kontenerów) \
**PhpMyAdmin:** http://127.0.0.1:8080 \
**WordPress:** http://127.0.0.1:9557 \
**Serwer z algorytmem rekomendacji:** http://127.0.0.1:5000 (w domyśle widoczny tylko dla kontenerów, na potrzeby testowania widoczny dla hosta)

*Coś w konfiguracji wordpressa powoduje automatyczne przekierowanie na port 9557, więc aktualnie niemożliwa jest zmiana portu na inny.*