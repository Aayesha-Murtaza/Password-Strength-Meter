import streamlit as st
import re
import secrets
import string

st.set_page_config(page_title="Password Strength Meter", page_icon="🔒", layout="wide")
st.title("🔐 Password Strength Meter")
st.write("Enter your password below to check its strength.")

# Custom weights for different security factors
WEIGHTS = {
    "length": 2,       # Password length
    "uppercase": 1,    # Uppercase letters
    "lowercase": 1,    # Lowercase letters
    "digit": 2,        # Numbers
    "special": 3,      # Special characters
    "no_repeats": 1,   # Avoid repeating characters
}
# Function to generate a strong random password
def generate_password(length=12):
    """Generates a strong random password."""
    if length < 8:
        length = 8  # Minimum secure length
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        # Ensure it meets strength criteria
        if (re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*]', password)):
            return password  # Return only if it meets all conditions

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Define a regex for checking common passwords
    common_passwords = [
        "password", "password123", "123456", "qwerty", "abc123", "letmein", "welcome", "monkey", "iloveyou"
    ]

    if password.lower() in common_passwords:
        return "❌ Avoid using common passwords", ""

    if re.search(r"(.)\1\1", password):  
        feedback.append("❌ Avoid using more than 3 consecutive identical characters") 
    else: 
        score += WEIGHTS["no_repeats"]

    # Length Check
    if len(password) >= 8:
        score += WEIGHTS["length"]
    else:
        feedback.append("❌ Password should be at least 8 characters long")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += WEIGHTS["uppercase"]
    else:
        feedback.append("❌ Include uppercase letters")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += WEIGHTS["lowercase"]
    else:
        feedback.append("❌ Include lowercase")        

    # Digit Check
    if re.search(r"\d", password):
       score += WEIGHTS["digit"]
    else:
        feedback.append("❌ Add at least one number (0-9)")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += WEIGHTS["special"]
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*)")

    # Strength Rating
    if score >= 8:
        return "✅ Strong Password!", f"{', '.join(feedback)}"
    elif score >= 4:
        return "⚠️ Moderate Password - Consider adding more security features.", f"{', '.join(feedback)}"
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", f"{', '.join(feedback)}"

# Layout with columns
col1, col2 = st.columns([2, 1])

# Password input and strength check
with col1:
    password = st.text_input("🔑 Enter your password:", type="password")
    if password.strip():
        response, feedback = check_password_strength(password)
        if "Strong" in response:
            st.success(response)
        elif "Moderate" in response:
            st.warning(response)
        else:
            st.error(response)
        
        st.write("**Feedback:**")
        for tip in feedback.split(', '):
            st.markdown(f"{tip}")

# Password generator button
with col2:
    if st.button("🔄 Generate Strong Password"):
        new_password = generate_password()
        st.text_input("✅ Generated Password:", value=new_password, disabled=True)
        st.success("Copy and use this secure password!")
