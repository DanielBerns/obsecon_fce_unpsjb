from typing import Dict

from components.configuration import CLI
from components.core import create_application, show
from components.precios_claros import Actions

import pdb

def get_arguments() -> Dict[str, str]:
    cli = CLI()
    cli.add_arguments(
        "-d",
        "--dotenv",
        type=str,
        default=".env",
        required=False,
        help="name of dotenv file",
    )
    cli.add_arguments(
        "-m",
        "--mode",
        choices=["dev", "test", "live"],
        type=str,
        default="live",
        required=False,
        help="how to run? dev, test or live",
    )
    cli.add_arguments(
        "-s",
        "--sample",
        type=str,
        default="20240217183349",
        required=False,
        help="sample key is a timestamp",
    )
    return cli.arguments

    
def main() -> None:
    application_name: str = "run_precios_claros_download"
    arguments = get_arguments()

    with create_application(application_name, arguments) as application:
        show(f"{application_name:s} 1")
        sample_key = arguments["sample"]
        report_key = "dev"
        Actions.report_sample(application, sample_key, report_key)
        show(f"{application_name:s} 2")


if __name__ == "__main__":
    main()
