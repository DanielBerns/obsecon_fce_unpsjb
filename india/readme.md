## How to start nlp_news

$ . ~/.venvs/fce/bin/activate
$ python run_nlp_news_start.py -m (test|live)
$ sudo cp supervisord/supervisord.conf /etc/supervisord.conf
$ supervisorctl start run_nlp_news_telegram_bot_(test|live)

