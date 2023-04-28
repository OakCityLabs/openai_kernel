from metakernel import Magic


class OpenAIApiMagic(Magic):
    def line_api_key(self, value):
        """
        %api_key API_KEY - set OpenAI API key.
        """
        self.kernel.api_key = value

    def line_api_key_path(self, value):
        """
        %api_key_path API_KEY_PATH - set path to OpenAI API key file.
        """
        self.kernel.api_key_path = value

    def line_organization(self, value):
        """
        %organization ORGANIZATION - set organization for OpenAI API.
        """
        self.kernel.organization = value


def register_magics(kernel):
    kernel.register_magics(OpenAIApiMagic)
