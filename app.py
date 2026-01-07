import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

st.title("🤖 TalentScout Hiring Assistant")
st.write("I will help with initial candidate screening.")

# -----------------------------
# Session State Initialization
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 Welcome to TalentScout.\nLet's start your screening.\nWhat is your full name?"}
    ]

# -----------------------------
# Helper Functions
# -----------------------------
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def generate_questions(tech_stack):
    questions = []
    for tech in tech_stack:
        tech = tech.lower()
        if "python" in tech:
            questions.extend([
                "Explain the difference between list and tuple in Python.",
                "What are decorators in Python?",
                "How does garbage collection work in Python?"
            ])
        elif "django" in tech:
            questions.extend([
                "What is Django ORM?",
                "Explain Django middleware.",
                "Difference between function-based and class-based views."
            ])
        elif "sql" in tech:
            questions.extend([
                "What is normalization?",
                "Difference between INNER JOIN and LEFT JOIN.",
                "What is an index in SQL?"
            ])
        elif "java" in tech:
            questions.extend([
                "Explain OOP principles in Java.",
                "What is JVM?",
                "Difference between abstract class and interface."
            ])
        else:
            questions.append(f"Explain your experience with {tech}.")
    return questions[:5]

# -----------------------------
# Display Chat Messages
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
user_input = st.chat_input("Type your response here...")

if user_input:
    add_message("user", user_input)

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        add_message("assistant", "Thank you for your time! 👋 We will contact you soon.")
        st.stop()

    # Conversation Flow
    if st.session_state.step == 0:
        st.session_state.data["name"] = user_input
        add_message("assistant", "Please enter your email address:")
        st.session_state.step += 1

    elif st.session_state.step == 1:
        st.session_state.data["email"] = user_input
        add_message("assistant", "Please enter your phone number:")
        st.session_state.step += 1

    elif st.session_state.step == 2:
        st.session_state.data["phone"] = user_input
        add_message("assistant", "How many years of experience do you have?")
        st.session_state.step += 1

    elif st.session_state.step == 3:
        st.session_state.data["experience"] = user_input
        add_message("assistant", "What position are you applying for?")
        st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.data["position"] = user_input
        add_message("assistant", "What is your current location?")
        st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.data["location"] = user_input
        add_message("assistant", "Please list your tech stack (comma separated):")
        st.session_state.step += 1

    elif st.session_state.step == 6:
        tech_stack = [t.strip() for t in user_input.split(",")]
        st.session_state.data["tech_stack"] = tech_stack

        questions = generate_questions(tech_stack)
        question_text = "Great! Here are some technical questions:\n\n"
        for i, q in enumerate(questions, 1):
            question_text += f"{i}. {q}\n"

        add_message("assistant", question_text)
        add_message("assistant", "Thank you for completing the screening! ✅ Our team will review your responses.")
        st.session_state.step += 1

    else:
        add_message("assistant", "Screening already completed. Thank you! 🙌")

    st.rerun()
