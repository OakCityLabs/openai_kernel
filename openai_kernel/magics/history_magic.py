from metakernel import Magic, option

from openai_kernel.outputs import MarkdownOutput


class HistoryMagic(Magic):
    @option(
        "-r",
        "--raw",
        action="store_true",
        default=False,
        help="Print history in a raw format",
    )
    def line_history(self, raw=False):
        """
        %history - Show OpenAI chat history
        """
        self.retval = self.kernel.history
        self.raw = raw

    def post_process(self, retval):
        if not self.raw:
            markdown = ""
            for msg in self.retval:
                markdown += f"{msg}<br />"
            return MarkdownOutput(str(retval), markdown)
        else:
            return self.retval


def register_magics(kernel):
    kernel.register_magics(HistoryMagic)
