# TREAT-Gemini

This is an experimental repository to port [TREAT](https://github.com/Kuberwastaken/TREAT) to use the Gemini 2.0 Flash model.

## Setup Instructions

### Step 1: Generate Your API Key
To use Gemini 2.0, generate an API key from Google AI Studio:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Generate and copy your API key.

### Step 2: Add the API Key to the Project
1. Create a file named `.env` in the `treat/env` directory.
2. Paste the following into the `.env` file:

```
   API_KEY=your_generated_api_key_here
```

## Known Issues

- **Accuracy Concerns:** Google Gemini Flash 2.0 currently achieves about **40% accuracy** on test cases, making it **unusable** as the main model.
- **Highly Limited Usage:** Google has API limits on the model (fairly so) as it's free.

## Seeking Contributions

Improvements and optimizations are highly encouraged. If you have ideas to enhance accuracy or functionality, feel free to contribute via pull requests or by opening an issue.


