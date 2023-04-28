from metakernel import Magic


class ClearHistoryMagic(Magic):
    def line_clear_history(self):
        """
        %clear_history - Clear OpenAI chat history
        """
        self.kernel.clear_history()


def register_magics(kernel):
    kernel.register_magics(ClearHistoryMagic)
