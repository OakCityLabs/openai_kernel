import os
import json
import sys
import traceback
from metakernel import MetaKernel, ExceptionWrapper
import openai
import requests

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


def get_default_api_key_path():
    home = os.path.expanduser("~")
    default_api_key_path = os.path.join(home, '.openai_api_key')
    if os.path.exists(default_api_key_path):
        return default_api_key_path


class OpenAIKernel(MetaKernel):
    app_name = 'openai_kernel'
    implementation = 'OpenAI Kernel'
    implementation_version = __version__
    language_info = {
        'name': 'text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "OpenAI Kernel - An interface to OpenAI models"

    help_suffix = "??"


    def __init__(self, *args, **kwargs):
        self.variables = {
            "system_prompt": "You are a helpful assistant.",
            "model": "gpt-3.5-turbo",
        }
        super(OpenAIKernel, self).__init__(*args, **kwargs)
        self.kernel_json = get_kernel_json()
        self._history = []

        if openai.api_key is None and openai.api_key_path is None:
            default_api_key_path = get_default_api_key_path()
            if default_api_key_path:
                openai.api_key_path = default_api_key_path

    @property
    def api_key(self):
        return openai.api_key

    @api_key.setter
    def api_key(self, key):
        openai.api_key_path = None
        openai.api_key = key

    @property
    def api_key_path(self):
        return openai.api_key_path

    @api_key_path.setter
    def api_key_path(self, path):
        openai.api_key_path = path

    @property
    def history(self):
        return [{"role": "system", "content": self.variables["system_prompt"]}] + self._history
    
    def get_variable(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            return self.variables.get(name, None)
        
    def set_variable(self, name, value):
        if name == "api_key":
            self.api_key = value
        elif name == "api_key_path":
            self.api_key_path = value
        else:
            self.variables[name] = value

    def do_execute_direct(self, code, silent=False):
        msg = {"role": "user", "content": code}
        resp_content = code
        try:
            resp = openai.ChatCompletion.create(model=self.variables["model"], messages=self.history + [msg])
            resp_content = resp.choices[0].message.content
            self._history += [msg]
            self._history += [{"role": "assistant", "content": resp_content}]
        except Exception as e:
            if isinstance(e, openai.error.AuthenticationError):
                if "No API key provided" in e.user_message:
                    message = "No OpenAI API key provided, set your API key by using the 'magic' commands '%api_key API_KEY' or '%api_key_path PATH_TO_API_KEY', creating a .openai_api_key file in your home directory, or by setting the OPENAI_API_KEY or OPENAI_API_KEY_PATH environment variables"
                else:
                    message = e.user_message
                resp_content = ExceptionWrapper(str(type(e)), str(e), [message + "\n"] + traceback.format_tb(e.__traceback__))
            elif isinstance(e, requests.exceptions.ConnectionError):
                message = "Something went wrong communicating with the OpenAI API, please try again"
                resp_content = ExceptionWrapper(str(type(e)), str(e), [message + "\n"] + traceback.format_tb(e.__traceback__))
            else:
                resp_content = ExceptionWrapper(str(type(e)), str(e), [str(type(e))] + traceback.format_tb(e.__traceback__))
        if not silent:
            return resp_content
