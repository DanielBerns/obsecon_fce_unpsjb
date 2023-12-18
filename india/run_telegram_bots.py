from pathlib import Path
from components.core import execute_list_of_commands

def main() -> None:
    commands = [
        Path("~/Apps/observatorio_fce_unpsjb/india/run_telegram_webdeprecios_crd.sh"),
        Path("~/Apps/observatorio_fce_unpsjb/india/run_telegram_webdeprecios_rel.sh"),
        Path("~/Apps/observatorio_fce_unpsjb/india/run_telegram_webdeprecios_eqs.sh"),
        Path("~/Apps/observatorio_fce_unpsjb/india/run_telegram_webdeprecios_pmy.sh"),
        Path("~/Apps/observatorio_fce_unpsjb/india/run_telegram_webdeprecios_rty.sh"),        
        ]
    execute_commands(commands)
    
if __name__ == "__main__":
    main()
