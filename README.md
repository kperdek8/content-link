# Content-link
Algorytm rekomendacji artykułów na blogu. \
Projekt składa się z dwóch części:
* Wtyczki Wordpress, która zbiera informacje o artykułach odwiedzonych przez danego użytkownika. \
* Serwera Flask zintegrowanego z algorytmem, który zwraca rekomendacje artykułów. \

Z założenia wtyczka Wordpress stanowi tylko przykładową implemetancję. Istnieje możliwość dostosowania zapytań SQL serwera Flask do własnej implementacji wtyczki, pod warunkiem że pozwala ona na ustanowienie relacji między użytkownikiem, odwiedzonymi artykułami oraz ich tagami.
