import streamlit as st
import datetime
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page configuration
st.set_page_config(
    page_title="JBS Support Assistance",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the title and header (centered)
st.markdown("<h1 style='text-align: center;'>JBS Support Assistance</h1>", unsafe_allow_html=True) 

# Welcome message (centered)
st.markdown("<p style='text-align: center;'>Welcome to the JBS Support Assistance tool. Please enter the details below to get a comprehensive response to your inquiry.</p>", unsafe_allow_html=True) 

# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gemini-pro"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
llm_model = "gemini-pro" if current_date > target_date else "gemini-pro"

# Replace with your actual API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyD_D1Ifsgs8V-gAH9AV81fJUpQN7p4Mhwc"

# Initialize LLM and Memory
llm = ChatGoogleGenerativeAI(temperature=0.0, model=llm_model)
memory = ConversationBufferMemory()

# Create ConversationChain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Initialize session state if not already present
if 'customer_name' not in st.session_state:
    st.session_state.customer_name = ""
if 'person_name' not in st.session_state:
    st.session_state.person_name = ""
if 'response' not in st.session_state:
    st.session_state.response = ""
if 'inquiry_history' not in st.session_state:
    st.session_state.inquiry_history = [] 
if 'inquiries_and_responses' not in st.session_state:
    st.session_state.inquiries_and_responses = []

# Function to display chat history
def display_chat_history():
    for entry in st.session_state.inquiries_and_responses:
        st.markdown(f"**Response:** {entry['response']}")
        st.markdown("---")

# Show the chat history
st.markdown("<h3 style='text-align: center;'>Chat History</h3>", unsafe_allow_html=True)
display_chat_history()

# Show the form
st.markdown("<h3 style='text-align: center;'>Submit Your Inquiry</h3>", unsafe_allow_html=True)  # Center the header
with st.form(key="support_form"):
    if not st.session_state.customer_name or not st.session_state.person_name:
        col1, col2 = st.columns(2)  # Create two columns

        with col1:  # Place Customer Name in the first column
            st.session_state.customer_name = st.text_input("Customer Name", value=st.session_state.customer_name)

        with col2:  # Place Person Name in the second column
            st.session_state.person_name = st.text_input("Person Name", value=st.session_state.person_name)

    inquiry = st.text_area("Inquiry")
    submit_button = st.form_submit_button(label="Submit")

# Process the inquiry and generate the response when the form is submitted
if submit_button:
    if st.session_state.customer_name and st.session_state.person_name and inquiry:
        # Add the inquiry to the history
        st.session_state.inquiry_history.append(inquiry)

        # Build response structure
        response_structure = f"""
        ## JBS Support Response 

        **Customer:** {st.session_state.customer_name}
        **Person:** {st.session_state.person_name}
        **Inquiry:** {inquiry}

        **Response:**
        """

        try:
            # Generate response using the ConversationChain (using keyword arguments)
            response = conversation.run(
                input=response_structure + 
                """
                Please provide a detailed and helpful response to the customer's inquiry. 
                Ensure that your response:

                - Only provide the first level support.
                - Addresses all aspects of the customer's question thoroughly.
                - Includes references to any external data or solutions used.
                - Maintains a friendly, professional, and approachable tone.
                - Is written clearly and is easy to understand, avoiding jargon unless necessary.
                - Is accurate and complete, leaving no questions unanswered.

                For support inquiries, you can contact JBS Customer Support at:
                Email: customercare@jbs.live
                Website: https://jbs.live/

                Here's the customer's past inquiries:
                {st.session_state.inquiry_history}

                Customer's Inquiry:
                {inquiry}

                Contact Person:
                {st.session_state.person_name} from {st.session_state.customer_name} reached out with this request. Use all available information to provide the best possible support.

                The contact person from {st.session_state.customer_name} is {st.session_state.person_name}. 
                Use all available resources to provide a complete and accurate response.

                A thorough and informative response that covers all aspects of the inquiry.
                The response should be well-referenced, complete, and delivered in a clear, friendly manner.
                """
            )

            # Save the inquiry and response
            st.session_state.inquiries_and_responses.append({
                'customer_name': st.session_state.customer_name,
                'person_name': st.session_state.person_name,
                'inquiry': inquiry,
                'response': response
            })

            # Display the response with a centered subheader
            st.markdown("<h2 style='text-align: center;'>JBS Support Response</h2>", unsafe_allow_html=True)
            st.markdown(response)
            st.session_state.response = response  # Store the response in session state

        except Exception as e:  # Catch any unexpected errors
            st.error(f"An error occurred: {e}")
            st.session_state.response = ""  # Reset response if error occurs

    else:
        st.warning("Please fill out all fields to submit the inquiry.")

# Contact section (centered)
st.markdown("<h3 style='text-align: center;'>Contact</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Customer Care Center , Tel (KHI) : +92 (21) 111-527-527 , ext: 3263 & 3264| d: +92 (21) 34373100</p>", unsafe_allow_html=True) 
