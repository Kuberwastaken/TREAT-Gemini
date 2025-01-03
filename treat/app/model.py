import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Define uncertain response keywords
uncertain_keywords = ["maybe", "unclear", "i don't know", "not sure", "possibly", "could be"]

def analyze_script(script):
    try:
        # Chunk size within token limits for Gemini
        chunk_size = 1000
        # Split the script into chunks
        script_chunks = [script[i:i + chunk_size] for i in range(0, len(script), chunk_size)]
        
        # Define trigger categories
        trigger_categories = [
            "Violence",
            "Death",
            "Substance Use",
            "Gore",
            "Vomit",
            "Sexual Content",
            "Sexual Abuse",
            "Self-Harm",
            "Gun Use",
            "Animal Cruelty",
            "Mental Health Issues"
        ]
        
        # Initialize a set to store identified triggers
        identified_triggers = set()

        # Analyze each chunk separately
        for chunk in script_chunks:
            for category in trigger_categories:
                # Create a more specific and detailed prompt for the model to analyze each category
                if category == "Sexual Content":
                    prompt = f"Carefully analyze this text and tell me, is there clear, explicit sexual activity, behavior, or inappropriate content present? Only say 'yes' if you are very confident and it is explicit. Otherwise respond with 'no'.\n\nText:\n{chunk}\n\nContext: This text is part of a larger script."
                else:
                    prompt = f"Carefully analyze this text. Does it contain content related to {category}? Answer 'yes' or 'no'.\n\nText:\n{chunk}\n"
                
                # Generate the response using Gemini
                response = model.generate_content(prompt)
                response_text = response.text.strip()

                # Print the response for debugging
                print(f"Response for {category}: {response_text}")

                # Check if the response contains any of the uncertain keywords
                if any(uncertain_keyword in response_text.lower() for uncertain_keyword in uncertain_keywords):
                    print(f"Skipping {category} due to uncertainty: {response_text}")
                    continue

                # Check if the response contains a positive indication of the category
                if "yes" in response_text.lower().strip():
                    identified_triggers.add(category)

        # If no triggers are identified, return "None"
        if not identified_triggers:
            return ["None"]

        return list(identified_triggers)
    except Exception as e:
        return {"error": str(e)}