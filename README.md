Name :- Mohan S Reddy \
Linkedin Profile :- https://www.linkedin.com/in/mohan-s-reddy-45099724a \
Phone Number :- 8762386628 \ 
EMail ID :- mohansreddy1198@gmail.com \
Resume :- https://drive.google.com/file/d/1kHgonHtxsiGSAdDPf45ZE4U5u3yHSaw-/view?usp=sharing \

# AI TriviaX

An interactive web application for generating and administering multiple-choice quizzes.

## Overview

AI TriviaX is a Streamlit application powered by the Groq Llama3 language model. It's designed to create dynamic and engaging quizzes on various topics, allowing users to test their knowledge in an interactive way.

## Setup

1. *Clone (Optional):* `git clone <repository_url>`
2. *Install:* `pip install streamlit langchain langchain-groq difflib python-dotenv`
3. *API Key:* Set the `GROQ_API_KEY` environment variable in a `.env` file. *Do not hardcode it in the script.*
4. *Run:* `streamlit run app.py`

## Usage

1. Open the Streamlit app in your browser.
2. Enter the desired quiz topic in the text input and press Enter.
3. Answer the multiple-choice questions using the radio buttons.
4. Click "Submit Answer" to check your response and receive feedback.
5. Continue through the quiz until all questions are answered or you choose to exit.
6. View your score at the end of the quiz.

## Key Features

* Dynamic question generation using Llama3.
* Question uniqueness through memory and similarity checks.
* Immediate feedback on answers.
* Customizable number of questions (using `MAX_QUESTIONS` variable).
* User-friendly Streamlit interface.
* Exit and restart quiz options.

## Dependencies

* Streamlit
* LangChain
* LangChain-Groq
* `difflib` (for similarity checking)
* `python-dotenv` (for environment variables)

## API Key

You need a Groq API key to use this application. Get one from Groq and set it as an environment variable in a `.env` file (recommended) or, for testing only, as a variable in the script. *Never commit your API key to version control.*  Create a `.env` file in the same directory as your script and add the following line (replacing with your actual key):
