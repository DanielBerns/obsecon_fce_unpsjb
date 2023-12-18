#!/usr/bin/env bash

cd ~/Apps/observatorio_fce_unpsjb/india/
. ~/.venvs/fce/bin/activate
python run_telegram_webdeprecios_rty.py -m live
