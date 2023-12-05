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
$ cd india
$ pip install -r requirements.txt

# How to start sshd (Fedora 39)

$ systemctl enable sshd
$ systemctl start sshd
$ systemctl status sshd
$ netstat -ant | grep 22
$ ss -lt

# How to install at
$ dnf -y install at
$ systemctl enable --now atd

# How to git

gu.sh

pg.sh

Write!
