import streamlit as st

def generate_quiz(subject, topics, num_questions):
    # Define your quiz questions and answers here
    quiz = {
        "Physics": {
            "Motion": {
                "question": "What is the formula for calculating velocity?",
                "options": ["v = d/t", "v = a*t", "v = F/m", "v = m*a"],
                "answer": 0  # Index of correct answer in options list
            },
            "Electricity": {
                "question": "What is Ohm's law?",
                "options": ["V = IR", "V = I/R", "I = VR", "R = VI"],
                "answer": 0
            },
            # Add more questions and topics as needed
        }
    }

    # Fetch questions for the specified subject and topics
    questions = []
    for topic in topics.split(","):
        if topic.strip() in quiz.get(subject, {}):
            questions.append(quiz[subject][topic.strip()])

    # Limit the number of questions
    num_questions = min(num_questions, len(questions))

    return questions[:num_questions]

def main():
    st.title("Quiz App")

    # Session state for storing quiz data
    if 'quiz_questions' not in st.session_state:
        st.session_state['quiz_questions'] = []
    if 'score' not in st.session_state:
        st.session_state['score'] = 0

    # Input fields for subject, topics, and number of questions
    subject = st.text_input("Enter subject name:", "Physics")
    topics = st.text_input("Enter topics (comma-separated):", "Motion, Electricity")
    num_questions = st.number_input("Enter number of questions:", min_value=1, max_value=10, step=1, value=3)

    # Button to generate quiz
    if st.button("Start Quiz"):
        st.session_state['quiz_questions'] = generate_quiz(subject, topics, num_questions)
        st.session_state['score'] = 0  # Reset score

    # Display quiz questions and collect user answers
    for index, question_data in enumerate(st.session_state['quiz_questions']):
        st.write(f"Question {index+1}: {question_data['question']}")
        selected_option_index = st.radio(f"Options for Question {index+1}", options=question_data["options"], key=f"radio_{index}")

        # Store selected option in session state
        st.session_state[f"selected_option_{index}"] = selected_option_index

        correct_answer = question_data["answer"]

        # Check if selected answer is correct
        if selected_option_index == correct_answer:
            st.session_state['score'] += 1  # Increment score for correct answer

    # Display final score
    if st.session_state['quiz_questions']:
        st.write(f"Your final score: {st.session_state['score']}/{len(st.session_state['quiz_questions'])}")

if __name__ == "__main__":
    main()
