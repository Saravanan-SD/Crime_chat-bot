import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from schema import schema, CYPHER_GENERATION_TEMPLATE

# Load environment variables from a .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
URL= os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv('NEO4J_PASSWORD')

# Initialize the Neo4j graph connection
graph = Neo4jGraph(URL, USERNAME, PASSWORD)
graph.refresh_schema()

# Initialize the QA chain
CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

# Initialize the chain
chain = GraphCypherQAChain.from_llm(
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    llm=ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-0125"),
    graph=graph,
    verbose=True
)
# Page Config
st.set_page_config("Crime Chatbot!", page_icon=":cop:")

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm Crime Chatbot! How can I help you?"},
    ]

def write_message(role, content, save = True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)

# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Submit handler
def handle_submit(user_input):
    """
    Submit handler: Talks with an LLM and provides context using data from Neo4j.
    """
    with st.spinner('Thinking...'):
        response = chain.run(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        write_message('assistant', response)

# Handle any user input
if user_input := st.chat_input("What is up?"):
    # Display user message in chat message container    
    st.session_state.messages.append({"role": "user", "content": user_input})
    write_message('user', user_input)
    # Generate a response
    handle_submit(user_input)
    
