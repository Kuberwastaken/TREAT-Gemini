from flask import Flask, request, jsonify, render_template
from app import app
from app.model import analyze_script
import logging
import asyncio
from functools import partial

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def async_to_sync(async_func):
    """Decorator to run async functions in Flask routes"""
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering async_to_sync wrapper for {async_func.__name__}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            logger.debug("Running async function in event loop")
            result = loop.run_until_complete(async_func(*args, **kwargs))
            logger.debug("Async function completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in async execution: {str(e)}", exc_info=True)
            raise
        finally:
            logger.debug("Closing event loop")
            loop.close()
    return wrapper

@app.route('/')
def home():
    logger.debug("Serving home page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@async_to_sync
async def upload_script():
    logger.debug("Received upload request")
    try:
        # Log request details
        logger.debug(f"Request Content-Type: {request.content_type}")
        logger.debug(f"Request headers: {dict(request.headers)}")
        
        # Get the JSON data from the request
        data = request.get_json()
        logger.debug(f"Received data: {data}")
        
        content = data.get('text', '')
        logger.debug(f"Content length: {len(content)} characters")
        
        if not content:
            logger.warning("No text content provided")
            return jsonify({"error": "No text content provided"}), 400
        
        # Analyze the script
        logger.debug("Starting script analysis")
        analysis_results = await analyze_script(content)
        logger.debug(f"Analysis results: {analysis_results}")
        
        if "error" in analysis_results:
            logger.error(f"Analysis error: {analysis_results['error']}")
            return jsonify({"error": analysis_results["error"]}), 500
        
        # Transform the results
        logger.debug("Transforming results")
        results_list = []
        for category, details in analysis_results.items():
            results_list.append({
                "category": category,
                "status": details["status"],
                "confidence": details["confidence"],
                "matches": details["chunk_matches"],
                "examples": details.get("examples", [])
            })
        
        logger.debug(f"Transformed results: {results_list}")
        return jsonify({"results": results_list})
        
    except Exception as e:
        logger.error("Error in upload_script", exc_info=True)
        return jsonify({"error": str(e)}), 500