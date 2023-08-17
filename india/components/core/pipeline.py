class Pipeline:
    def __init__(self):
        self._bot: Bot = 
        self._sequence: List[ContentProcessor] = []
        
    def add(self, processor: ContentProcessor) -> None:
        self._sequence.append(processor)

    def processors(self) -> ContentProcessor:
        for this_processor in self.sequence:
            yield this_processor
