import os
import json
import sys

from metakernel import MetaKernel
import openai

from .version import __version__


def get_kernel_json():
    """Get the kernel json for the kernel."""
    here = os.path.dirname(__file__)
    default_json_file = os.path.join(here, 'kernel.json')
    json_file = os.environ.get('OPENAI_KERNEL_JSON', default_json_file)
    with open(json_file) as fid:
        data = json.load(fid)
    data['argv'][0] = sys.executable
    return data


def get_api_key():
    api_key = os.environ.get('OPENAI_API_KEY', None)
    return api_key


def get_api_key_path():
    home = os.path.expanduser("~")
    default_api_key_path = os.path.join(home, '.openai_api_key')
    api_key_path = os.environ.get('OPENAI_API_KEY_PATH', default_api_key_path)
    if os.path.exists(api_key_path):
        return api_key_path


class OpenAIKernel(MetaKernel):
    app_name = 'openai_kernel'
    implementation = 'OpenAI Kernel'
    implementation_version = __version__
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "OpenAI Kernel - An interface to OpenAI models"


    def __init__(self, *args, **kwargs):
        super(OpenAIKernel, self).__init__(*args, **kwargs)
        self.kernel_json = get_kernel_json()
        self.initial_system = {"role": "system", "content": "You are a helpful assistant."}
        self._history = []
        self.model = "gpt-3.5-turbo"

        api_key = get_api_key()
        if api_key is not None:
            openai.api_key = api_key
        else:
            api_key_path = get_api_key_path()
            if api_key_path is not None:
                openai.api_key_path = api_key_path

    @property
    def history(self):
        return [self.initial_system] + self._history

    def do_execute_direct(self, code, silent=False):
        msg = {"role": "user", "content": code}
        resp = openai.ChatCompletion.create(model=self.model, messages=self.history + [msg])
        resp_content = resp.choices[0].message.content
        self._history += [msg]
        self._history += [{"role": "assistant", "content": resp_content}]
        return resp_content


if __name__ == '__main__':
    try:
        from ipykernel.kernelapp import IPKernelApp
    except ImportError:
        from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=OpenAIKernel)