from pathlib import Path 

# identifier = os.environ.get("IDENTIFIER") or "volunteers"
# root_path = Path('~', 'Apps').expanduser()
# data_path = Path(root_path, 'data', identifier)
# secrets_path = Path(root_path, 'secrets', identifier)
# token_file = Path(secrets_path, 'token').with_suffix('.txt')
# update_code_path = Path(os.getcwd()).parent

def get_telegram_token(token_file: Path) -> str:
    if token_file.exists():
        with open(token_file, 'r') as source:
            token = source.read()
        return token.strip()
    else:
        with open(token_file, 'w') as target:
            print(f"You must edit {str(token_file):s} "
                  "and replace the default token "
                  "with a valid telegram token"
                 )
            token = "112358132134"  
            target.write(f"{token:s}\n")
        return token
