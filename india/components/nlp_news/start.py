import logging

from components.core import Crontab
from components.helpers import write_text
from components.core import FromFileTargetTemplate
from components.nlp_news.app import create_app


def filename():
    return __file__[:-3]


def run_start() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        template_builder = FromFileTargetTemplate(app.fs.template_update_repo_sh)
        text = template_builder.template.render()
        write_text(app.fs.update_repo_sh, text)

        template_builder = FromFileTargetTemplate(app.fs.template_run_nlp_news_telegram_bot_sh)
        text = template_builder.template.render(mode=app.cli_args["mode"])
        write_text(app.fs.run_nlp_news_telegram_bot_sh, text)        

        template_builder = FromFileTargetTemplate(app.fs.template_run_nlp_news_websites_bot_sh)
        text = template_builder.template.render(mode=app.cli_args["mode"])
        write_text(app.fs.run_nlp_news_websites_bot_sh, text)        

        crontab = Crontab()
        crontab.add("update_repo",
                    str(app.fs.update_repo_sh),
                    "15", "*", "*", "*", "*")
        crontab.add("run_news_bots", 
                    str(app.fs.run_news_websites_bot_sh),
                    "58", "*", "*", "*", "*")
        crontab.update(app.fs.crontab_txt)
