import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


# Configuration for Google AI Studio
STUDIO_AI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta"
STUDIO_AI_MODEL = "gemini-1.5-pro-latest"

def call_studio_ai(prompt, files=None, model_name=None):
    """
    Call Google AI Studio (Gemini API) with comprehensive error handling and file support.
    
    Args:
        prompt (str): The prompt text to send to the AI
        files (list): Optional list of file paths to include in the request
        model_name (str): Optional model name override (defaults to STUDIO_AI_MODEL)
    
    Returns:
        str: The AI response text
    """
    # Input validation
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING] GEMINI_API_KEY not found. Using fallback response for demonstration.")
        return _get_fallback_response(prompt, files)
    
    try:
        client = genai.Client(
            api_key=api_key,
            # The client handles the endpoint URL internally
        )
        
        # Use provided model or default
        model = model_name or STUDIO_AI_MODEL
        
        # Prepare content parts with comprehensive error handling
        parts = [types.Part.from_text(text=prompt)]
        
        # Add file parts if provided
        if files:
            if not isinstance(files, list):
                files = [files]
                
            for file_path in files:
                if not file_path or not isinstance(file_path, str):
                    print(f"[WARNING] Skipping invalid file path: {file_path}")
                    continue
                    
                if not os.path.exists(file_path):
                    print(f"[WARNING] File not found: {file_path}")
                    continue
                
                try:
                    # Check file size (limit to 20MB for safety)
                    file_size = os.path.getsize(file_path)
                    if file_size > 20 * 1024 * 1024:  # 20MB
                        print(f"[WARNING] File too large, skipping: {file_path} ({file_size} bytes)")
                        continue
                    
                    file_lower = file_path.lower()
                    if file_lower.endswith('.pdf'):
                        # For PDF files, read and encode as binary data
                        try:
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            parts.append(types.Part.from_data(
                                data=file_data,
                                mime_type="application/pdf"
                            ))
                            print(f"[INFO] Added PDF file: {file_path}")
                        except Exception as e:
                            print(f"[ERROR] Failed to read PDF file {file_path}: {e}")
                            
                    elif file_lower.endswith('.docx'):
                        # For DOCX files, extract text content using python-docx
                        try:
                            from docx import Document
                            doc = Document(file_path)
                            docx_content = []
                            for paragraph in doc.paragraphs:
                                if paragraph.text.strip():
                                    docx_content.append(paragraph.text)
                            
                            if docx_content:
                                full_content = '\n'.join(docx_content)
                                parts.append(types.Part.from_text(
                                    text=f"\n\nDOCX File: {file_path}\nContent:\n{full_content}"
                                ))
                                print(f"[INFO] Added DOCX file content: {file_path}")
                            else:
                                print(f"[WARNING] DOCX file appears to be empty: {file_path}")
                        except ImportError:
                            print("[ERROR] python-docx not installed. Cannot process DOCX files.")
                        except Exception as e:
                            print(f"[ERROR] Failed to read DOCX file {file_path}: {e}")
                            
                    elif file_lower.endswith(('.txt', '.md')):
                        # For text files, read content
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                file_content = f.read()
                            parts.append(types.Part.from_text(
                                text=f"\n\nFile: {file_path}\nContent:\n{file_content}"
                            ))
                            print(f"[INFO] Added text file: {file_path}")
                        except UnicodeDecodeError:
                            try:
                                with open(file_path, 'r', encoding='latin-1') as f:
                                    file_content = f.read()
                                parts.append(types.Part.from_text(
                                    text=f"\n\nFile: {file_path}\nContent:\n{file_content}"
                                ))
                                print(f"[INFO] Added text file (latin-1 encoding): {file_path}")
                            except Exception as e:
                                print(f"[ERROR] Failed to read text file {file_path}: {e}")
                        except Exception as e:
                            print(f"[ERROR] Failed to read text file {file_path}: {e}")
                    else:
                        print(f"[WARNING] Unsupported file type: {file_path}")
                        
                except OSError as e:
                    print(f"[ERROR] File system error for {file_path}: {e}")
                except Exception as e:
                    print(f"[ERROR] Unexpected error processing file {file_path}: {e}")
        
        contents = [types.Content(role="user", parts=parts)]
        
        # Generate response with error handling
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            
            if response and hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        return candidate.content.parts[0].text
            
            print("[WARNING] No valid response generated from API")
            return _get_fallback_response(prompt, files)
            
        except Exception as api_error:
            print(f"[ERROR] API call failed: {api_error}")
            return _get_fallback_response(prompt, files)
            
    except Exception as e:
        print(f"[ERROR] Failed to initialize AI client: {e}")
        return _get_fallback_response(prompt, files)


def _get_fallback_response(prompt, files=None):
    """
    Provide a fallback response when AI API is unavailable.
    """
    file_info = ""
    if files:
        file_count = len(files) if isinstance(files, list) else 1
        file_info = f" with {file_count} file(s)"
    
    return f"""[SIMULATED AI RESPONSE]
This is a simulated response for demonstration purposes. The actual AI service is unavailable.

Your prompt: "{prompt[:100]}{'...' if len(prompt) > 100 else ''}"
Files provided: {file_info}

For legal analysis and case workflow, this would typically provide:
- Analysis of communication patterns for coercive control indicators
- Summarization of key legal facts and dates
- Bullet-point legal arguments relevant to family law cases
- Metadata extraction from legal documents

To use real AI analysis, set the GEMINI_API_KEY environment variable with your Google AI Studio API key.
"""

def generate():
    """
    Generate content using Google AI Studio with legal case analysis loaded from external file.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[WARNING] GEMINI_API_KEY not found. Cannot generate content.")
        return "API key required for content generation"
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Load legal case analysis from external file
        content_file = "case_content/legal_case_analysis.txt"
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                legal_content = f.read()
        except FileNotFoundError:
            print(f"[ERROR] Legal content file not found: {content_file}")
            return "Legal content file not found"
        except Exception as e:
            print(f"[ERROR] Failed to read legal content: {e}")
            return f"Failed to read legal content: {e}"

        model = "gemini-2.5-pro-preview-tts"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=legal_content),
                ],
            ),
        ]

        # Configuration for content generation
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=2048,
        )

        file_index = 0
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
                file_name = f"ENTER_FILE_NAME_{file_index}"
                file_index += 1
                save_binary_file(file_name, chunk.candidates[0].content.parts[0].inline_data.data)
                print(f"[INFO] Generated file: {file_name}")
            else:
                print(chunk.candidates[0].content.parts[0].text)
                
    except Exception as e:
        print(f"[ERROR] Content generation failed: {e}")
        return f"Content generation failed: {e}"

