from html import (Node,
                  Attribute, 
                  Text,
                  Tag,
                  Block,
                  Processor,
                  )


class AlphaError(Exception):
    pass


def build_attribute(tag: Tag, candidate: Attribute) -> Tag:
    current = tag.attributes.get(candidate.name, None)
    if current:
        raise AlphaError(
            f"attribute included already: {current.render} - {candidate.render}"
        )
    else
        tag.attributes[candidate.name] = candidate
        return tag
            

# <meta charset="UTF-8">
# <meta name="viewport" content="width=device-width, initial-scale=1">
# <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
# <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
# <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">


def build_head(title: str) -> Block:
    block = Block()
    block.add_node(
        Tag("<", "head", ">")
    )
    block.add_node(
        Tag("<", "meta", ">")
        .bind(lambda tag: build_attribute(
                            tag, 
                            Attribute("name", "viewport")
                          )
        )
        .bind(lambda tag: build_attribute(
                            tag, 
                            Attribute("content", "width=device-width, initial-scale=1")
                          )
        )
    )
    block.add_node(Tag("<", "link", ">")
                   .bind(lambda tag: build_attribute(
                            tag, 
                            Attribute("rel", "stylesheet")
                          )
        ))
    block.add_node(Text(title))    
    block.add_node(Tag("</", "head", ">"))    
    return block
    
class DocumentBuilder(DocumentProcessor):
    def __init__(self) -> None:
        document = Document()
        super().__init__(document)

