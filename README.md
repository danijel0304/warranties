# Garancije

Desktop program za evidenciju kupljenih proizvoda, trajanja garancije, računa,
produljenih jamstava i servisnih zapisa.

Program ima modernije, mirnije sučelje s podrškom za engleski i hrvatski jezik.
Engleski je zadani jezik, a hrvatski se može odabrati u programu. Jezik i tema
mijenjaju se u gornjem desnom dijelu prozora i spremaju se za sljedeće
pokretanje.

## Sadržaj mape

- `garancije.py` – glavni program
- `requirements.txt` – potrebni Python paketi
- `Pokreni_Garancije.sh` – Linux pokretač
- `Pokreni_Garancije.bat` – Windows pokretač
- `Pokreni_Garancije.desktop` – Linux desktop pokretač
- `.gitignore` – sprječava slanje lokalnih podataka i računa u Git

Lokalni podaci nisu dio repozitorija. Program ih automatski koristi ili stvara
uz `garancije.py`, neovisno o tome iz koje je mape pokrenut:

- `moje_garancije.csv` – aktivna baza podataka
- `Garancije.xlsx` – lokalna Excel datoteka povezana s evidencijom
- `dokumenti_garancija/` – spremljeni računi i dokumenti jamstva
- `backup/` – automatske sigurnosne kopije CSV baze
- `servisi_log.json` – povijest servisa; stvara se nakon prvog servisnog zapisa
- `postavke.json` – lokalni odabir jezika i teme

## Pokretanje

Potrebni su Python 3 i Tkinter.

Linux:

```bash
chmod +x Pokreni_Garancije.sh
./Pokreni_Garancije.sh
```

Za dvoklik na Linuxu pokrenite `Pokreni_Garancije.desktop`. Ako file manager
traži potvrdu, odaberite **Allow Launching** ili **Trust and Launch**.

Windows:

```bat
Pokreni_Garancije.bat
```

Skripte koriste instalirani Python. Ako nedostaju paketi iz `requirements.txt`,
instaliraju ih za trenutačnog korisnika preko `pip install --user`, bez `.venv`
okruženja.

## Izgled i jezik

U programu su dostupni:

- engleski jezik kao zadani
- hrvatski jezik kao izbor
- Light tema
- Dark tema

Odabir jezika i teme sprema se u `postavke.json`, koja se automatski stvara
nakon promjene postavki.

Ručno pokretanje:

```bash
python3 -m pip install -r requirements.txt
python3 garancije.py
```

Na distribucijama Linuxa Tkinter se obično instalira paketom `python-tk` ili
`python3-tk`, ovisno o distribuciji.

## OCR računa (neobavezno)

Za čitanje teksta sa slike računa potrebni su:

- Tesseract OCR i hrvatski jezični podaci
- Python paketi `Pillow` i `pytesseract`

Ti Python paketi uključeni su u `requirements.txt`, ali Tesseract treba
instalirati kroz upravitelj paketa operacijskog sustava.

## Podaci i sigurnosne kopije

Pri svakom pokretanju program kopira postojeći `moje_garancije.csv` u mapu
`backup/`. Gumb **SIGURNOSNA KOPIJA** izrađuje dodatnu kopiju CSV baze,
servisnih zapisa i priloženih dokumenata u mapu koju korisnik odabere.

Prije ručnog uređivanja ili zamjene CSV datoteke preporučuje se zatvoriti
program i napraviti sigurnosnu kopiju cijele ove mape.

## Napomene

- Obavezan je samo naziv proizvoda.
- Datumi se unose u obliku `DD.MM.GGGG`.
- Trajanje garancije unosi se kao cijeli broj godina.
- Excel uvoz i izvoz koristi pakete `pandas` i `openpyxl`.
- Brisanje je moguće poništiti samo tijekom trenutačnog pokretanja programa.
