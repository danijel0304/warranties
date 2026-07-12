# Warranties

Desktop app for tracking purchased products, warranty periods, receipts,
extended warranties, and service records.

The app uses English as the default language. Croatian is available from the
language selector in the top-right corner. The same area also contains the
Light/Dark theme switch, and both settings are saved for the next launch.

## Repository Contents

- `garancije.py` - main application
- `requirements.txt` - required Python packages
- `Pokreni_Garancije.sh` - Linux launcher
- `Pokreni_Garancije.bat` - Windows launcher
- `Pokreni_Garancije.desktop` - Linux desktop launcher
- `.gitignore` - prevents local data, receipts, backups, and settings from
  being committed

Local user data is not part of the repository. The app uses or creates these
files next to `garancije.py`:

- `moje_garancije.csv` - active local database
- `Garancije.xlsx` - local Excel file used with the records
- `dokumenti_garancija/` - saved receipts and warranty documents
- `backup/` - automatic CSV backups
- `servisi_log.json` - service history, created after the first service note
- `postavke.json` - local language and theme settings

## Running

Python 3 and Tkinter are required.

Linux:

```bash
chmod +x Pokreni_Garancije.sh
./Pokreni_Garancije.sh
```

For double-click launching on Linux, use `Pokreni_Garancije.desktop`. If your
file manager asks for confirmation, choose **Allow Launching** or
**Trust and Launch**.

Windows:

```bat
Pokreni_Garancije.bat
```

The launchers use the installed system Python. If packages from
`requirements.txt` are missing, they install them for the current user with
`pip install --user`, without creating a virtual environment.

Manual start:

```bash
python3 -m pip install -r requirements.txt
python3 garancije.py
```

On Linux distributions, Tkinter is usually installed through a system package
such as `python-tk` or `python3-tk`, depending on the distribution.

## Interface

Available options:

- English language by default
- Croatian language as an option
- Light theme
- Dark theme

The language and theme are saved in `postavke.json`, which is created
automatically after changing settings.

## Receipt OCR Optional

To read text from receipt images, you need:

- Tesseract OCR and Croatian language data
- Python packages `Pillow` and `pytesseract`

The Python packages are included in `requirements.txt`, but Tesseract itself
must be installed through the operating system package manager.

## Data And Backups

On each launch, the app copies the existing `moje_garancije.csv` file into the
`backup/` folder. The **Backup** button creates an additional backup of the CSV
database, service records, and attached documents in a folder selected by the
user.

Before manually editing or replacing the CSV file, close the app and back up
the whole local project folder.

## Notes

- Only the product name is required.
- Dates are entered as `DD.MM.YYYY`.
- Warranty duration is entered as a whole number of years.
- Excel import and export use `pandas` and `openpyxl`.
- Deleted records can be restored only during the current app session.

---

# Garancije

Desktop program za evidenciju kupljenih proizvoda, trajanja garancije, računa,
produljenih jamstava i servisnih zapisa.

Program koristi engleski kao zadani jezik. Hrvatski se može odabrati u gornjem
desnom dijelu prozora. Na istom mjestu nalazi se i izbor Light/Dark teme, a obje
postavke spremaju se za sljedeće pokretanje.

## Sadržaj Repozitorija

- `garancije.py` - glavni program
- `requirements.txt` - potrebni Python paketi
- `Pokreni_Garancije.sh` - Linux pokretač
- `Pokreni_Garancije.bat` - Windows pokretač
- `Pokreni_Garancije.desktop` - Linux desktop pokretač
- `.gitignore` - sprječava slanje lokalnih podataka, računa, sigurnosnih kopija
  i postavki u Git

Lokalni korisnički podaci nisu dio repozitorija. Program ih koristi ili stvara
uz `garancije.py`:

- `moje_garancije.csv` - aktivna lokalna baza podataka
- `Garancije.xlsx` - lokalna Excel datoteka povezana s evidencijom
- `dokumenti_garancija/` - spremljeni računi i dokumenti jamstva
- `backup/` - automatske sigurnosne kopije CSV baze
- `servisi_log.json` - povijest servisa; stvara se nakon prvog servisnog zapisa
- `postavke.json` - lokalni odabir jezika i teme

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

Ručno pokretanje:

```bash
python3 -m pip install -r requirements.txt
python3 garancije.py
```

Na distribucijama Linuxa Tkinter se obično instalira paketom `python-tk` ili
`python3-tk`, ovisno o distribuciji.

## Sučelje

U programu su dostupni:

- engleski jezik kao zadani
- hrvatski jezik kao izbor
- Light tema
- Dark tema

Odabir jezika i teme sprema se u `postavke.json`, koja se automatski stvara
nakon promjene postavki.

## OCR Računa Neobavezno

Za čitanje teksta sa slike računa potrebni su:

- Tesseract OCR i hrvatski jezični podaci
- Python paketi `Pillow` i `pytesseract`

Ti Python paketi uključeni su u `requirements.txt`, ali Tesseract treba
instalirati kroz upravitelj paketa operacijskog sustava.

## Podaci I Sigurnosne Kopije

Pri svakom pokretanju program kopira postojeći `moje_garancije.csv` u mapu
`backup/`. Gumb **Backup** izrađuje dodatnu kopiju CSV baze, servisnih zapisa i
priloženih dokumenata u mapu koju korisnik odabere.

Prije ručnog uređivanja ili zamjene CSV datoteke preporučuje se zatvoriti
program i napraviti sigurnosnu kopiju cijele lokalne mape projekta.

## Napomene

- Obavezan je samo naziv proizvoda.
- Datumi se unose u obliku `DD.MM.GGGG`.
- Trajanje garancije unosi se kao cijeli broj godina.
- Excel uvoz i izvoz koristi pakete `pandas` i `openpyxl`.
- Brisanje je moguće poništiti samo tijekom trenutačnog pokretanja programa.
