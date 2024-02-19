#!/usr/bin/env bash

cd ~/Code/github/DanielBerns/observatorio_fce_unpsjb/india
. ~/.venvs/fce/bin/activate
python run_telegram_webdeprecios_crd.py -m live
