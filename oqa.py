import streamlit as st
from PyPDF2 import PdfReader
from fpdf import FPDF
import random
import os

# Function to extract questions from PDF file
def extract_questions_from_pdf(pdf_file):
    questions = []
    with open(pdf_file, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            questions.append(text)
    return questions

# Function to assign questions to students
def assign_questions_to_students(questions, num_students):
    assigned_questions = {}
    available_questions = list(range(len(questions)))
    random.shuffle(available_questions)
    for student_num in range(1, num_students + 1):
        if available_questions:
            question_index = available_questions.pop()  # Assigning 1 question per student
            assigned_questions[student_num] = questions[question_index]
        else:
            assigned_questions[student_num] = "No more questions available."
    return assigned_questions

# Function to generate PDF with assigned question
def generate_pdf(assigned_question, roll_no):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = f"Question for Roll Number {roll_no}", ln = True, align = 'C')
    pdf.cell(200, 10, txt = assigned_question, ln = True, align = 'L')
    pdf_file_name = f"question_roll_{roll_no}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name

def main():
    st.title("Online Exam Questions")

    # Load PDF file and extract questions
    pdf_file = "D:\\aja lab exam programs\\alp.pdf"  # Replace with the actual path to your PDF file
    questions = extract_questions_from_pdf(pdf_file)

    # Check if session state is initialized
    if 'assigned_questions' not in st.session_state:
        st.session_state.assigned_questions = None

    roll_no = st.text_input("Enter your Roll Number")

    if roll_no:
        num_students = 74  # Number of students
        
        # Assign questions to students if not already assigned
        if st.session_state.assigned_questions is None:
            st.session_state.assigned_questions = assign_questions_to_students(questions, num_students)

        # Display assigned questions for the entered roll number
        if roll_no.isdigit():
            roll_no = int(roll_no)
            if roll_no in st.session_state.assigned_questions:
                st.header(f"Question for Roll Number {roll_no}")
                st.markdown(f"**Question:** {st.session_state.assigned_questions[roll_no]}")

                # Generate PDF for the assigned question
                pdf_file_name = generate_pdf(st.session_state.assigned_questions[roll_no], roll_no)

                # Provide download link for the generated PDF
                st.markdown(f"[Download Question PDF](/{pdf_file_name})")
            else:
                st.write("Roll Number not found or no question assigned.")
        else:
            st.write("Please enter a valid Roll Number.")

if __name__ == "__main__":
    main()
