import json
import re

def identify_triggers(model_response):
    """
    Process Gemini's JSON response to identify triggers
    """
    identified_triggers = set()
    
    try:
        # If the response is already a dict, use it directly
        if isinstance(model_response, dict):
            response_data = model_response
        else:
            # Clean and parse JSON response
            json_str = re.sub(r'```json\s*|\s*```', '', model_response)
            response_data = json.loads(json_str)
        
        # Process each category in the response
        for category, details in response_data.items():
            verdict = details.get("verdict", "").upper()
            confidence = details.get("confidence", "LOW").upper()
            reasoning = details.get("reasoning", "").upper()
            
            # Check for negations in reasoning
            negation_patterns = [
                r"NO INSTANCES",
                r"NOT PRESENT",
                r"NOT FOUND",
                r"DOES NOT CONTAIN",
                r"DIDN'T FIND",
                r"ABSENT",
                r"LACKS",
            ]
            
            has_negation = any(re.search(pattern, reasoning) for pattern in negation_patterns)
            
            # Add to identified triggers if conditions are met
            if verdict == "YES" and not has_negation and confidence in ["MEDIUM", "HIGH"]:
                identified_triggers.add(normalize_category(category))
                
    except Exception as e:
        logging.error(f"Error processing model response: {e}")
        return []
    
    return list(identified_triggers)

def normalize_category(category):
    """
    Normalize category names to match expected format
    """
    category_mapping = {
        "VIOLENCE": "Violence",
        "SELF_HARM": "Self-Harm",
        "DEATH": "Death",
        "SUBSTANCE_USE": "Substance Use",
        "SEXUAL_CONTENT": "Sexual Content",
        "SEXUAL_ABUSE": "Sexual Abuse",
        "GUN_USE": "Gun Use",
        "GORE": "Gore",
        "VOMIT": "Vomit",
        "MENTAL_HEALTH": "Mental Health Issues",
        "ANIMAL_CRUELTY": "Animal Cruelty"
    }
    
    # Normalize the category name
    normalized = category.upper().replace(" ", "_")
    return category_mapping.get(normalized, category)

def extract_category(response_text):
    """
    Extract category from response text with improved context awareness
    """
    trigger_categories = {
        "Violence": ["violence", "violent", "fighting", "physical harm"],
        "Self-Harm": ["self-harm", "self harm", "suicide", "self-injury"],
        "Death": ["death", "dying", "deceased", "fatal"],
        "Substance Use": ["drug", "alcohol", "substance", "addiction"],
        "Sexual Content": ["sexual content", "sexual themes", "sexual activity"],
        "Sexual Abuse": ["sexual abuse", "assault", "rape"],
        "Gun Use": ["gun", "firearm", "shooting", "weapon"],
        "Gore": ["gore", "blood", "graphic violence", "mutilation"],
        "Vomit": ["vomit", "throw up", "nausea", "sick"],
        "Mental Health Issues": ["mental health", "depression", "anxiety", "psychiatric"],
        "Animal Cruelty": ["animal abuse", "animal cruelty", "harm to animals"]
    }
    
    response_lower = response_text.lower()
    
    for category, keywords in trigger_categories.items():
        # Check if any keyword is present in a positive context
        for keyword in keywords:
            if keyword in response_lower:
                # Check for nearby negations
                start_idx = max(0, response_lower.find(keyword) - 50)
                end_idx = min(len(response_lower), response_lower.find(keyword) + 50)
                context = response_lower[start_idx:end_idx]
                
                negations = ["no", "not", "none", "absent", "lacks", "without"]
                if not any(neg in context.split() for neg in negations):
                    return category
                    
    return None