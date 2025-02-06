import re
import time
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Union
import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from ratelimit import limits, sleep_and_retry

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Rate limit configuration
CALLS_PER_MINUTE = 58  # Setting slightly below the 60 QPM limit
PERIOD = 60  # seconds
last_reset = datetime.now()
call_count = 0

API_KEY_FILE = "google_api_key.txt"
MODEL_NAME = "gemini-2.0-flash-thinking-exp"

# Increased to utilize Gemini's full context window
MAX_CHUNK_SIZE = 600000  # ~900K characters to leave room for prompt

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

class RateLimitError(Exception):
    """Custom exception for rate limit errors"""
    pass

def load_api_key() -> str:
    try:
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise APIError(f"API key file {API_KEY_FILE} not found")

def initialize_gemini():
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)
    
    # Configure for deep analysis
    model.generation_config = {
        "temperature": 0.1,  # Keep low for consistent analysis
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,  # Allow for detailed reasoning
    }
    return model

async def wait_for_quota_reset():
    """Wait until the next quota period"""
    global last_reset, call_count
    now = datetime.now()
    time_since_reset = (now - last_reset).total_seconds()
    
    if time_since_reset < PERIOD and call_count >= CALLS_PER_MINUTE:
        wait_time = PERIOD - time_since_reset
        logger.info(f"Rate limit reached. Waiting {wait_time:.1f} seconds for quota reset")
        await asyncio.sleep(wait_time)
        last_reset = datetime.now()
        call_count = 0
    elif time_since_reset >= PERIOD:
        last_reset = now
        call_count = 0

async def rate_limited_query(model, content: str, categories: List[str]) -> Dict:
    """Rate-limited version of the API query"""
    global call_count
    
    await wait_for_quota_reset()
    
    try:
        response = await model.generate_content_async(
            content,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        call_count += 1
        return response
    except Exception as e:
        if "RATE_LIMIT_EXCEEDED" in str(e):
            raise RateLimitError("Rate limit exceeded")
        raise APIError(f"API Error: {str(e)}")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=20),
    retry=retry_if_exception_type((RateLimitError, APIError)),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def query_gemini_api(model, content: str, categories: List[str]) -> Dict[str, Dict]:
    try:
        logger.debug("Starting Gemini API query")
        logger.debug(f"Content length: {len(content)} characters")
        logger.debug(f"Categories to analyze: {categories}")

        prompt = f"""You are a sophisticated content analysis system. Analyze the following text for potentially sensitive content.

For each category, provide:
1. A clear YES/NO/MAYBE verdict
2. Your detailed reasoning
3. Confidence level (LOW/MEDIUM/HIGH)
4. Specific examples from the text (if any)

Format your response as JSON with the following structure for each category:
{{
    "category_name": {{
        "verdict": "YES/NO/MAYBE",
        "reasoning": "Your detailed explanation",
        "confidence": "LOW/MEDIUM/HIGH",
        "examples": ["example1", "example2"]
    }}
}}

Categories to analyze: {', '.join(categories)}

Text to analyze:
{content}"""

        logger.debug("Sending rate-limited request to Gemini API")
        response = await rate_limited_query(model, prompt, categories)
        
        logger.debug("Received response from Gemini API")
        logger.debug(f"Raw response type: {type(response)}")
        logger.debug(f"Raw response: {response}")
        
        if not hasattr(response, 'candidates') or not response.candidates:
            logger.error("No candidates in response")
            raise APIError("No response generated")
        
        try:
            json_str = response.text
            logger.debug(f"Response text: {json_str}")
            
            # Clean up common JSON formatting issues
            json_str = re.sub(r'```json\s*|\s*```', '', json_str)
            json_str = re.sub(r'^[\s\n]*\{', '{', json_str)
            json_str = re.sub(r'\}[\s\n]*$', '}', json_str)
            
            logger.debug(f"Cleaned JSON string: {json_str}")
            
            parsed_response = json.loads(json_str)
            logger.debug(f"Successfully parsed JSON response: {parsed_response}")
            return parsed_response
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Problematic JSON string: {json_str}")
            raise APIError(f"Failed to parse model response as JSON: {str(e)}")
            
    except RateLimitError:
        logger.warning("Rate limit hit, will retry after waiting")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in query_gemini_api: {str(e)}", exc_info=True)
        raise

async def analyze_script(script: str) -> Dict[str, Union[int, str]]:
    logger.info("Starting Analysis")
    start_time = time.time()
    
    try:
        # Log script details
        logger.debug(f"Script length: {len(script)} characters")
        
        # Initialize Gemini model
        logger.debug("Initializing Gemini model")
        model = initialize_gemini()
        logger.debug("Model initialized successfully")

        # Calculate chunks
        chunks = [script[i:i+MAX_CHUNK_SIZE] for i in range(0, len(script), MAX_CHUNK_SIZE)]
        logger.debug(f"Split into {len(chunks)} chunks")

        categories = [
            "VIOLENCE", "DEATH", "SUBSTANCE_USE", "GORE",
            "VOMIT", "SEXUAL_CONTENT", "SEXUAL_ABUSE",
            "SELF_HARM", "GUN_USE", "ANIMAL_CRUELTY", "MENTAL_HEALTH"
        ]

        identified = {cat: {"count": 0, "confidence": [], "examples": []} for cat in categories}
        
        for chunk_idx, chunk in enumerate(chunks, 1):
            logger.info(f"Processing chunk {chunk_idx}/{len(chunks)}")
            logger.debug(f"Chunk {chunk_idx} length: {len(chunk)} characters")
            
            try:
                response = await query_gemini_api(model, chunk, categories)
                logger.debug(f"Received response for chunk {chunk_idx}")
                
                for category in categories:
                    if category in response:
                        logger.debug(f"Processing category {category} for chunk {chunk_idx}")
                        cat_data = response[category]
                        verdict = cat_data.get("verdict", "").upper()
                        confidence = cat_data.get("confidence", "LOW")
                        
                        if verdict == "YES":
                            identified[category]["count"] += 1
                            identified[category]["confidence"].append(confidence)
                            identified[category]["examples"].extend(cat_data.get("examples", []))
                            logger.debug(f"Found {category} in chunk {chunk_idx} with confidence {confidence}")
                    else:
                        logger.debug(f"Category {category} not found in response for chunk {chunk_idx}")
                
            except Exception as e:
                logger.error(f"Error processing chunk {chunk_idx}: {str(e)}", exc_info=True)
                continue

        logger.info("\n=== Final Results ===")
        final_results = {}
        for category in categories:
            count = identified[category]["count"]
            confidence_levels = identified[category]["confidence"]
            examples = identified[category]["examples"]
            
            status = "NOT_FOUND" if count == 0 else "CONFIRMED"
            # Determine overall confidence: if any high confidence then HIGH, else MEDIUM if any medium else LOW
            if "HIGH" in confidence_levels:
                overall_conf = "HIGH"
            elif "MEDIUM" in confidence_levels:
                overall_conf = "MEDIUM"
            else:
                overall_conf = "LOW"
            
            final_results[category] = {
                "status": status,
                "confidence": overall_conf,
                "chunk_matches": f"{count}/{len(chunks)}",
                "examples": examples[:3]
            }
            
            logger.info(f"{category}: {status} (Confidence: {overall_conf}, Matches: {count}/{len(chunks)})")

        total_time = time.time() - start_time
        logger.info(f"Total analysis time: {total_time:.1f}s")
        return final_results

    except Exception as e:
        logger.error("Error in analyze_script", exc_info=True)
        return {"error": str(e)}

async def get_detailed_analysis(script: str) -> Dict[str, Union[int, str]]:
    return await analyze_script(script)

# For running the script directly for testing purposes
if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 2:
        logger.error("Please provide a script file to analyze.")
        sys.exit(1)
    
    script_file = sys.argv[1]
    
    try:
        with open(script_file, "r", encoding="utf-8") as f:
            script_content = f.read()
    except Exception as e:
        logger.error(f"Error reading script file: {e}")
        sys.exit(1)
    
    analysis_results = asyncio.run(get_detailed_analysis(script_content))
    print(json.dumps(analysis_results, indent=4))
