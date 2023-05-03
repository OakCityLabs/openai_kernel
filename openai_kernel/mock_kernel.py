from unittest.mock import MagicMock

import requests
from openai.error import AuthenticationError
from openai.openai_object import OpenAIObject

from .kernel import OpenAIKernel


class MockOpenAIKernel(OpenAIKernel):
    """
    A kernel with a mock implementation of the OpenAI library.
    Install with `python -m openai_kernel.mock_kernel install`
    """

    app_name = "mock_openai_kernel"

    def __init__(self, *args, **kwargs):
        super(MockOpenAIKernel, self).__init__(*args, **kwargs)
        self.kernel_json = {
            "argv": [
                "python",
                "-m",
                "openai_kernel.mock_kernel",
                "-f",
                "{connection_file}",
            ],
            "display_name": "MockOpenAI",
            "language": "mock_openai",
            "name": "mock_openai",
        }

        mock_openai = MagicMock()
        mock_openai.api_key = None
        mock_openai.api_key_path = None

        def chat_completion_create(model, messages, **kwargs):
            content = messages[-1]["content"]

            if "no_api_key" in content:
                raise AuthenticationError("No API key provided, please set it")
            elif "connection_error" in content:
                raise requests.exceptions.ConnectionError()

            openai_msg = f"you said '{content}'"
            openai_resp = OpenAIObject.construct_from(
                {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "index": 0,
                            "message": {"content": openai_msg, "role": "assistant"},
                        }
                    ],
                    "created": 1682546524,
                    "id": "chatcmpl-79hV6JNgzMPhWx4cQgcr7j853bTIn",
                    "model": "gpt-3.5-turbo-0301",
                    "object": "chat.completion",
                    "usage": {
                        "completion_tokens": 9,
                        "prompt_tokens": 18,
                        "total_tokens": 27,
                    },
                }
            )
            return openai_resp

        mock_openai.ChatCompletion.create.side_effect = chat_completion_create

        self.openai = mock_openai


if __name__ == "__main__":
    MockOpenAIKernel.run_as_main()
