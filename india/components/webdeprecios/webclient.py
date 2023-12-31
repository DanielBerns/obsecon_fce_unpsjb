import json
from random import choices
from pathlib import Path
from typing import Dict, Tuple, Generator
import logging

import pdb

import requests

from components.helpers import get_container, get_resource, classname

AuthHeaders = requests.structures.CaseInsensitiveDict
Response = requests.Response

# identifier: str = os.environ.get("ATHENA_IDENTIFIER") or "random"
# website: str = os.environ.get("ATHENA_WEBSITE") or "http://127.0.0.1:5000"
# store_path.mkdir(mode=0o700, parents=True, exist_ok=True)
# https://forpythons.com/how-to-upload-file-with-python-requests/


class WebClientException(Exception):
    pass


class WebClient:
    CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789_()-+~"

    STORE = Path("~", "Info", "athena", "agent", "store").expanduser()

    def __init__(self, website: str) -> None:
        self._website: str = website
        self._create_user_url: str = f"{self.website:s}/api/users"
        self._tokens_url: str = f"{self.website:s}/api/tokens"
        self._current_user_url: str = f"{self.website:s}/api/users/current"
        self._all_the_messages_url: str = f"{self.website:s}/api/messages/all"
        self._empty_messages_url: str = f"{self.website:s}/api/messages/empty"
        self._publish_post_url: str = f"{self.website:s}/api/posts"

    def store_path(self, username: str) -> Path:
        return get_container(WebClient.STORE, username)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def website(self) -> str:
        return self._website

    @property
    def create_user_url(self) -> str:
        return self._create_user_url

    @property
    def tokens_url(self) -> str:
        return self._tokens_url

    @property
    def current_user_url(self) -> str:
        return self._current_user_url

    @property
    def all_the_messages_url(self) -> str:
        return self._all_the_messages_url

    @property
    def empty_messages_url(self) -> str:
        return self._empty_messages_url

    @property
    def publish_post_url(self) -> str:
        return self._publish_post_url

    def create_user(self, username: str, password: str) -> Response:
        payload: Dict[str, str] = {"username": username, "password": password}
        response = requests.post(self.create_user_url, json=payload)
        return response

    def login_user(self, username: str, password: str) -> Response:
        return requests.post(
            self.tokens_url, auth=requests.auth.HTTPBasicAuth(username, password)
        )

    def get_current_user(self, auth_headers: AuthHeaders) -> Response:
        return requests.get(self.current_user_url, headers=auth_headers)

    def publish_post(self, auth_headers: AuthHeaders, content: str) -> Response:
        payload = {"content": content}
        response = requests.post(
            self.publish_post_url, headers=auth_headers, json=payload
        )
        return response

    def get_messages(
        self, auth_headers: AuthHeaders
    ) -> Generator[Dict[str, str], None, None]:
        response = requests.get(self.all_the_messages_url, headers=auth_headers)
        if response.status_code >= 400:
            logging.error(
                f"{classname(self):s}.get_messages https status_code {response.status_code:d}"
            )
        else:
            logging.info(
                f"{classname(self):s}.get_messages https status_code {response.status_code:d}"
            )
            as_json = response.json()
            for message in as_json["items"]:
                yield message

    def clear_messages(self, auth_headers: AuthHeaders) -> Response:
        response = requests.get(empty_messages_url, headers=auth_headers)
        return response

    @staticmethod
    def get_token_headers(token: str) -> AuthHeaders:
        auth_headers = AuthHeaders()
        auth_headers["Accept"] = "application/json"
        auth_headers["Authorization"] = f"Bearer {token}"
        return auth_headers

    @staticmethod
    def empty_data(file_identifier: Path) -> Dict[str, str]:
        custom_data = {"username": "", "password": "", "register": ""}
        with open(file_identifier, "w") as target:
            json.dump(custom_data, target)
        return custom_data

    @staticmethod
    def load_credentials(file_identifier: Path) -> Dict[str, str]:
        try:
            with open(file_identifier, "r") as source:
                some_data = json.load(source)
        except FileNotFoundError:
            logging.error(f"{str(file_identifier):s} not found!")
            some_data = empty_data(file_identifier)
        except json.decoder.JSONDecodeError:
            logging.error(f"{str(file_identifier):s} bad json!")
            some_data = empty_data(file_identifier)
        return some_data

    @staticmethod
    def write_data(some_data: Dict[str, str], file_identifier: Path) -> None:
        with open(file_identifier, "w") as target:
            json.dump(some_data, target)

    @staticmethod
    def generate_credentials(credentials_file_identifier: Path) -> Dict[str, str]:
        credentials = {}
        credentials["username"] = "".join(choices(WebClient.CHARACTERS, k=10))
        credentials["password"] = "".join(choices(WebClient.CHARACTERS, k=10))
        credentials["register"] = "yes"
        WebClient.write_data(credentials, credentials_file_identifier)
        return credentials

    @staticmethod
    def get_credentials_fields(credentials: Dict[str, str]) -> Tuple[str, str, str]:
        try:
            username, password, register = (
                credentials["username"],
                credentials["password"],
                credentials["register"],
            )
        except KeyError as message:
            logging.error(f"Error {str(message):s} - {str(credentials):s}")
            username, password, register = "", "", ""
        return username, password, register

    def get_auth_headers(self, username: str) -> AuthHeaders:
        store_path: Path = self.store_path(username)
        credentials_file_identifier = get_resource(store_path, "credentials", ".json")
        if credentials_file_identifier.exists():
            credentials = WebClient.load_credentials(credentials_file_identifier)
        else:
            credentials = WebClient.generate_credentials(credentials_file_identifier)
            credentials["username"] = username
            WebClient.write_data(credentials, credentials_file_identifier)
        username, password, register = WebClient.get_credentials_fields(credentials)
        auth_headers = None
        try:
            if len(username) == 0:
                remark = "username unexpected null value"
                logging.error(remark)
                raise WebClientException(remark)
            if len(password) == 0:
                remark = "password unexpected null value"
                logging.error(remark)
                raise WebClientException(remark)
            if register == "yes":
                logging.info("Registering user")
                response = self.create_user(username, password)
                WebClient.report(response)
                if response.status_code == 200:
                    credentials["user"] = response.json()
                    credentials["register"] = "no"
                    WebClient.write_data(credentials, credentials_file_identifier)
                else:
                    logging.error(f"ERROR: https status_code {response.status_code:d}")
            elif register == "no":
                logging.info("No need to register user")
            else:
                remark = f"register unexpected value {register:s}"
                logging.error(remark)
                raise WebClientException(remark)
        except WebClientException as message:
            logging.error(f"Error: {str(message)}:s")
        else:
            logging.info("Getting authentication token")
            response = self.login_user(username, password)
            WebClient.report(response)
            if response.status_code == 200:
                logging.info("Logged in")
                token_json = response.json()
                token = token_json["token"]
                logging.info(f"Got the token {token:s}")
                auth_headers = WebClient.get_token_headers(token)
        return auth_headers

    @staticmethod
    def report(response: Response) -> None:
        status_code = response.status_code
        text = response.text
        logging.info("status_code", status_code)
        logging.info("*" * 80)
        logging.info(text)
        logging.info("*" * 80)
