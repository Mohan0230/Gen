import streamlit as st
from langchain import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import difflib
import time

# Initialize ChatGroq
GROQ_API_KEY = "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"
chat = ChatGroq(model_name="llama3-70b-8192", groq_api_key=GROQ_API_KEY)

# Memory to track quiz progress
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_text" not in st.session_state:
    st.session_state.question_text = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "user_topic" not in st.session_state:
    st.session_state.user_topic = ""
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = ""
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# Maximum number of questions
MAX_QUESTIONS = 10

# System Prompt Template with Question Memory Check
prompt = PromptTemplate(input_variables=["question", "past_questions"], template="""
You are an AI-powered educational assessment tool designed to generate high-quality Multiple Choice Questions (MCQs).
Your priority is to ensure unique questions, accurate answer generation, and an adaptive experience.

Instructions:
* Generate a unique MCQ based on the given topic.
* Ensure the MCQ is clear, concise, and challenging.
* Do NOT repeat any previously generated questions.
* Cross-check the new question against the provided list of past questions to ensure it is truly unique.
* Avoid generating questions that are slightly relevant or reworded versions of previous questions.
* Ensure the question differs significantly in concept from all past questions.
* Provide the correct answer at the end in the format: "Answer: (option)"
* Do not include any introductory text like 'Here is a unique MCQ based on the topic'.
* Do not include "Your Answer (a/b/c/d):" in the output.

Previously Asked Questions:
{past_questions}

Topic: {question}

MCQ:
""")

# Function to check similarity
def is_similar(new_question, previous_questions, threshold=0.75):
    for prev_q in previous_questions:
        similarity = difflib.SequenceMatcher(None, new_question.lower(), prev_q.lower()).ratio()
        if similarity >= threshold:
            return True
    return False

# Function to ask MCQ
def ask_mcq(topic):
    retries = 20  # Maximum attempts to get a unique question
    past_questions = "\n".join(st.session_state.asked_questions) if st.session_state.asked_questions else "None"
    
    while retries > 0:
        response = chat.invoke([HumanMessage(content=prompt.format(question=topic, past_questions=past_questions))])
        question_text = response.content.strip()
        
        # Ensure the question is not similar to previous ones
        if question_text not in st.session_state.asked_questions and not is_similar(question_text, st.session_state.asked_questions):
            st.session_state.asked_questions.add(question_text)

            # Extract correct answer
            lines = question_text.split("\n")
            answer_line = [line for line in lines if line.lower().startswith("answer:")]
            if answer_line:
                st.session_state.correct_answer = answer_line[0].split(":", 1)[1].strip()
                question_text = "\n".join([line for line in lines if not line.lower().startswith("answer:")])
            
            return question_text
        
        retries -= 1  # Reduce retry count
        time.sleep(1)  # Avoiding quick repetitions if needed
    return "No unique question available. Try a different topic."

# Streamlit UI
st.title("🤖AI TriviaX")

user_topic_input = st.text_input("Enter your topic to start the quiz and press Enter:")

if user_topic_input and not st.session_state.quiz_started:
    st.session_state.user_topic = user_topic_input
    st.session_state.quiz_started = True
    st.session_state.question_text = ask_mcq(st.session_state.user_topic)
    st.session_state.score = 0
    st.session_state.asked_questions.clear()
    st.session_state.question_count = 0
    st.rerun()

if st.session_state.quiz_started:
    if st.session_state.question_count < MAX_QUESTIONS:
        st.subheader(f"Question {st.session_state.question_count + 1}:")
        question_lines = [line for line in st.session_state.question_text.split("\n") if line.strip()]
        question_text = question_lines[0]
        options = question_lines[1:]
        
        st.write(question_text)
        if options:
            selected_option = st.radio("Select your answer:", options, index=None, key=f"radio_option_{st.session_state.question_count}")
        else:
            selected_option = None
        
        if st.button("Submit Answer") and selected_option:
            if selected_option.strip().lower() == st.session_state.correct_answer.strip().lower():
                st.session_state.score += 1
                st.success("✅ Correct! Well done.")
            else:
                st.error(f"❌ Incorrect. The correct answer is {st.session_state.correct_answer}.")
            
            # Increment question count
            st.session_state.question_count += 1
            
            # Generate next question if limit not reached
            if st.session_state.question_count < MAX_QUESTIONS:
                st.session_state.question_text = ask_mcq(st.session_state.user_topic)
            st.rerun()
        
        st.write(f"**Score:** {st.session_state.score} / {MAX_QUESTIONS}")

    # End Quiz if question limit is reached
    if st.session_state.question_count == MAX_QUESTIONS:
        st.success(f"🎉 Quiz Completed! Your Final Score: {st.session_state.score} / {MAX_QUESTIONS}")
        if st.button("Restart Quiz"):
            st.session_state.quiz_started = False
            st.session_state.asked_questions.clear()
            st.session_state.question_text = ""
            st.session_state.question_count = 0
            st.rerun()
