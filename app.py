import streamlit as st
import openai
import base64
from io import BytesIO

# Assuming your OpenAI API key is set in your environment variables for security
# Set it directly in the code for demonstration, but be cautious with your key's security
openai.api_key = "sk-gvRy"

st.title('COBOL to C# Converter')

# Text area for user input
user_input = st.text_area("Enter COBOL code to convert to C#:", height=300)

def generate_downloadable_file(text):
    """Generate a downloadable file from the provided text."""
    towrite = BytesIO()
    towrite.write(text.encode('utf-8'))
    towrite.seek(0)  # Move cursor to the beginning of the file
    return towrite

if st.button('Convert and Generate Business Rules'):
    if user_input:
        # Call to OpenAI's API for code conversion
        conversion_response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Generate C# code equivalent for the provided COBOL code: {user_input}",
            max_tokens=250  # Adjusted for potential length of C# code
        )
        converted_code = conversion_response.choices[0].text.strip()

        # Call to OpenAI's API for business rules generation
        business_rules_response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Generate business rules from the provided COBOL Tandem program: {user_input}",
            max_tokens=150
        )
        business_rules = business_rules_response.choices[0].text.strip()

        # Display the results
        st.subheader("Converted C# Code:")
        st.text(converted_code)
        
        st.subheader("Business Rules:")
        st.text(business_rules)

        # Download buttons
        converted_code_file = generate_downloadable_file(converted_code)
        st.download_button(label="Download Converted C# Code",
                           data=converted_code_file,
                           file_name="converted_code.txt",
                           mime='text/plain')
        
        business_rules_file = generate_downloadable_file(business_rules)
        st.download_button(label="Download Business Rules",
                           data=business_rules_file,
                           file_name="business_rules.txt",
                           mime='text/plain')

    else:
        st.warning("Please enter COBOL code to convert.")
