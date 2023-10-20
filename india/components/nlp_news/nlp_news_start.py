import logging

from components.core import CLIConfig, Crontab
from components.core import FromFileTargetTemplate
from nlp_news_app import create_app


def filename():
    return __file__[:-3]


def nlp_news_start() -> None:
    cli_cfg = CLIConfig()   
    cli_cfg.add_arguments()
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg.args) as app:
        print("app started!")
        template_builder = FromFileTargetTemplate(app.fs.template_update_app_sh)
        text = template_builder.template.render()
        write_text(app.fs.update_app_sh, text)
        crontab = Crontab()
        crontab.add("run_news_bots", 
                    str(app.fs.run_news_bots_sh),
                    "58", "*", "*", "*", "*")
        crontab.add("update_app",
                    str(app.fs.update_app_sh),
                    "15", "*", "*", "*", "*")
        crontab.update(app.fs.crontab_txt)
        print("app stopped!")
