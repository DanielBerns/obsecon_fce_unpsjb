#!/usr/bin/env bash

cd ~/Apps/observatorio_fce_unpsjb/india/apps/nlp_news/
. ~/.venvs/fce/bin/activate
python run_websites_bot.py
deactivate
cd -
