# observatorio_fce_unpsjb

A repo for supermarket price analysis and download software

Un repo para el software de descarga y análisis de precios en supermercados

# How to install

$ mkdir ~/Apps
$ cd Apps
$ git clone git@github.com:DanielBerns/observatorio_fce_unpsjb.git
$ cd observatorio_fce_unpsjb
$ mkdir ~/.venvs
$ python -m venv ~/.venvs/fce 
$ . ~/.venvs/fce/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt

After installing all the packages succesfully
$ python start.py
$ export COMMAND=~/Apps/observatorio_fce_unpsjb/india/run_news_grabber.sh
$ export COMMAND_TIME=40
$ python edit_crontab.py



# How to start

$ cd ~/Apps/observatorio_fce_unpsjb/india
$ . ~/.venvs/pc/bin/activate
$ python start.py

# How to git

gu.sh

pg.sh
