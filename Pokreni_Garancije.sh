#!/usr/bin/env bash

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$SCRIPT_DIR" || exit 1

if command -v python3 >/dev/null 2>&1; then
    BASE_PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    BASE_PYTHON="python"
else
    echo "Python nije pronaden. Instalirajte Python 3 i pokrenite skriptu ponovno."
    if [ -t 0 ]; then read -r -p "Pritisnite Enter za izlaz..." _; fi
    exit 1
fi

PYTHON="$BASE_PYTHON"

if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    if ! "$PYTHON" -c "import pandas, openpyxl, PIL, pytesseract" >/dev/null 2>&1; then
        echo "Nedostaju Python paketi. Instaliram u korisnicki Python..."
        if ! "$PYTHON" -m pip install --user --disable-pip-version-check -r "$SCRIPT_DIR/requirements.txt"; then
            echo
            echo "Instalacija paketa nije uspjela."
            if [ -t 0 ]; then read -r -p "Pritisnite Enter za izlaz..." _; fi
            exit 1
        fi
    fi
fi

echo "Pokrecem Garancije..."
"$PYTHON" "$SCRIPT_DIR/garancije.py"
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
    echo
    echo "Program je zavrsio s greskom: $STATUS"
    if [ -t 0 ]; then read -r -p "Pritisnite Enter za izlaz..." _; fi
fi

exit "$STATUS"
