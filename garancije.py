import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import re
import sqlite3
from datetime import datetime
import os
import shutil
import uuid
import platform
import subprocess
import sys
import pandas as pd

# --- KONFIGURACIJA ---

def odredi_baznu_mapu():
    if not getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))

    izvrsna_mapa = os.path.dirname(os.path.abspath(sys.executable))
    if os.access(izvrsna_mapa, os.W_OK):
        return izvrsna_mapa

    dokumenti = os.path.join(os.path.expanduser("~"), "Documents")
    if os.path.isdir(dokumenti):
        return os.path.join(dokumenti, "Garancije")

    return os.path.join(os.path.expanduser("~"), "Garancije")


BAZNA_MAPA = odredi_baznu_mapu()
DATABASE_DATOTEKA = os.path.join(BAZNA_MAPA, "garancije.db")
DATOTEKA = os.path.join(BAZNA_MAPA, "moje_garancije.csv")
SERVISI_DATOTEKA = os.path.join(BAZNA_MAPA, "servisi_log.json")
DOKUMENTI_MAPA = os.path.join(BAZNA_MAPA, "dokumenti_garancija")
BACKUP_MAPA = os.path.join(BAZNA_MAPA, "backup")
POSTAVKE_DATOTEKA = os.path.join(BAZNA_MAPA, "postavke.json")

STUPCI = ["ID", "Trgovina", "Broj Računa", "Naziv Proizvoda", "Šifra", "Cijena (€)", "Datum Kupovine", "Trajanje Garancije (god)", "Datum Isteka Garancije", "Originalni Račun", "Produljeno Jamstvo"]
DB_STUPCI = [
    "id",
    "trgovina",
    "broj_racuna",
    "naziv_proizvoda",
    "sifra",
    "cijena",
    "datum_kupovine",
    "trajanje_garancije",
    "datum_isteka",
    "originalni_racun",
    "produljeno_jamstvo",
]

JEZICI = {"en": "English", "hr": "Hrvatski"}
JEZICI_PO_NAZIVU = {naziv: kod for kod, naziv in JEZICI.items()}

PRIJEVODI = {
    "hr": {
        "app_title": "Garancije",
        "app_subtitle": "Evidencija kupnji, računa i servisa",
        "new_entry": "Novi unos",
        "ocr_button": "OCR računa",
        "choose": "Odaberi",
        "remove": "Ukloni",
        "add": "Dodaj",
        "clear": "Očisti",
        "backup": "Sigurnosna kopija",
        "theme": "Tema",
        "theme_dark": "Tamna",
        "theme_light": "Svijetla",
        "language": "Jezik",
        "filter": "Filter",
        "total_fmt": "Ukupno: {count}",
        "active_fmt": "Aktivno: {count}",
        "expired_fmt": "Isteklo: {count}",
        "search": "Pretraži",
        "delete_selected": "Obriši odabrano",
        "delete_expired": "Obriši istekle",
        "restore_deleted": "Vrati izbrisano",
        "export_excel": "Izvezi u Excel",
        "import_excel": "Uvezi iz Excela",
        "menu_open_receipt": "Otvori originalni račun",
        "menu_open_warranty": "Otvori produljeno jamstvo",
        "menu_service_history": "Povijest servisa",
        "menu_edit_product": "Uredi proizvod",
        "select_receipt_image": "Odaberi sliku računa",
        "filetype_images": "Slike",
        "loading_title": "Učitavam",
        "loading_ocr": "Skeniram sliku. Ovo može potrajati nekoliko sekundi.",
        "ocr_window_title": "Očitani račun",
        "ocr_raw_text_label": "Tekst koji je program pročitao s računa:",
        "ocr_detected_label": "Automatski prepoznati podaci:",
        "date": "Datum",
        "amount": "Iznos (€)",
        "keep_ocr_data": "Zadrži ove podatke",
        "transferred_title": "Prebačeno",
        "transferred_msg": "Dopunite naziv proizvoda i trgovinu, zatim spremite unos.",
        "missing_module_title": "Nedostaje modul",
        "missing_module_msg": "Za OCR instalirajte Tesseract OCR i Python pakete iz requirements.txt.",
        "ocr_error_title": "Greška u prepoznavanju",
        "ocr_error_msg": "Nisam uspio pročitati sliku.\nDetalji greške: {error}",
        "delete_title": "Brisanje",
        "delete_expired_confirm": "Obrisati svih {count} isteklih garancija?",
        "delete_selected_confirm": "Obrisati odabrano?",
        "required_title": "Nedostaje podatak",
        "required_product": "Naziv proizvoda je obavezan.",
        "doc_missing_title": "Dokument",
        "doc_missing": "Dokument nije priložen.",
        "edit_title": "Uredi proizvod",
        "save": "Spremi",
        "service_title": "Povijest servisa",
        "recorded_repairs": "Zabilježeni popravci",
        "add_service": "Dodaj zapis",
        "import_title": "Uvoz",
        "import_success": "Uvoz završen.\nDodano/ažurirano zapisa: {records}\nDokumenata vraćeno: {docs}\nDokumenata nije pronađeno: {missing}",
        "export_title": "Izvoz",
        "export_success": "Uspješno izvezeno u Excel.",
        "export_success_with_docs": "Uspješno izvezeno u Excel.\nDokumenti su kopirani u:\n{path}",
        "filetype_excel": "Excel",
        "filetype_excel_csv": "Excel/CSV",
        "error_title": "Greška",
        "backup_select_title": "Odaberi mapu za spremanje sigurnosne kopije",
        "backup_success_title": "Uspjeh",
        "backup_success": "Sigurnosna kopija svih podataka uspješno je spremljena u:\n{path}",
        "backup_error": "Došlo je do greške prilikom izrade sigurnosne kopije:\n{error}",
        "doc_receipt": "RAČUN",
        "doc_warranty": "JAMSTVO",
        "columns": {
            "ID": "ID",
            "Trgovina": "Trgovina",
            "Broj Računa": "Broj računa",
            "Naziv Proizvoda": "Naziv proizvoda",
            "Šifra": "Šifra",
            "Cijena (€)": "Cijena (€)",
            "Datum Kupovine": "Datum kupovine",
            "Trajanje Garancije (god)": "Trajanje garancije (god)",
            "Datum Isteka Garancije": "Datum isteka garancije",
            "Originalni Račun": "Originalni račun",
            "Produljeno Jamstvo": "Produljeno jamstvo",
        },
    },
    "en": {
        "app_title": "Warranties",
        "app_subtitle": "Purchases, receipts and service records",
        "new_entry": "New entry",
        "ocr_button": "Receipt OCR",
        "choose": "Choose",
        "remove": "Remove",
        "add": "Add",
        "clear": "Clear",
        "backup": "Backup",
        "theme": "Theme",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "language": "Language",
        "filter": "Filter",
        "total_fmt": "Total: {count}",
        "active_fmt": "Active: {count}",
        "expired_fmt": "Expired: {count}",
        "search": "Search",
        "delete_selected": "Delete selected",
        "delete_expired": "Delete expired",
        "restore_deleted": "Restore deleted",
        "export_excel": "Export to Excel",
        "import_excel": "Import from Excel",
        "menu_open_receipt": "Open original receipt",
        "menu_open_warranty": "Open extended warranty",
        "menu_service_history": "Service history",
        "menu_edit_product": "Edit product",
        "select_receipt_image": "Choose receipt image",
        "filetype_images": "Images",
        "loading_title": "Loading",
        "loading_ocr": "Scanning the image. This can take a few seconds.",
        "ocr_window_title": "Scanned receipt",
        "ocr_raw_text_label": "Text read from the receipt:",
        "ocr_detected_label": "Automatically detected data:",
        "date": "Date",
        "amount": "Amount (€)",
        "keep_ocr_data": "Keep these values",
        "transferred_title": "Transferred",
        "transferred_msg": "Fill in the product name and store, then save the entry.",
        "missing_module_title": "Missing module",
        "missing_module_msg": "Install Tesseract OCR and the Python packages from requirements.txt to use OCR.",
        "ocr_error_title": "Recognition error",
        "ocr_error_msg": "I could not read the image.\nError details: {error}",
        "delete_title": "Delete",
        "delete_expired_confirm": "Delete all {count} expired warranties?",
        "delete_selected_confirm": "Delete selected items?",
        "required_title": "Missing field",
        "required_product": "Product name is required.",
        "doc_missing_title": "Document",
        "doc_missing": "No document is attached.",
        "edit_title": "Edit product",
        "save": "Save",
        "service_title": "Service history",
        "recorded_repairs": "Recorded repairs",
        "add_service": "Add note",
        "import_title": "Import",
        "import_success": "Import finished.\nAdded/updated records: {records}\nDocuments restored: {docs}\nDocuments not found: {missing}",
        "export_title": "Export",
        "export_success": "Successfully exported to Excel.",
        "export_success_with_docs": "Successfully exported to Excel.\nDocuments were copied to:\n{path}",
        "filetype_excel": "Excel",
        "filetype_excel_csv": "Excel/CSV",
        "error_title": "Error",
        "backup_select_title": "Choose backup destination folder",
        "backup_success_title": "Success",
        "backup_success": "All data was backed up successfully to:\n{path}",
        "backup_error": "An error occurred while creating the backup:\n{error}",
        "doc_receipt": "RECEIPT",
        "doc_warranty": "WARRANTY",
        "columns": {
            "ID": "ID",
            "Trgovina": "Store",
            "Broj Računa": "Receipt number",
            "Naziv Proizvoda": "Product name",
            "Šifra": "Code",
            "Cijena (€)": "Price (€)",
            "Datum Kupovine": "Purchase date",
            "Trajanje Garancije (god)": "Warranty length (years)",
            "Datum Isteka Garancije": "Warranty expiry date",
            "Originalni Račun": "Original receipt",
            "Produljeno Jamstvo": "Extended warranty",
        },
    },
}

class GarancijeApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x850")
        self.root.minsize(1180, 720)

        self.postavke = self.ucitaj_postavke()
        self.jezik = self.postavke.get("jezik", "en")
        if self.jezik not in PRIJEVODI:
            self.jezik = "en"
        self.tema = self.postavke.get("tema")
        if self.tema not in ("light", "dark"):
            self.tema = "dark" if bool(self.postavke.get("dark_mode", False)) else "light"
        self.dark_mode = self.tema == "dark"
        self.svi_podaci = []
        self.servisi_podaci = {}
        self.povijest_brisanja = []
        self.trenutni_filter = "SVI"
        self.db = None

        self.putanja_orig_racun = tk.StringVar()
        self.putanja_prod_jamstvo = tk.StringVar()

        self.inicijaliziraj_sustav()
        self.postavi_stilove()
        self.root.title(self.t("app_title"))
        self.kreiraj_sucelje()
        self.popravi_i_ucitaj_podatke()
        self.automatski_lokalni_backup()

    def ucitaj_postavke(self):
        if not os.path.exists(POSTAVKE_DATOTEKA):
            return {}
        try:
            with open(POSTAVKE_DATOTEKA, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def spremi_postavke(self):
        postavke = {"jezik": self.jezik, "tema": self.tema, "dark_mode": self.dark_mode}
        with open(POSTAVKE_DATOTEKA, 'w', encoding='utf-8') as f:
            json.dump(postavke, f, ensure_ascii=False, indent=2)

    def t(self, kljuc, **vrijednosti):
        tekst = PRIJEVODI.get(self.jezik, PRIJEVODI["en"]).get(kljuc, PRIJEVODI["en"].get(kljuc, kljuc))
        return tekst.format(**vrijednosti) if vrijednosti else tekst

    def naziv_stupca(self, stupac):
        return PRIJEVODI.get(self.jezik, PRIJEVODI["en"])["columns"].get(stupac, stupac)

    def naziv_trenutne_teme(self):
        return self.t("theme_dark") if self.dark_mode else self.t("theme_light")

    def inicijaliziraj_sustav(self):
        for mapa in [BACKUP_MAPA, DOKUMENTI_MAPA]:
            if not os.path.exists(mapa): os.makedirs(mapa)
        self.inicijaliziraj_bazu()
        self.migriraj_legacy_podatke()

    def inicijaliziraj_bazu(self):
        self.db = sqlite3.connect(DATABASE_DATOTEKA)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS garancije (
                id TEXT PRIMARY KEY,
                trgovina TEXT NOT NULL DEFAULT '',
                broj_racuna TEXT NOT NULL DEFAULT '',
                naziv_proizvoda TEXT NOT NULL DEFAULT '',
                sifra TEXT NOT NULL DEFAULT '',
                cijena TEXT NOT NULL DEFAULT '',
                datum_kupovine TEXT NOT NULL DEFAULT '',
                trajanje_garancije TEXT NOT NULL DEFAULT '',
                datum_isteka TEXT NOT NULL DEFAULT '',
                originalni_racun TEXT NOT NULL DEFAULT '',
                produljeno_jamstvo TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS servisi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                garancija_id TEXT NOT NULL,
                datum TEXT NOT NULL DEFAULT '',
                opis TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.db.commit()

    def broj_redaka_u_bazi(self, tablica):
        cur = self.db.execute(f"SELECT COUNT(*) FROM {tablica}")
        return cur.fetchone()[0]

    def dohvati_meta(self, kljuc):
        cur = self.db.execute("SELECT value FROM meta WHERE key = ?", (kljuc,))
        red = cur.fetchone()
        return red[0] if red else ""

    def postavi_meta(self, kljuc, vrijednost):
        with self.db:
            self.db.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
                (kljuc, vrijednost)
            )

    def normaliziraj_redak_podataka(self, red):
        if len(red) == 12:
            red = [red[0]] + red[2:]
        elif len(red) == 10:
            red = red[:-1] + ["", red[-1]]
        elif len(red) < 10:
            red = [str(uuid.uuid4())[:8]] + red[-9:]

        red = list(red)
        while len(red) < len(STUPCI):
            red.append("")

        red = ["" if vrijednost is None else str(vrijednost) for vrijednost in red[:len(STUPCI)]]
        if not red[0]:
            red[0] = str(uuid.uuid4())[:8]
        if not red[8]:
            red[8] = self.izracunaj_istek(red[6], red[7])
        return red

    def ucitaj_podatke_iz_csv_datoteke(self, putanja):
        podaci = []
        with open(putanja, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for red in reader:
                if not red or len(red) < 4:
                    continue
                podaci.append(self.normaliziraj_redak_podataka(red))
        return podaci

    def migriraj_legacy_podatke(self):
        if os.path.exists(DATOTEKA) and self.dohvati_meta("legacy_csv_migrated") != "1":
            if self.broj_redaka_u_bazi("garancije") == 0:
                self.svi_podaci = self.ucitaj_podatke_iz_csv_datoteke(DATOTEKA)
                self.spremi_sve_u_bazu()
            self.postavi_meta("legacy_csv_migrated", "1")

        if os.path.exists(SERVISI_DATOTEKA) and self.dohvati_meta("legacy_services_migrated") != "1":
            if self.broj_redaka_u_bazi("servisi") == 0:
                self.servisi_podaci = self.ucitaj_servise_iz_json_datoteke(SERVISI_DATOTEKA)
                self.spremi_sve_servise_u_bazu()
            self.postavi_meta("legacy_services_migrated", "1")

    def automatski_lokalni_backup(self):
        if self.svi_podaci and os.path.exists(DATABASE_DATOTEKA):
            datum = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.napravi_backup_baze(os.path.join(BACKUP_MAPA, f"backup_{datum}.db"))
            self.izvezi_podatke_u_csv(os.path.join(BACKUP_MAPA, f"backup_{datum}.csv"))

    def napravi_backup_baze(self, putanja):
        with sqlite3.connect(putanja) as backup_db:
            self.db.backup(backup_db)

    def popravi_i_ucitaj_podatke(self):
        self.svi_podaci = self.ucitaj_sve_iz_baze()
        self.servisi_podaci = self.ucitaj_servise_iz_baze()
        self.osvjezi_tablicu_i_statistiku()

    def ucitaj_sve_iz_baze(self):
        cur = self.db.execute(f"SELECT {', '.join(DB_STUPCI)} FROM garancije ORDER BY rowid")
        return [["" if vrijednost is None else str(vrijednost) for vrijednost in red] for red in cur.fetchall()]

    def spremi_sve_u_bazu(self):
        sada = datetime.now().isoformat(timespec="seconds")
        with self.db:
            self.db.execute("DELETE FROM garancije")
            for red in self.svi_podaci:
                red = self.normaliziraj_redak_podataka(red)
                vrijednosti = red + [sada, sada]
                self.db.execute(
                    f"""
                    INSERT OR REPLACE INTO garancije ({', '.join(DB_STUPCI)}, created_at, updated_at)
                    VALUES ({', '.join(['?'] * (len(DB_STUPCI) + 2))})
                    """,
                    vrijednosti
                )

    def ucitaj_servise_iz_baze(self):
        cur = self.db.execute("SELECT garancija_id, datum, opis FROM servisi ORDER BY id")
        servisi = {}
        for p_id, datum, opis in cur.fetchall():
            servisi.setdefault(p_id, []).append({"datum": datum or "", "opis": opis or ""})
        return servisi

    def ucitaj_servise_iz_json_datoteke(self, putanja):
        try:
            with open(putanja, 'r', encoding='utf-8') as f:
                podaci = json.load(f)
            return podaci if isinstance(podaci, dict) else {}
        except Exception:
            return {}

    def spremi_sve_servise_u_bazu(self):
        sada = datetime.now().isoformat(timespec="seconds")
        with self.db:
            self.db.execute("DELETE FROM servisi")
            for p_id, zapisi in self.servisi_podaci.items():
                if not isinstance(zapisi, list):
                    continue
                for zapis in zapisi:
                    if not isinstance(zapis, dict):
                        continue
                    self.db.execute(
                        "INSERT INTO servisi (garancija_id, datum, opis, created_at) VALUES (?, ?, ?, ?)",
                        (p_id, str(zapis.get("datum", "")), str(zapis.get("opis", "")), sada)
                    )

    def spremi_servis_u_bazu(self, p_id, zapis):
        with self.db:
            self.db.execute(
                "INSERT INTO servisi (garancija_id, datum, opis, created_at) VALUES (?, ?, ?, ?)",
                (p_id, zapis["datum"], zapis["opis"], datetime.now().isoformat(timespec="seconds"))
            )

    def postavi_stilove(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.azuriraj_temu()

    def azuriraj_temu(self):
        if self.dark_mode:
            self.boje = {
                "bg": "#20231f",
                "panel": "#282c28",
                "panel_alt": "#303530",
                "sidebar": "#252a25",
                "sidebar_text": "#dce2dc",
                "sidebar_muted": "#a6ada6",
                "text": "#dce2dc",
                "muted": "#aeb6ae",
                "border": "#3c443d",
                "entry": "#252a25",
                "heading": "#333932",
                "accent": "#6f967d",
                "accent_dark": "#5d826c",
                "secondary": "#4b554d",
                "danger": "#9b665f",
                "warning": "#967850",
                "success": "#668a70",
                "row_ok": "#26342b",
                "row_expired": "#3a2d2b",
                "row_ok_text": "#c9d8ce",
                "row_expired_text": "#dbc4c0",
            }
        else:
            self.boje = {
                "bg": "#f1f3f0",
                "panel": "#fbfbf8",
                "panel_alt": "#e7ebe6",
                "sidebar": "#e2e7e1",
                "sidebar_text": "#2f3832",
                "sidebar_muted": "#6d766f",
                "text": "#28312b",
                "muted": "#6d766f",
                "border": "#d4dbd2",
                "entry": "#fbfbf8",
                "heading": "#e4e9e2",
                "accent": "#6f967d",
                "accent_dark": "#5d826c",
                "secondary": "#7d887f",
                "danger": "#a86a62",
                "warning": "#9b8058",
                "success": "#6f967d",
                "row_ok": "#edf3ee",
                "row_expired": "#f6ece9",
                "row_ok_text": "#4d6d59",
                "row_expired_text": "#865b55",
            }

        c = self.boje
        self.bg_sidebar = c["sidebar"]
        self.root.configure(bg=c["bg"])
        self.style.configure("Sidebar.TFrame", background=c["sidebar"])
        self.style.configure("Main.TFrame", background=c["bg"])
        self.style.configure("Panel.TFrame", background=c["panel"])
        self.style.configure("TLabel", background=c["bg"], foreground=c["text"], font=('Segoe UI', 10))
        self.style.configure("Muted.TLabel", background=c["bg"], foreground=c["muted"], font=('Segoe UI', 9))
        self.style.configure("Panel.TLabel", background=c["panel"], foreground=c["text"], font=('Segoe UI', 10))
        self.style.configure("Sidebar.TLabel", background=c["sidebar"], foreground=c["sidebar_text"], font=('Segoe UI', 10))
        self.style.configure("SidebarMuted.TLabel", background=c["sidebar"], foreground=c["sidebar_muted"], font=('Segoe UI', 9))
        self.style.configure("TEntry", fieldbackground=c["entry"], foreground=c["text"], bordercolor=c["border"], lightcolor=c["border"], darkcolor=c["border"], padding=4)
        self.style.configure("TCombobox", fieldbackground=c["entry"], foreground=c["text"], arrowcolor=c["text"], bordercolor=c["border"], padding=4)
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", c["entry"]), ("!disabled", c["entry"])],
            foreground=[("readonly", c["text"]), ("!disabled", c["text"])],
            selectbackground=[("readonly", c["entry"]), ("!disabled", c["entry"])],
            selectforeground=[("readonly", c["text"]), ("!disabled", c["text"])],
            arrowcolor=[("readonly", c["text"]), ("!disabled", c["text"])],
        )
        self.root.option_add("*TCombobox*Listbox.background", c["panel"])
        self.root.option_add("*TCombobox*Listbox.foreground", c["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", c["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.style.configure("Treeview", background=c["panel"], fieldbackground=c["panel"], foreground=c["text"], rowheight=32, borderwidth=0, font=('Segoe UI', 10))
        self.style.configure("Treeview.Heading", background=c["heading"], foreground=c["text"], relief="flat", font=('Segoe UI', 10, 'bold'))
        self.style.map("Treeview", background=[("selected", c["accent_dark"])], foreground=[("selected", "#ffffff")])

    def gumb(self, roditelj, tekst, naredba, vrsta="secondary", font_size=10):
        c = self.boje
        pozadine = {
            "primary": c["accent"],
            "secondary": c["secondary"],
            "danger": c["danger"],
            "warning": c["warning"],
            "success": c["success"],
        }
        bg = pozadine.get(vrsta, c["secondary"])
        return tk.Button(
            roditelj,
            text=tekst,
            command=naredba,
            bg=bg,
            fg="#ffffff",
            activebackground=c["accent_dark"] if vrsta == "primary" else bg,
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            font=('Segoe UI', font_size, 'bold'),
            padx=12,
            pady=7,
        )

    def labela(self, roditelj, tekst, bg=None, fg=None, font=('Segoe UI', 10), **kwargs):
        c = self.boje
        return tk.Label(roditelj, text=tekst, bg=bg or c["bg"], fg=fg or c["text"], font=font, **kwargs)

    def stiliziraj_prozor(self, prozor, naslov, geometrija=None):
        prozor.title(naslov)
        if geometrija:
            prozor.geometry(geometrija)
        prozor.configure(bg=self.boje["bg"])

    def kreiraj_sucelje(self):
        c = self.boje

        sidebar = tk.Frame(self.root, bg=c["sidebar"], width=330)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        header = tk.Frame(sidebar, bg=c["sidebar"])
        header.pack(fill="x", padx=22, pady=(24, 18))
        self.labela(header, self.t("app_title"), bg=c["sidebar"], fg=c["sidebar_text"], font=('Segoe UI', 22, 'bold')).pack(anchor="w")
        self.labela(header, self.t("app_subtitle"), bg=c["sidebar"], fg=c["sidebar_muted"], font=('Segoe UI', 9), wraplength=260, justify="left").pack(anchor="w", pady=(4, 0))

        self.labela(sidebar, self.t("new_entry"), bg=c["sidebar"], fg=c["sidebar_text"], font=('Segoe UI', 12, 'bold')).pack(anchor="w", padx=22, pady=(4, 10))
        self.gumb(sidebar, self.t("ocr_button"), self.pravi_ocr_izbornik, "secondary").pack(fill="x", padx=22, pady=(0, 14))

        self.unos_vars = {}
        for p in STUPCI[1:-2]:
            self.labela(sidebar, self.naziv_stupca(p), bg=c["sidebar"], fg=c["sidebar_muted"], font=('Segoe UI', 8, 'bold')).pack(anchor="w", padx=22, pady=(6, 2))
            v = tk.StringVar()
            ttk.Entry(sidebar, textvariable=v, font=('Segoe UI', 10)).pack(fill="x", padx=22, pady=1, ipady=3)
            self.unos_vars[p] = v

        for naslov, var in [(self.naziv_stupca("Originalni Račun"), self.putanja_orig_racun), (self.naziv_stupca("Produljeno Jamstvo"), self.putanja_prod_jamstvo)]:
            self.labela(sidebar, naslov, bg=c["sidebar"], fg=c["sidebar_muted"], font=('Segoe UI', 8, 'bold')).pack(anchor="w", padx=22, pady=(10, 2))
            okvir = tk.Frame(sidebar, bg=c["sidebar"])
            okvir.pack(fill="x", padx=22)
            ttk.Entry(okvir, textvariable=var, state="readonly", font=('Segoe UI', 9)).pack(side="left", fill="x", expand=True, ipady=3)
            self.gumb(okvir, "X", lambda v=var: v.set(""), "secondary", 9).pack(side="right", padx=(6, 0))
            self.gumb(okvir, self.t("choose"), lambda v=var: self.odaberi_doc(v), "secondary", 9).pack(side="right", padx=(6, 0))

        okvir_akcije = tk.Frame(sidebar, bg=c["sidebar"])
        okvir_akcije.pack(fill="x", padx=22, pady=18)
        self.gumb(okvir_akcije, self.t("add"), self.spremi_novi, "primary", 10).pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.gumb(okvir_akcije, self.t("clear"), self.ocisti_unos, "secondary", 10).pack(side="right", fill="x", expand=True, padx=(6, 0))

        bot = tk.Frame(sidebar, bg=c["sidebar"])
        bot.pack(side="bottom", fill="x", padx=22, pady=18)
        self.gumb(bot, self.t("backup"), self.napravi_rucni_backup, "secondary", 9).pack(fill="x")

        main = tk.Frame(self.root, bg=c["bg"])
        main.pack(side="right", fill="both", expand=True, padx=24, pady=22)

        top_bar = tk.Frame(main, bg=c["bg"])
        top_bar.pack(fill="x", pady=(0, 8))

        self.labela(top_bar, f"{self.t('filter')}:", bg=c["bg"], fg=c["muted"], font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(0, 8))

        self.lbl_stat_ukupno = tk.Label(top_bar, text=self.t("total_fmt", count=0), font=('Segoe UI', 10, 'bold'), bg=c["panel_alt"], fg=c["text"], padx=12, pady=7, cursor="hand2", bd=0)
        self.lbl_stat_ukupno.pack(side="left", padx=(0, 8))
        self.lbl_stat_ukupno.bind("<Button-1>", lambda e: self.postavi_filter("SVI"))

        self.lbl_stat_aktivno = tk.Label(top_bar, text=self.t("active_fmt", count=0), font=('Segoe UI', 10, 'bold'), bg=c["panel_alt"], fg=c["text"], padx=12, pady=7, cursor="hand2", bd=0)
        self.lbl_stat_aktivno.pack(side="left", padx=(0, 8))
        self.lbl_stat_aktivno.bind("<Button-1>", lambda e: self.postavi_filter("AKTIVNI"))

        self.lbl_stat_isteklo = tk.Label(top_bar, text=self.t("expired_fmt", count=0), font=('Segoe UI', 10, 'bold'), bg=c["panel_alt"], fg=c["text"], padx=12, pady=7, cursor="hand2", bd=0)
        self.lbl_stat_isteklo.pack(side="left")
        self.lbl_stat_isteklo.bind("<Button-1>", lambda e: self.postavi_filter("ISTEKLI"))

        postavke_okvir = tk.Frame(top_bar, bg=c["bg"])
        postavke_okvir.pack(side="right")

        self.labela(postavke_okvir, f"{self.t('language')}:", bg=c["bg"], fg=c["muted"], font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(0, 6))
        self.var_jezik = tk.StringVar(value=JEZICI[self.jezik])
        combo_jezik = ttk.Combobox(postavke_okvir, textvariable=self.var_jezik, values=list(JEZICI.values()), state="readonly", width=10)
        combo_jezik.pack(side="left", padx=(0, 14), ipady=3)
        combo_jezik.bind("<<ComboboxSelected>>", self.promijeni_jezik)

        self.labela(postavke_okvir, f"{self.t('theme')}:", bg=c["bg"], fg=c["muted"], font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(0, 6))
        self.var_tema = tk.StringVar(value=self.tema)
        tema_okvir = tk.Frame(postavke_okvir, bg=c["bg"])
        tema_okvir.pack(side="left")
        for vrijednost, tekst in [("light", self.t("theme_light")), ("dark", self.t("theme_dark"))]:
            odabrano = self.tema == vrijednost
            tk.Radiobutton(
                tema_okvir,
                text=tekst,
                value=vrijednost,
                variable=self.var_tema,
                command=self.promijeni_temu,
                indicatoron=False,
                bg=c["accent"] if odabrano else c["panel_alt"],
                fg="#ffffff" if odabrano else c["text"],
                selectcolor=c["accent"],
                activebackground=c["accent_dark"],
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                cursor="hand2",
                font=('Segoe UI', 9, 'bold'),
                padx=10,
                pady=6,
            ).pack(side="left", padx=(0, 5) if vrijednost == "light" else (0, 0))

        search_bar = tk.Frame(main, bg=c["bg"])
        search_bar.pack(fill="x", pady=(0, 14))
        okvir_trazi = tk.Frame(search_bar, bg=c["bg"])
        okvir_trazi.pack(side="right")
        self.labela(okvir_trazi, f"{self.t('search')}:", bg=c["bg"], fg=c["muted"], font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(0, 8))
        self.var_pretraga = tk.StringVar()
        self.var_pretraga.trace_add("write", self.primijeni_pretragu)
        ttk.Entry(okvir_trazi, textvariable=self.var_pretraga, width=34, font=('Segoe UI', 10)).pack(side="left", ipady=5)

        tab_frame = tk.Frame(main, bg=c["panel"], highlightbackground=c["border"], highlightthickness=1, bd=0)
        tab_frame.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(tab_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(tab_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(tab_frame, columns=STUPCI, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.osnovne_sirine_stupaca = {
            "ID": 0,
            "Trgovina": 130,
            "Broj Računa": 125,
            "Naziv Proizvoda": 190,
            "Šifra": 95,
            "Cijena (€)": 105,
            "Datum Kupovine": 130,
            "Trajanje Garancije (god)": 180,
            "Datum Isteka Garancije": 165,
            "Originalni Račun": 135,
            "Produljeno Jamstvo": 155,
        }
        self.min_sirine_stupaca = {
            "Trgovina": 72,
            "Broj Računa": 72,
            "Naziv Proizvoda": 105,
            "Šifra": 54,
            "Cijena (€)": 64,
            "Datum Kupovine": 82,
            "Trajanje Garancije (god)": 92,
            "Datum Isteka Garancije": 92,
            "Originalni Račun": 78,
            "Produljeno Jamstvo": 88,
        }
        self._zadnja_sirina_tablice = 0
        for s in STUPCI:
            self.tree.heading(s, text=self.naziv_stupca(s), command=lambda _s=s: self.sortiraj(_s))
            sirina = self.osnovne_sirine_stupaca.get(s, 120)
            min_sirina = 0 if s == "ID" else self.min_sirine_stupaca.get(s, 60)
            self.tree.column(s, width=sirina, minwidth=min_sirina, stretch=False, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Configure>", self.prilagodi_sirine_stupaca)
        self.tree.bind("<Button-3>", self.prikazi_meni)
        self.tree.bind("<Double-1>", self.dvostruki_klik_otvori)
        self.root.after_idle(self.prilagodi_sirine_stupaca)

        bot_bar = tk.Frame(main, bg=c["bg"])
        bot_bar.pack(fill="x", pady=(14, 0))

        self.gumb(bot_bar, self.t("delete_selected"), self.obrisi_proizvod, "danger").pack(side="left", padx=(0, 8))
        self.gumb(bot_bar, self.t("delete_expired"), self.obrisi_istekle, "warning").pack(side="left", padx=(0, 8))
        self.gumb(bot_bar, self.t("restore_deleted"), self.vrati_izbrisano, "secondary").pack(side="left")

        self.gumb(bot_bar, self.t("export_excel"), self.izvezi_u_excel, "success").pack(side="right", padx=(8, 0))
        self.gumb(bot_bar, self.t("import_excel"), self.uvezi_iz_excela, "secondary").pack(side="right")

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label=self.t("menu_open_receipt"), command=lambda: self.otvori_doc(9))
        self.menu.add_command(label=self.t("menu_open_warranty"), command=lambda: self.otvori_doc(10))
        self.menu.add_separator()
        self.menu.add_command(label=self.t("menu_service_history"), command=self.otvori_servis)
        self.menu.add_command(label=self.t("menu_edit_product"), command=self.uredi_proizvod)

    def obnovi_sucelje(self):
        spremljeni_unosi = {}
        if hasattr(self, "unos_vars"):
            spremljeni_unosi = {k: v.get() for k, v in self.unos_vars.items()}
        spremljena_pretraga = self.var_pretraga.get() if hasattr(self, "var_pretraga") else ""
        spremljen_orig = self.putanja_orig_racun.get()
        spremljeno_jamstvo = self.putanja_prod_jamstvo.get()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.postavi_stilove()
        self.root.title(self.t("app_title"))
        self.kreiraj_sucelje()

        for k, vrijednost in spremljeni_unosi.items():
            if k in self.unos_vars:
                self.unos_vars[k].set(vrijednost)
        self.putanja_orig_racun.set(spremljen_orig)
        self.putanja_prod_jamstvo.set(spremljeno_jamstvo)
        self.var_pretraga.set(spremljena_pretraga)
        self.osvjezi_tablicu_i_statistiku()

    def promijeni_jezik(self, _event=None):
        novi_jezik = JEZICI_PO_NAZIVU.get(self.var_jezik.get(), self.jezik)
        if novi_jezik == self.jezik:
            return
        self.jezik = novi_jezik
        self.spremi_postavke()
        self.obnovi_sucelje()

    def promijeni_temu(self, _event=None):
        nova_tema = self.var_tema.get()
        if nova_tema not in ("light", "dark") or nova_tema == self.tema:
            return
        self.tema = nova_tema
        self.dark_mode = self.tema == "dark"
        self.spremi_postavke()
        self.obnovi_sucelje()

    def prilagodi_sirine_stupaca(self, event=None):
        if not hasattr(self, "tree") or not hasattr(self, "osnovne_sirine_stupaca"):
            return

        dostupno = event.width if event else self.tree.winfo_width()
        dostupno = max(240, dostupno - 4)
        if abs(dostupno - self._zadnja_sirina_tablice) < 3:
            return
        self._zadnja_sirina_tablice = dostupno

        vidljivi_stupci = [s for s in STUPCI if s != "ID"]
        osnovno_ukupno = sum(self.osnovne_sirine_stupaca[s] for s in vidljivi_stupci)
        min_ukupno = sum(self.min_sirine_stupaca[s] for s in vidljivi_stupci)

        if dostupno >= osnovno_ukupno:
            faktor = dostupno / osnovno_ukupno
            sirine = {s: int(self.osnovne_sirine_stupaca[s] * faktor) for s in vidljivi_stupci}
        elif dostupno >= min_ukupno:
            dodatno = dostupno - min_ukupno
            fleksibilno = sum(self.osnovne_sirine_stupaca[s] - self.min_sirine_stupaca[s] for s in vidljivi_stupci)
            sirine = {}
            for s in vidljivi_stupci:
                udio = (self.osnovne_sirine_stupaca[s] - self.min_sirine_stupaca[s]) / fleksibilno
                sirine[s] = int(self.min_sirine_stupaca[s] + dodatno * udio)
        else:
            faktor = dostupno / min_ukupno
            sirine = {s: max(32, int(self.min_sirine_stupaca[s] * faktor)) for s in vidljivi_stupci}

        razlika = dostupno - sum(sirine.values())
        if razlika:
            sirine["Naziv Proizvoda"] = max(32, sirine["Naziv Proizvoda"] + razlika)

        self.tree.column("ID", width=0, minwidth=0, stretch=False)
        for s in vidljivi_stupci:
            self.tree.column(s, width=max(32, sirine[s]), stretch=False)

    # --- FUNKCIJA OČISTI UNOS ---

    def ocisti_unos(self):
        for var in self.unos_vars.values(): var.set("")
        self.putanja_orig_racun.set("")
        self.putanja_prod_jamstvo.set("")

    # --- PRAVI OCR LOGIKA ---

    def pravi_ocr_izbornik(self):
        putanja = filedialog.askopenfilename(title=self.t("select_receipt_image"), filetypes=[(self.t("filetype_images"), "*.png *.jpg *.jpeg *.bmp")])
        if not putanja: return

        try:
            import pytesseract
            from PIL import Image

            slika = Image.open(putanja)
            messagebox.showinfo(self.t("loading_title"), self.t("loading_ocr"))

            očitani_tekst = pytesseract.image_to_string(slika)

            datum_match = re.search(r'\d{2}[./]\d{2}[./]\d{4}', očitani_tekst)
            prepoznat_datum = datum_match.group(0).replace('/', '.') if datum_match else ""

            cijene = re.findall(r'\d+[,.]\d{2}', očitani_tekst)
            prepoznata_cijena = cijene[-1] if cijene else ""

            win = tk.Toplevel(self.root)
            self.stiliziraj_prozor(win, self.t("ocr_window_title"), "640x650")

            self.labela(win, self.t("ocr_raw_text_label"), bg=self.boje["bg"], fg=self.boje["text"], font=('Segoe UI', 10, 'bold')).pack(anchor="w", padx=20, pady=(16, 6))

            txt_okvir = tk.Text(win, height=15, bg=self.boje["panel"], fg=self.boje["text"], insertbackground=self.boje["text"], relief="flat", bd=1, highlightbackground=self.boje["border"], highlightthickness=1)
            txt_okvir.pack(fill="both", expand=True, padx=20)
            txt_okvir.insert("1.0", očitani_tekst)

            self.labela(win, self.t("ocr_detected_label"), bg=self.boje["bg"], fg=self.boje["text"], font=('Segoe UI', 10, 'bold')).pack(anchor="w", padx=20, pady=(14, 8))

            okvir_podataka = tk.Frame(win, bg=self.boje["bg"])
            okvir_podataka.pack(fill="x", padx=20)

            self.labela(okvir_podataka, f"{self.t('date')}:", bg=self.boje["bg"]).pack(side="left")
            unos_datum = ttk.Entry(okvir_podataka, width=15)
            unos_datum.pack(side="left", padx=10)
            unos_datum.insert(0, prepoznat_datum)

            self.labela(okvir_podataka, f"{self.t('amount')}:", bg=self.boje["bg"]).pack(side="left", padx=(15, 0))
            unos_cijena = ttk.Entry(okvir_podataka, width=15)
            unos_cijena.pack(side="left", padx=10)
            unos_cijena.insert(0, prepoznata_cijena)

            def prebaci_podatke():
                self.unos_vars["Datum Kupovine"].set(unos_datum.get())
                self.unos_vars["Cijena (€)"].set(unos_cijena.get())
                self.putanja_orig_racun.set(putanja)
                win.destroy()
                messagebox.showinfo(self.t("transferred_title"), self.t("transferred_msg"))

            self.gumb(win, self.t("keep_ocr_data"), prebaci_podatke, "primary").pack(pady=20)

        except ImportError:
            messagebox.showerror(self.t("missing_module_title"), self.t("missing_module_msg"))
        except Exception as e:
            messagebox.showerror(self.t("ocr_error_title"), self.t("ocr_error_msg", error=e))

    # --- OSTATAK LOGIKE ---

    def postavi_filter(self, tip):
        self.trenutni_filter = tip
        self.osvjezi_tablicu_i_statistiku()

    def primijeni_pretragu(self, *args):
        self.osvjezi_tablicu_i_statistiku()

    def obrisi_istekle(self):
        istekli = [r for r in self.svi_podaci if self.je_li_isteklo(r[8])]
        if not istekli: return

        if messagebox.askyesno(self.t("delete_title"), self.t("delete_expired_confirm", count=len(istekli))):
            self.povijest_brisanja.append(istekli)
            self.svi_podaci = [r for r in self.svi_podaci if not self.je_li_isteklo(r[8])]
            self.spremi_sve_u_bazu()
            self.osvjezi_tablicu_i_statistiku()

    def odaberi_doc(self, var):
        p = filedialog.askopenfilename()
        if p: var.set(p)

    def spremi_novi(self):
        v = {k: var.get().strip() for k, var in self.unos_vars.items()}
        if not v["Naziv Proizvoda"]:
            messagebox.showwarning(self.t("required_title"), self.t("required_product"))
            return

        p_id = str(uuid.uuid4())[:8]
        istek = self.izracunaj_istek(v["Datum Kupovine"], v["Trajanje Garancije (god)"])
        final_orig = self.kopiraj_datoteku(self.putanja_orig_racun.get(), f"Racun_{p_id}")
        final_prod = self.kopiraj_datoteku(self.putanja_prod_jamstvo.get(), f"Jamstvo_{p_id}")

        novi = [p_id, v["Trgovina"], v["Broj Računa"], v["Naziv Proizvoda"], v["Šifra"],
                v["Cijena (€)"], v["Datum Kupovine"], v["Trajanje Garancije (god)"], istek, final_orig, final_prod]

        self.svi_podaci.append(novi)
        self.spremi_sve_u_bazu()
        self.osvjezi_tablicu_i_statistiku()
        self.ocisti_unos()

    def kopiraj_datoteku(self, putanja, prefiks):
        if not putanja or not os.path.exists(putanja): return ""
        nova = os.path.join(DOKUMENTI_MAPA, f"{prefiks}{os.path.splitext(putanja)[1]}")
        shutil.copy2(putanja, nova)
        return os.path.relpath(nova, BAZNA_MAPA)

    def kopiraj_mapu_dokumenata(self, ciljna_mapa):
        if not os.path.isdir(DOKUMENTI_MAPA):
            return ""

        cilj = os.path.join(ciljna_mapa, "dokumenti_garancija")
        if os.path.abspath(cilj) != os.path.abspath(DOKUMENTI_MAPA):
            shutil.copytree(DOKUMENTI_MAPA, cilj, dirs_exist_ok=True)
        return cilj

    def ocisti_import_vrijednost(self, vrijednost):
        if vrijednost is None:
            return ""
        try:
            if pd.isna(vrijednost):
                return ""
        except (TypeError, ValueError):
            pass
        if isinstance(vrijednost, datetime):
            return vrijednost.strftime("%d.%m.%Y")
        if isinstance(vrijednost, float) and vrijednost.is_integer():
            return str(int(vrijednost))
        tekst = str(vrijednost).strip()
        return "" if tekst.lower() in ("nan", "nat", "none") else tekst

    def normaliziraj_import_putanju(self, putanja):
        putanja = self.ocisti_import_vrijednost(putanja)
        if not putanja:
            return ""
        if os.path.isabs(putanja):
            return putanja
        return os.path.normpath(putanja.replace("\\", os.sep).replace("/", os.sep))

    def naziv_datoteke_iz_putanje(self, putanja):
        return os.path.basename(str(putanja).replace("\\", "/"))

    def kandidati_za_import_dokument(self, spremljena_putanja, mapa_uvoza):
        putanja = self.normaliziraj_import_putanju(spremljena_putanja)
        if not putanja:
            return []

        kandidati = []
        if os.path.isabs(putanja):
            kandidati.append(putanja)
        else:
            kandidati.extend([
                os.path.join(mapa_uvoza, putanja),
                os.path.join(BAZNA_MAPA, putanja),
            ])

        naziv = self.naziv_datoteke_iz_putanje(putanja)
        if naziv:
            kandidati.extend([
                os.path.join(mapa_uvoza, "dokumenti_garancija", naziv),
                os.path.join(DOKUMENTI_MAPA, naziv),
            ])

        jedinstveni = []
        vidjeni = set()
        for kandidat in kandidati:
            aps = os.path.abspath(kandidat)
            if aps not in vidjeni:
                vidjeni.add(aps)
                jedinstveni.append(kandidat)
        return jedinstveni

    def pronadi_import_dokument(self, spremljena_putanja, mapa_uvoza):
        for kandidat in self.kandidati_za_import_dokument(spremljena_putanja, mapa_uvoza):
            if os.path.isfile(kandidat):
                return kandidat
        return ""

    def uvezi_dokument_iz_backupa(self, spremljena_putanja, mapa_uvoza, p_id, prefiks):
        putanja = self.normaliziraj_import_putanju(spremljena_putanja)
        if not putanja:
            return "", False, False

        izvor = self.pronadi_import_dokument(putanja, mapa_uvoza)
        if not izvor:
            return putanja, False, True

        ekstenzija = os.path.splitext(izvor)[1] or os.path.splitext(putanja)[1]
        odrediste = os.path.join(DOKUMENTI_MAPA, f"{prefiks}_{p_id}{ekstenzija}")
        os.makedirs(DOKUMENTI_MAPA, exist_ok=True)
        if os.path.abspath(izvor) != os.path.abspath(odrediste):
            shutil.copy2(izvor, odrediste)
        return os.path.relpath(odrediste, BAZNA_MAPA), True, False

    def redak_iz_importa(self, red, mapa_uvoza):
        vrijednosti = {stupac: self.ocisti_import_vrijednost(red.get(stupac, "")) for stupac in STUPCI}
        p_id = vrijednosti["ID"] or str(uuid.uuid4())[:8]

        racun, racun_vracen, racun_nedostaje = self.uvezi_dokument_iz_backupa(
            vrijednosti["Originalni Račun"], mapa_uvoza, p_id, "Racun"
        )
        jamstvo, jamstvo_vraceno, jamstvo_nedostaje = self.uvezi_dokument_iz_backupa(
            vrijednosti["Produljeno Jamstvo"], mapa_uvoza, p_id, "Jamstvo"
        )

        istek = vrijednosti["Datum Isteka Garancije"]
        if not istek:
            istek = self.izracunaj_istek(vrijednosti["Datum Kupovine"], vrijednosti["Trajanje Garancije (god)"])

        novi = [
            p_id,
            vrijednosti["Trgovina"],
            vrijednosti["Broj Računa"],
            vrijednosti["Naziv Proizvoda"],
            vrijednosti["Šifra"],
            vrijednosti["Cijena (€)"],
            vrijednosti["Datum Kupovine"],
            vrijednosti["Trajanje Garancije (god)"],
            istek,
            racun,
            jamstvo,
        ]
        vraceno = int(racun_vracen) + int(jamstvo_vraceno)
        nedostaje = int(racun_nedostaje) + int(jamstvo_nedostaje)
        return novi, vraceno, nedostaje

    def uvezi_servise_iz_backupa(self, mapa_uvoza):
        servis_backup = os.path.join(mapa_uvoza, "servisi_log.json")
        if not os.path.isfile(servis_backup):
            return
        servisni_podaci = self.ucitaj_servise_iz_json_datoteke(servis_backup)
        if not servisni_podaci:
            return
        for p_id, zapisi in servisni_podaci.items():
            if isinstance(zapisi, list):
                self.servisi_podaci[p_id] = zapisi
        self.spremi_sve_servise_u_bazu()

    def puna_putanja_dokumenta(self, putanja):
        if not putanja:
            return ""
        if os.path.isabs(putanja):
            return putanja
        return os.path.join(BAZNA_MAPA, putanja)

    def osvjezi_tablicu_i_statistiku(self, podaci=None):
        if podaci is None: podaci = self.svi_podaci
        for r in self.tree.get_children(): self.tree.delete(r)

        c = self.boje
        aktivno, isteklo = 0, 0
        upit = self.var_pretraga.get().lower()

        for red in podaci:
            status = "isteklo" if self.je_li_isteklo(red[8]) else "vrijedi"
            if status == "vrijedi": aktivno += 1
            else: isteklo += 1

            if upit and not any(upit in str(v).lower() for v in red): continue
            if self.trenutni_filter == "AKTIVNI" and status != "vrijedi": continue
            if self.trenutni_filter == "ISTEKLI" and status != "isteklo": continue

            prikaz = list(red)
            prikaz[9] = self.t("doc_receipt") if red[9] else ""
            prikaz[10] = self.t("doc_warranty") if red[10] else ""
            self.tree.insert("", "end", values=prikaz, tags=(status,))

        self.tree.tag_configure("vrijedi", background=c["row_ok"], foreground=c["row_ok_text"])
        self.tree.tag_configure("isteklo", background=c["row_expired"], foreground=c["row_expired_text"])

        self.lbl_stat_ukupno.config(text=self.t("total_fmt", count=len(self.svi_podaci)))
        self.lbl_stat_aktivno.config(text=self.t("active_fmt", count=aktivno))
        self.lbl_stat_isteklo.config(text=self.t("expired_fmt", count=isteklo))

        self.lbl_stat_ukupno.config(
            bg=c["secondary"] if self.trenutni_filter == "SVI" else c["panel_alt"],
            fg="#ffffff" if self.trenutni_filter == "SVI" else c["text"],
        )
        self.lbl_stat_aktivno.config(
            bg=c["success"] if self.trenutni_filter == "AKTIVNI" else c["panel_alt"],
            fg="#ffffff" if self.trenutni_filter == "AKTIVNI" else c["text"],
        )
        self.lbl_stat_isteklo.config(
            bg=c["danger"] if self.trenutni_filter == "ISTEKLI" else c["panel_alt"],
            fg="#ffffff" if self.trenutni_filter == "ISTEKLI" else c["text"],
        )

    def prikazi_meni(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def dvostruki_klik_otvori(self, event):
        sel = self.tree.selection()
        if not sel: return
        p_id = self.tree.item(sel[0], "values")[0]
        for r in self.svi_podaci:
            if r[0] == p_id:
                racun = self.puna_putanja_dokumenta(r[9])
                jamstvo = self.puna_putanja_dokumenta(r[10])
                if racun and os.path.exists(racun): self.pokreni_datoteku(racun)
                elif jamstvo and os.path.exists(jamstvo): self.pokreni_datoteku(jamstvo)
                break

    def otvori_doc(self, idx):
        sel = self.tree.selection()
        if not sel: return
        p_id = self.tree.item(sel[0], "values")[0]
        for r in self.svi_podaci:
            if r[0] == p_id:
                putanja = self.puna_putanja_dokumenta(r[idx])
                if putanja and os.path.exists(putanja): self.pokreni_datoteku(putanja)
                else: messagebox.showinfo(self.t("doc_missing_title"), self.t("doc_missing"))
                break

    def pokreni_datoteku(self, putanja):
        if platform.system() == "Windows": os.startfile(putanja)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", putanja])

    def dodaj_dokument_naknadno(self, idx):
        sel = self.tree.selection()
        if not sel: return
        p = filedialog.askopenfilename()
        if p:
            p_id = self.tree.item(sel[0], "values")[0]
            prefiks = "Racun_" if idx == 9 else "Jamstvo_"
            nova = self.kopiraj_datoteku(p, f"{prefiks}{p_id}")
            for r in self.svi_podaci:
                if r[0] == p_id: r[idx] = nova
            self.spremi_sve_u_bazu()
            self.osvjezi_tablicu_i_statistiku()

    def obrisi_proizvod(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno(self.t("delete_title"), self.t("delete_selected_confirm")):
            za_brisanje_id = [self.tree.item(i, "values")[0] for i in sel]
            obrisani = [r for r in self.svi_podaci if r[0] in za_brisanje_id]
            if obrisani:
                self.povijest_brisanja.append(obrisani)
                self.svi_podaci = [r for r in self.svi_podaci if r[0] not in za_brisanje_id]
                self.spremi_sve_u_bazu()
                self.osvjezi_tablicu_i_statistiku()

    def vrati_izbrisano(self):
        if not self.povijest_brisanja: return
        zadnje = self.povijest_brisanja.pop()
        self.svi_podaci.extend(zadnje)
        self.spremi_sve_u_bazu()
        self.osvjezi_tablicu_i_statistiku()

    def uredi_proizvod(self):
        sel = self.tree.selection()
        if not sel: return
        p_id = self.tree.item(sel[0], "values")[0]
        for r in self.svi_podaci:
            if r[0] == p_id:
                edit_win = tk.Toplevel(self.root)
                self.stiliziraj_prozor(edit_win, self.t("edit_title"), "460x560")
                body = tk.Frame(edit_win, bg=self.boje["bg"])
                body.pack(fill="both", expand=True, padx=24, pady=18)
                nove_v = {}
                for i, s in enumerate(STUPCI[1:-2], 1):
                    self.labela(body, self.naziv_stupca(s), bg=self.boje["bg"], fg=self.boje["muted"], font=('Segoe UI', 9, 'bold')).pack(anchor="w", pady=(8, 2))
                    v = tk.StringVar(value=r[i])
                    ttk.Entry(body, textvariable=v).pack(fill="x", ipady=4)
                    nove_v[s] = v
                def spasi():
                    r[1:9] = [nove_v[s].get() for s in STUPCI[1:-2]]
                    r[8] = self.izracunaj_istek(r[6], r[7])
                    self.spremi_sve_u_bazu()
                    self.osvjezi_tablicu_i_statistiku()
                    edit_win.destroy()
                self.gumb(body, self.t("save"), spasi, "primary").pack(fill="x", pady=(18, 0))
                break

    def otvori_servis(self):
        sel = self.tree.selection()
        if not sel: return
        p_id = self.tree.item(sel[0], "values")[0]
        sw = tk.Toplevel(self.root)
        self.stiliziraj_prozor(sw, self.t("service_title"), "480x420")
        body = tk.Frame(sw, bg=self.boje["bg"])
        body.pack(fill="both", expand=True, padx=20, pady=18)
        self.labela(body, self.t("recorded_repairs"), bg=self.boje["bg"], fg=self.boje["text"], font=('Segoe UI', 11, 'bold')).pack(anchor="w", pady=(0, 8))
        lb = tk.Listbox(body, bg=self.boje["panel"], fg=self.boje["text"], selectbackground=self.boje["accent_dark"], selectforeground="#ffffff", relief="flat", highlightbackground=self.boje["border"], highlightthickness=1)
        lb.pack(fill="both", expand=True)
        for s in self.servisi_podaci.get(p_id, []): lb.insert("end", f"[{s['datum']}] {s['opis']}")
        en = ttk.Entry(body)
        en.pack(fill="x", pady=(10, 8), ipady=4)
        def dodaj():
            if en.get():
                z = {"datum": datetime.now().strftime("%d.%m.%Y"), "opis": en.get()}
                self.servisi_podaci.setdefault(p_id, []).append(z)
                lb.insert("end", f"[{z['datum']}] {z['opis']}")
                self.spremi_servis_u_bazu(p_id, z)
                en.delete(0, 'end')
        self.gumb(body, self.t("add_service"), dodaj, "primary").pack(fill="x")

    def izvezi_u_excel(self):
        if not self.svi_podaci: return
        putanja = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[(self.t("filetype_excel"), "*.xlsx")], initialfile="Garancije_Eksport.xlsx")
        if putanja:
            pd.DataFrame(self.svi_podaci, columns=STUPCI).to_excel(putanja, index=False)
            dokumenti_backup = self.kopiraj_mapu_dokumenata(os.path.dirname(putanja))
            if dokumenti_backup:
                messagebox.showinfo(self.t("export_title"), self.t("export_success_with_docs", path=dokumenti_backup))
            else:
                messagebox.showinfo(self.t("export_title"), self.t("export_success"))

    def uvezi_iz_excela(self):
        p = filedialog.askopenfilename(filetypes=[(self.t("filetype_excel_csv"), "*.xlsx *.csv")])
        if not p: return
        try:
            df = pd.read_excel(p) if p.lower().endswith('.xlsx') else pd.read_csv(p)
            mapa_uvoza = os.path.dirname(os.path.abspath(p))
            indeks_po_id = {r[0]: i for i, r in enumerate(self.svi_podaci) if r[0]}
            broj_zapisa = 0
            vraceni_dokumenti = 0
            dokumenti_nedostaju = 0

            for _, red in df.iterrows():
                novi, vraceno, nedostaje = self.redak_iz_importa(red, mapa_uvoza)
                if not any(novi[i] for i in [1, 2, 3, 4, 5, 6, 7, 9, 10]):
                    continue

                postojeci_idx = indeks_po_id.get(novi[0])
                if postojeci_idx is None:
                    indeks_po_id[novi[0]] = len(self.svi_podaci)
                    self.svi_podaci.append(novi)
                else:
                    stari = self.svi_podaci[postojeci_idx]
                    if not novi[9] and stari[9]:
                        novi[9] = stari[9]
                    if not novi[10] and stari[10]:
                        novi[10] = stari[10]
                    self.svi_podaci[postojeci_idx] = novi

                broj_zapisa += 1
                vraceni_dokumenti += vraceno
                dokumenti_nedostaju += nedostaje

            self.uvezi_servise_iz_backupa(mapa_uvoza)
            self.spremi_sve_u_bazu()
            self.osvjezi_tablicu_i_statistiku()
            messagebox.showinfo(
                self.t("import_title"),
                self.t("import_success", records=broj_zapisa, docs=vraceni_dokumenti, missing=dokumenti_nedostaju)
            )
        except Exception as e: messagebox.showerror(self.t("error_title"), str(e))

    def napravi_rucni_backup(self):
        target = filedialog.askdirectory(title=self.t("backup_select_title"))
        if not target: return

        try:
            datum = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir = os.path.join(target, f"Garancije_Backup_{datum}")
            os.makedirs(backup_dir)

            if os.path.exists(DATABASE_DATOTEKA):
                self.napravi_backup_baze(os.path.join(backup_dir, "garancije.db"))
            self.izvezi_podatke_u_csv(os.path.join(backup_dir, "moje_garancije.csv"))
            self.izvezi_servise_u_json(os.path.join(backup_dir, "servisi_log.json"))
            if os.path.exists(DOKUMENTI_MAPA):
                self.kopiraj_mapu_dokumenata(backup_dir)

            messagebox.showinfo(self.t("backup_success_title"), self.t("backup_success", path=backup_dir))
        except Exception as e:
            messagebox.showerror(self.t("error_title"), self.t("backup_error", error=e))

    def izvezi_podatke_u_csv(self, putanja):
        with open(putanja, mode='w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(STUPCI); w.writerows(self.svi_podaci)

    def izvezi_servise_u_json(self, putanja):
        with open(putanja, 'w', encoding='utf-8') as f:
            json.dump(self.servisi_podaci, f, ensure_ascii=False, indent=2)

    def izracunaj_istek(self, d, t):
        try:
            dt = datetime.strptime(d, "%d.%m.%Y")
            return dt.replace(year=dt.year + int(t)).strftime("%d.%m.%Y")
        except: return "N/A"

    def je_li_isteklo(self, d):
        try: return datetime.strptime(d, "%d.%m.%Y") < datetime.now()
        except: return False

    def prebaci_temu(self):
        self.tema = "light" if self.dark_mode else "dark"
        self.dark_mode = self.tema == "dark"
        self.spremi_postavke()
        self.obnovi_sucelje()

    def sortiraj(self, col):
        idx = STUPCI.index(col)
        self.svi_podaci.sort(key=lambda x: x[idx].lower() if isinstance(x[idx], str) else x[idx])
        self.osvjezi_tablicu_i_statistiku()

if __name__ == "__main__":
    root = tk.Tk()
    app = GarancijeApp(root)
    root.mainloop()
