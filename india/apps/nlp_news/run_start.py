import logging

from context import components
from components.core import CLIConfig, Crontab
from nlp_news_app import create_app


def filename():
    return __file__[:-3]


def main() -> None:
    cli_cfg = CLIConfig()   
    cli_cfg.add_arguments()
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg.args) as app:
        print("app created!")
        crontab = Crontab()
        crontab.add("run_news_bots", 
                    str(app.fs.run_news_bots_sh),
                    "58", "*", "*", "*", "*")
        crontab.add("update_app",
                    str(app.fs.update_app_sh),
                    "15", "*", "*", "*", "*")
        # crontab.add("run_pc_sampler_1",
        #             str(app.fs.run_precios_claros_sampler_sh),
        #             "*", "19", "1", "*", "*")
        # crontab.add("run_pc_sampler_2",
        #             str(app.fs.run_precios_claros_sampler_sh),
        #             "*", "19", "15", "*", "*")
        # crontab.add("run_pc_sampler_3",
        #             str(app.fs.run_precios_claros_sampler_sh),
        #             "*", "17", "*", "*", "1")
        # 
        # crontab.add("run_pc_report_sampler_1",
        #             str(app.fs.run_precios_claros_report_sampler_sh),
        #             "*", "23", "1", "*", "*")
        # crontab.add("run_pc_report_sampler_2",
        #             str(app.fs.run_precios_claros_report_sampler_sh),
        #             "*", "23", "15", "*", "*")
        # crontab.add("run_pc_report_sampler_3",
        #             str(app.fs.run_precios_claros_report_sampler_sh),
        #             "*", "23", "*", "*", "1")
        
        crontab.update(app.fs.crontab_txt)


if __name__ == "__main__":
    main()
