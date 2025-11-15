# Gemini Integration

I have replaced OpenAI with Gemini for challenge generation. Please note the following:

1.  I have added the `google-generativeai` to your `pyproject.toml`. You will need to install this dependency.
2.  I have added a `GEMINI_API_KEY` to your `.env` file in `backend/src`. Please replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.

Once you have installed the dependencies and added your API key, the application will use Gemini to generate challenges.
