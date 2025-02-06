![Treat_Banner](static/images/readme-images/Treat_Banner.png)

<h1 align="center">
  Trigger Recognition for Enjoyable and Appropriate Television - Gemini 2.0 Thinking
</h1>

<p align="center">
<img src="https://img.shields.io/static/v1?label=Kuberwastaken&message=TREAT&color=daa3b2&logo=github" alt="Kuberwastaken - TREAT">
<img src="https://img.shields.io/badge/version-Alpha-daa3b2" alt="Version Alpha">
</p>

<h1 align="center">
  NOTE: THIS VERSION'S DEVELOPMENT IS IN HIATUS UNTIL (AND IF) A MORE GENEROUS RATE LIMIT IS OFFERED BY GOOGLE
</h1>

I was tired of getting grossed out watching unexpected scenes in movies and TV and losing my appetite, that's why I created TREAT.

The goal of this project is to empower viewers by forewarning them about potential triggers in the content they watch, making the viewing experience more enjoyable, inclusive, and appropriate for everyone.

TREAT is a web application that uses natural language processing to analyze movie and TV show scripts, identifying potential triggers to help viewers make informed choices.

## Installation Instructions
### Prerequisites
 - Star the Repository to Show Your Support (:P)
 - Clone the Repository to Your Local Machine:

    ```bash
   git clone https://github.com/Kuberwastaken/TREAT-Gemini.git
    ```

## Get Your Free API Key
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **Create API Key** in the left panel
4. Name your key (e.g., "TREAT_DEV")
5. Copy the generated key

🔒 **Security Setup (Recommended)**
```bash
# Linux/macOS
export GEMINI_API_KEY="your_key_here"
```

### Environment Setup
To set up the development environment, you will need to create a virtual environment and install the necessary dependencies.

1. Create a Virtual Environment:

   ```bash
   python3 -m venv treat-gemini
   ```

2. Activate the Virtual Environment:

   ```bash
   source treat-env/bin/activate   # On Unix or MacOS
   treat-env\Scripts\activate      # On Windows
   ```

3. Install Dependencies:

   Navigate to the project directory and run:

   ```bash
   pip install -r requirements.txt
   ```

## Project Usage
1. **Start the Flask Server:**

   ```bash
   python run.py
   ```

2. **Open Your Browser:** 

   Navigate to `http://127.0.0.1:5000` to access the TREAT web interface.

3. **Analyze Scripts:**

   You can manually enter a script in the provided text area and click "Analyze Script."

## File Descriptions
- **app.py:** The main Flask application file that handles routing.

- **app/routes.py:** Contains the Flask routes for handling script uploads.

- **app/model.py:** Includes the script analysis functions using the Llama-3.2-1B model.

- **templates/index.html:** The main HTML file for the web interface.

- **static/css/style.css:** Custom CSS for styling the web interface.

- **static/js/app.js:** JavaScript for handling client-side interactions.

## Types of Triggers Detected
The TREAT application focuses on identifying a variety of potential triggers in scripts, including but not limited to:

- **Violence:** Scenes of physical aggression or harm.

- **Self-Harm:** Depictions of self-inflicted injury.

- **Death:** Depictions of death or dying characters.

- **Sexual Content:** Any depiction or mention of sexual activity, intimacy, or behavior.

- **Sexual Abuse:** Instances of sexual violence or exploitation.

- **Gun Use:** Depictions of firearms and their usage.

- **Gore:** Graphic depiction of injury, blood, or dismemberment.

- **Vomit:** Depictions of vomiting or nausea-inducing content.

- **Mental Health Issues:** Depictions of mental health struggles, including anxiety, depression, or disorders.

- **Animal Cruelty:** Depictions of harm or abuse towards animals.

These categories help address a very real-world problem by forewarning viewers about potentially distressing content, enhancing their viewing experience.

Adding new categories is as simple as specifying a new category under model.py and utils.py (no detailed prompts needed as it's a deep reasoning model)

## Why Gemini 2.0 Thinking?
✅ **Best Features**
- **1M Token Context Window**: Process ~1,500 pages of text in a single request
- **Free Tier Access**: Available through Google AI Studio with basic usage 
- **Multimodal Understanding**: Analyzes text, images, and eventually audio/
- **Enhanced Safety**: Built with self-critique RL and automated red 
- **Cost Efficiency**: ~40k operations/$ in paid tiers (when scaled) 

⚠️ **Current Limitations**
- **Strict Rate Limits**: 60 QPM (queries per minute) in public preview 
- **Output Restrictions**: 8k token response limit 
- **Preview Limitations**: Some features like image analysis still in private preview 

## Acknowledgements
I would like to thank:

- Google : For developing and allowing access to the Gemini model, a very critical component of this project.

- Parasite (2019): For that unexpected jumpscare that ruined my appetite and ultimately inspired this project.
