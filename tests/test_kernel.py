
import unittest
import jupyter_kernel_test


class OpenAIKernelTests(jupyter_kernel_test.KernelTests):
    kernel_name = "openai"
    language_name = "text"

    def test_openai_no_api_key(self):
        self.flush_channels()
        reply, output_msgs = self.execute_helper(code='its high noon')
        self.assertEqual(output_msgs[0]['header']['msg_type'], 'error')
        self.assertEqual(output_msgs[0]['content']['ename'], "<class 'openai.error.AuthenticationError'>")
        assert output_msgs[0]['content']['evalue'].startswith("No API key provided")
        assert output_msgs[0]['content']['traceback'][0].startswith("No OpenAI API key provided, set your API key by using the 'magic' commands '%api_key API_KEY' or '%api_key_path PATH_TO_API_KEY', creating a .openai_api_key file in your home directory, or by setting the OPENAI_API_KEY or OPENAI_API_KEY_PATH environment variables")

    def test_openai_set_api_key_magic(self):
        """Set API key path using line magic, setting api key using magic clear api_key_path"""
        self.flush_channels()
        reply, output_msgs = self.execute_helper(code='%api_key_path /path/to/sekrit')
        reply, output_msgs = self.execute_helper(code='%get api_key_path')
        self.assertEqual(output_msgs[0]['header']['msg_type'], 'execute_result')
        self.assertEqual(output_msgs[0]['content']['data']['text/plain'], "'/path/to/sekrit'")
        reply, output_msgs = self.execute_helper(code='%get api_key')
        self.assertEqual(reply['header']['msg_type'], 'execute_reply')
        self.assertEqual(reply['content']['status'], 'ok')
        assert len(output_msgs) == 0

        reply, output_msgs = self.execute_helper(code='%api_key bother')

        reply, output_msgs = self.execute_helper(code='%get api_key')
        self.assertEqual(output_msgs[0]['header']['msg_type'], 'execute_result')
        self.assertEqual(output_msgs[0]['content']['data']['text/plain'], "'bother'")
        reply, output_msgs = self.execute_helper(code='%get api_key_path')
        self.assertEqual(reply['header']['msg_type'], 'execute_reply')
        self.assertEqual(reply['content']['status'], 'ok')
        assert len(output_msgs) == 0

    def test_openai_set_variable(self):
        """Set a variable with the overridden set line magic"""
        reply, output_msgs = self.execute_helper(code='%get system_prompt')
        self.assertEqual(output_msgs[0]['header']['msg_type'], 'execute_result')
        self.assertEqual(output_msgs[0]['content']['data']['text/plain'], "'You are a helpful assistant.'")
        reply, output_msgs = self.execute_helper(code='%set system_prompt aliens have taken over earth')
        reply, output_msgs = self.execute_helper(code='%get system_prompt')
        self.assertEqual(output_msgs[0]['header']['msg_type'], 'execute_result')
        self.assertEqual(output_msgs[0]['content']['data']['text/plain'], "'aliens have taken over earth'")


if __name__ == '__main__':
    unittest.main()
