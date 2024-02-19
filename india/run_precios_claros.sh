#!/usr/bin/env bash

. ~/.venvs/fce/bin/activate

python run_precios_claros_report_delta.py -m live -r 20231204175645 -c 20231211121751
python run_precios_claros_report_delta.py -m live -r 20231211121751 -c 20231218150359
python run_precios_claros_report_delta.py -m live -r 20231218150359 -c 20231226141145
python run_precios_claros_report_delta.py -m live -r 20231226141145 -c 20240102191924
python run_precios_claros_report_delta.py -m live -r 20240102191924 -c 20240111133430
python run_precios_claros_report_delta.py -m live -r 20240111133430 -c 20240118222908









