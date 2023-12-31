class JSON2CSV:
    def __init__(self, home: Path, label: str) -> None:
        self._container = get_container(home, label)
        self._events_json = JSONDocument(self.container)
        self._rows_csv = CSVDocument(self.container)

    @property
    def container(self) -> Path:
        return self._container

    @property
    def events_json(self) -> JSONDocument:
        return self._events_json

    @property
    def rows_csv(self) -> CSVDocument:
        return self._rows_csv

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def update_events(self, source: JSONSource) -> None:
        self.events_json.update(source)

    def write_csv(self) -> None:
        self.rows_csv.write(self.events_json)


# def csv_to_excel(
#     csv_identifier: Path,
#     excel_identifier: Path) -> None:
#     df = pd.read_csv(csv_identifier, delimiter='|', index_col=None)
#     df.to_excel(excel_identifier)
