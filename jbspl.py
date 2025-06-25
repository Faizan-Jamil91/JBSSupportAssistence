import streamlit as st
import datetime
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page configuration with professional branding
st.set_page_config(
    page_title="JBS Support Portal",
    page_icon=":technologist:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://jbs.live/support',
        'Report a bug': "mailto:customercare@jbs.live",
        'About': "JBS Support Assistant v2.1"
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .header { 
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    .response-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .history-item {
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #3498db;
        background-color: #f1f8ff;
    }
    .contact-bar {
        background-color: #2c3e50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    .stButton>button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 8px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# Define the title and header with professional styling
st.markdown("<h1 class='header' style='text-align: center;'>JBS Customer Support Portal</h1>", unsafe_allow_html=True) 

# Welcome message
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <p>Welcome to the JBS Support Assistant. Submit your inquiry below for comprehensive assistance.</p>
    <p><em>All inquiries are processed securely and confidentially</em></p>
</div>
""", unsafe_allow_html=True)

# Get the current date
current_date = datetime.datetime.now().date()
target_date = datetime.date(2024, 6, 12)

# Set the model variable (using more consistent naming)
llm_model = "gemini-2.0-flash"  # Maintained for future date logic

# API Key Management
os.environ["GOOGLE_API_KEY"] = "AIzaSyCYyo69R1YhYArdTbs765WTi70-93D0r4Y"

# Initialize LLM and Memory
llm = ChatGoogleGenerativeAI(
    temperature=0.0, 
    model=llm_model,
    max_output_tokens=2048
)
memory = ConversationBufferMemory()

# Create ConversationChain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# Session State Initialization
session_defaults = {
    'customer_name': "",
    'person_name': "",
    'inquiry': "",
    'inquiry_history': [],
    'inquiries_and_responses': [],
    'submitted': False
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Function to display chat history professionally
def display_chat_history():
    if not st.session_state.inquiries_and_responses:
        st.info("No conversation history yet. Submit your first inquiry to begin.")
        return
        
    for i, entry in enumerate(st.session_state.inquiries_and_responses):
        with st.expander(f"Inquiry #{i+1} - {entry['customer_name']}", expanded=False):
            st.markdown(f"**Customer:** {entry['customer_name']}")
            st.markdown(f"**Contact:** {entry['person_name']}")
            st.markdown(f"**Inquiry:**\n{entry['inquiry']}")
            st.markdown(f"**Response:**\n{entry['response']}")
            st.markdown(f"<small>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</small>", 
                       unsafe_allow_html=True)

# Main layout columns
left_col, right_col = st.columns([1, 2], gap="large")

# History Panel
with left_col:
    st.markdown("<h3 style='text-align: center;'>Conversation History</h3>", unsafe_allow_html=True)
    display_chat_history()

# Inquiry Form
with right_col:
    st.markdown("<h3 style='text-align: center;'>New Support Request</h3>", unsafe_allow_html=True)
    
    with st.form(key="support_form", clear_on_submit=True):
        cols = st.columns(2)
        with cols[0]:
            customer = st.text_input("Customer Organization", 
                                   value=st.session_state.customer_name,
                                   placeholder="Company Name")
        with cols[1]:
            contact = st.text_input("Contact Person", 
                                  value=st.session_state.person_name,
                                  placeholder="Your Name")
        
        inquiry = st.text_area("Detailed Inquiry", 
                             height=200,
                             placeholder="Describe your issue or question in detail...",
                             value=st.session_state.inquiry)
        
        submitted = st.form_submit_button("Submit Request")
        
        if submitted:
            if not customer or not contact or not inquiry:
                st.error("Please complete all fields before submitting")
            else:
                st.session_state.customer_name = customer
                st.session_state.person_name = contact
                st.session_state.inquiry = inquiry
                st.session_state.submitted = True

# Process submission
if st.session_state.submitted:
    with st.spinner("Analyzing your inquiry and preparing response..."):
        try:
            # Build structured prompt
            prompt = f"""
            ## JBS SUPPORT REQUEST
            
            **Customer Organization:** {st.session_state.customer_name}
            **Contact Person:** {st.session_state.person_name}
            
            ### INQUIRY DETAILS:
            {st.session_state.inquiry}
            
            ### RESPONSE GUIDELINES:
            1. Provide first-level support resolution
            2. Address all aspects of the inquiry thoroughly
            3. Reference relevant knowledge base articles if applicable
            4. Maintain professional yet approachable tone
            5. Clearly explain technical concepts
            6. Include official support contacts when appropriate
            7. Structure response with clear sections
            
            ### PAST INQUIRIES CONTEXT:
            {st.session_state.inquiry_history[-3:] if st.session_state.inquiry_history else 'No prior inquiries'}
            
            ### REQUIRED OUTPUT FORMAT:
            **JBS Support Response**\n\n
            [Comprehensive response here]\n\n
            **Support Resources:**\n
            Email: customercare@jbs.live | 
            Web: https://jbs.live | 
            Phone: +92 (21) 111-527-527 (Ext: 3263, 3264) | 
            Direct: +92 (21) 34373100

            """
            
            # Generate response
            response = conversation.run(input=prompt)
            
            # Store interaction
            st.session_state.inquiry_history.append(st.session_state.inquiry)
            st.session_state.inquiries_and_responses.append({
                'customer_name': st.session_state.customer_name,
                'person_name': st.session_state.person_name,
                'inquiry': st.session_state.inquiry,
                'response': response
            })
            
            # Display response
            st.success("Response generated successfully!")
            st.markdown("<div class='response-box'>", unsafe_allow_html=True)
            st.markdown(f"**JBS Official Response**")
            st.markdown("---")
            st.markdown(response)
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Response generation failed: {str(e)}")
            st.error("Please try again or contact support directly")
            
    st.session_state.submitted = False

# Professional contact footer
st.markdown("""
<div class='contact-bar'>
    <strong>JBS Customer Support</strong> | 
    Email: customercare@jbs.live | 
    Web: https://jbs.live | 
    Phone: +92 (21) 111-527-527 (Ext: 3263, 3264) | 
    Direct: +92 (21) 34373100
</div>
""", unsafe_allow_html=True)
