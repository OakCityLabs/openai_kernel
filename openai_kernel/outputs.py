class MarkdownOutput:
    def __init__(self, text, markdown=None):
        self.text = text
        self.markdown = markdown if markdown is not None else text

    def _repr_markdown_(self):
        return self.markdown

    def __repr__(self):
        return self.text
