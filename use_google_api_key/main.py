import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    model_id = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-lite")

    if not api_key or api_key == "your_api_key_here":
        print("Error: GOOGLE_API_KEY is not set in the .env file.")
        return

    # 2. Read prompt.md
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print("Error: prompt.md file not found.")
        return

    # 3. Initialize Google GenAI Client
    client = genai.Client(api_key=api_key)

    # 4. Call Gemini Model
    print(f"Calling model: {model_id}...")
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_content
        )
        # 5. Output response text
        print("\n--- Response ---")
        print(response.text)
    except Exception as e:
        print(f"An error occurred during the API call: {e}")

if __name__ == "__main__":
    main()
