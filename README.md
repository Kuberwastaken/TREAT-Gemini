![Treat_Banner](https://github.com/Kuberwastaken/TREAT-Gemini/blob/main/static/readme-images/New_Treat_Banner.png?raw=true)

<h1 align="center">
  TREAT-Gemini
</h1>

<p align="center">
<img src="https://img.shields.io/static/v1?label=Kuberwastaken&message=TREAT-Gemini&color=pink&logo=github" alt="Kuberwastaken - TREAT">
<img src="https://img.shields.io/badge/License-Apache_2.0-pink" alt="License Apache 2.0">
</p>

This Experimental version of TREAT uses Google's Gemini 2.0 Flash model

At this moment, this version is **NOT STABLE**

## Project Description

I was tired of getting grossed out watching unexpected scenes in movies and TV and losing my appetite, that's why I created TREAT.

The goal of this project is to empower viewers by forewarning them about potential triggers in the content they watch, making the viewing experience more enjoyable, inclusive, and appropriate for everyone.

TREAT is a web application that uses natural language processing to analyze movie and TV show scripts, identifying potential triggers to help viewers make informed choices.


## Installation Instructions
### Prerequisites
 - Star the Repository to Show Your Support.
 - Clone the Repository to Your Local Machine:

    ```bash
   git clone https://github.com/Kuberwastaken/TREAT-Gemini.git
    ```

### Step 1: Generate Your API Key
To use Gemini 2.0, generate an API key from Google AI Studio:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).

2. Generate and copy your API key.

   ![API Key Instructions](https://github.com/Kuberwastaken/TREAT-Gemini/blob/main/static/readme-images/instuctions.png?raw=true)

### Step 2: Add the API Key to the Project
1. Create a file named `.env` in the `treat/env` directory.
2. Paste the following into the `.env` file:

   ```
   API_KEY=your_generated_api_key_here
   ```

### Environment Setup
To set up the development environment, you will need to create a virtual environment and install the necessary dependencies.

1. Create a Virtual Environment:

   ```bash
   python3 -m venv treat-gemini
   ```

2. Activate the Virtual Environment:

   ```bash
   source treat-gemini/bin/activate   # On Unix or MacOS
   treat-gemini\Scripts\activate      # On Windows
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

- **app/model.py:** Includes the script analysis functions using the gemini-2.0-flash-exp model.

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

Adding new categories is as simple as specifying a new category under model.py and utils.py

## Design Choices

- **Inspiration:** I aimed for a simple and intuitive user experience, focusing on simplicity and ease of use. This decision stemmed from the need to create a tool that is easy to navigate for all users, regardless of background or age.

- **Theme and Color Scheme:** The chosen theme and color scheme create a visually appealing and engaging environment. The chocolate and sweets theme is intended to stick to the TREAT theme and make the experience enjoyable and pleasant.

## Known Issues

- **Accuracy Concerns:** Google Gemini Flash 2.0 currently achieves about **40% accuracy** on test cases, making it **unusable** as the main model.

- **Highly Limited Usage:** Google has API limits on the model (fairly so) as it's free.

## Open Source Contribution
This model is currently highly unstable with only 40% accuracy in the given test_files, any improvments to the model is highly encouraged!

## Acknowledgements
I would like to thank:

- Google: For developing the gemini-2.0-flash-exp model, a very critical component of this project.

- Parasite (2019): For that unexpected jumpscare that ruined my appetite and ultimately inspired this project.

## License
This project is licensed under the [Apache 2.0 License](https://github.com/Kuberwastaken/TREAT-Gemini/blob/main/LICENSE).