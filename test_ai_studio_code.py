import unittest
from unittest.mock import patch, MagicMock, call, PropertyMock
import os
import sys

# Add the project root to the Python path to allow for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_studio_code import call_studio_ai, STUDIO_AI_MODEL

class TestCallStudioAI(unittest.TestCase):

    def setUp(self):
        """Set up environment variables for tests."""
        self.api_key = "test-api-key"
        os.environ["GEMINI_API_KEY"] = self.api_key

    def tearDown(self):
        """Clean up environment variables after tests."""
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

    @patch('ai_studio_code.genai')
    def test_successful_call(self, mock_genai):
        """Test a successful API call without files."""
        mock_response = MagicMock()
        mock_response.text = "Hello, world!"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model

        prompt = "test prompt"
        response = call_studio_ai(prompt)

        mock_genai.configure.assert_called_once_with(api_key=self.api_key)
        mock_genai.GenerativeModel.assert_called_once_with(model_name=STUDIO_AI_MODEL)
        mock_model.generate_content.assert_called_once_with([prompt])
        self.assertEqual(response, "Hello, world!")

    @patch('ai_studio_code.genai')
    def test_call_with_files(self, mock_genai):
        """Test an API call with file uploads."""
        mock_response = MagicMock()
        mock_response.text = "Response with file."
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model
        
        mock_uploaded_file = MagicMock()
        mock_genai.upload_file.return_value = mock_uploaded_file

        prompt = "test prompt"
        files = ["/fake/path/to/file1.txt", "/fake/path/to/file2.jpg"]
        
        response = call_studio_ai(prompt, files=files)

        mock_genai.configure.assert_called_once_with(api_key=self.api_key)
        mock_genai.GenerativeModel.assert_called_once_with(model_name=STUDIO_AI_MODEL)
        
        upload_calls = [call(path="/fake/path/to/file1.txt"), call(path="/fake/path/to/file2.jpg")]
        mock_genai.upload_file.assert_has_calls(upload_calls)
        
        mock_model.generate_content.assert_called_once_with([prompt, mock_uploaded_file, mock_uploaded_file])
        self.assertEqual(response, "Response with file.")

    def test_missing_api_key(self):
        """Test that a ValueError is raised when the API key is missing."""
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        with self.assertRaises(ValueError) as context:
            call_studio_ai("test prompt")
        self.assertEqual(str(context.exception), "GEMINI_API_KEY environment variable is required")

    @patch('ai_studio_code.genai')
    def test_blocked_response(self, mock_genai):
        """Test handling of a blocked response from the API."""
        mock_response = MagicMock()
        # Mock the .text property to raise a ValueError
        type(mock_response).text = PropertyMock(side_effect=ValueError("No text parts"))
        mock_response.parts = ["Blocked content"]
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        mock_genai.GenerativeModel.return_value = mock_model

        prompt = "a prompt that gets blocked"
        response = call_studio_ai(prompt)

        self.assertEqual(response, "['Blocked content']")

    @patch('ai_studio_code.genai')
    def test_custom_model_name(self, mock_genai):
        """Test that a custom model name is used when provided."""
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Success"
        mock_model.generate_content.return_value = mock_response

        custom_model = "gemini-pro-custom"
        call_studio_ai("test prompt", model_name=custom_model)

        mock_genai.GenerativeModel.assert_called_once_with(model_name=custom_model)

if __name__ == '__main__':
    unittest.main()
