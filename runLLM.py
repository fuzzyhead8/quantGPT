from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

def get_strategy(message_txt):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_txt,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # Check if the response includes the expected code block
        response_content = messages.data[0].content[0].text.value
        if '```' in response_content:
            parts = response_content.split('```')
            if len(parts) >= 2:
                comment, code = parts[0], parts[1]
                # Optional: further clean up the code block
                if "python" in code:
                    code = code.split("python", 1)[1].strip()
                return comment.strip(), code.strip()
            else:
                print("Error: Unexpected response format.")
                return response_content, None
        else:
            print("Error: No code block found in the response.")
            return response_content, None
    else:
        print("Run status:", run.status)
        return None, None

def write_strategy(code, comment):
    if code is not None:
        with open("./assistant_files/GeneratedStrategy.py", "w") as f:
            f.write(code)
    else:
        print("No code to write to GeneratedStrategy.py")

    if comment is not None:
        with open("./assistant_files/GeneratedStrategy.txt", "w") as f:
            f.write(comment)
    else:
        print("No comment to write to GeneratedStrategy.txt")
