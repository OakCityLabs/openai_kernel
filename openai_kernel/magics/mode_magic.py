from metakernel import Magic


class ModeMagic(Magic):
    def line_mode(self, value):
        """
        %mode MODE - set the mode of this kernel, e.g. chat or image.
        """
        self.kernel.mode = value


def register_magics(kernel):
    kernel.register_magics(ModeMagic)
