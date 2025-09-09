import anthropic
import sys
import os
import argparse

# Set the ANTHROPIC_API_KEY environment variable
os.environ["ANTHROPIC_API_KEY"] = "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"

def ask_claude(prompt: str, model: str = "claude-3-5-sonnet-20240620"):
    """
    Sends a prompt to the Claude API and prints the response.

    Args:
        prompt: The question or instruction for Claude.
        model: The model to use (e.g., "claude-3-opus-20240229").
    """
    try:
        # The client automatically looks for the ANTHROPIC_API_KEY environment variable.
        client = anthropic.Anthropic()

        message = client.messages.create(
            model=model,
            max_tokens=4096,  # Increased for longer responses
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # The response is in the first content block.
        response_text = message.content[0].text
        print(response_text)

    except ImportError:
        print("Error: The 'anthropic' library is not installed.")
        print("Please install it using: pip install anthropic")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your ANTHROPIC_API_KEY is set correctly.")


if __name__ == "__main__":
    # The argparse module allows us to easily handle command-line arguments. [1, 3, 8]
    parser = argparse.ArgumentParser(
        description="A command-line interface to ask questions to Anthropic's Claude AI."
    )
    # This defines a required "prompt" argument. [3, 12]
    parser.add_argument("prompt", type=str, help="The prompt or question to send to Claude.")
    
    # This is an optional argument to specify a different model.
    parser.add_argument(
        "--model", 
        type=str, 
        default="claude-3-5-sonnet-20240620", 
        help="The Claude model to use (e.g., 'claude-3-opus-20240229')."
    )

    # Optional argument to include workflow file
    parser.add_argument(
        "--workflow", 
        type=str, 
        default="updated_litigation_workflow.md", 
        help="Path to the workflow markdown file to include in the prompt."
    )

    args = parser.parse_args()
    
    # Check if a prompt was provided.
    if not args.prompt:
        print("Error: No prompt provided. Please provide a question or instruction.")
        # Show the help message and exit.
        parser.print_help()
    else:
        full_prompt = args.prompt
        # Try to read the workflow file
        workflow_path = os.path.join(os.path.dirname(__file__), args.workflow)
        if os.path.exists(workflow_path):
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_content = f.read()
            full_prompt += "\n\nWorkflow Content:\n" + workflow_content
        ask_claude(full_prompt, args.model)
