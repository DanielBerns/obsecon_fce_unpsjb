#!/usr/bin/env bash

cd ~/Apps/observatorio_fce_unpsjb/india/
. ~/.venvs/fce/bin/activate
python run_nlp_news_websites_bot.py -m {{mode}}
deactivate
cd -
