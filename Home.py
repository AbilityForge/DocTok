import streamlit as st

# Set the title of the web page
st.title("DocTok: Technical Documentation Chatbot Generator")

# Add an introduction section
st.header("Introduction")
st.write("""
**DocTok** is designed to improve how users interact with technical documentation. 
Traditional methods of searching through manuals, guides, or extensive documentation often prove time-consuming and inefficient. 
DocTok addresses this by transforming static documents into a dynamic conversational experience.

The project originated from the need to bridge the gap between vast technical data and user accessibility, focusing on 
creating a seamless interface where users can query documents as they would in a conversation.
""")

# Add the project objectives
st.header("Objectives and Motivation")
st.write("""
**Primary Objective:** To provide real-time, conversational access to dense technical documents, allowing users to retrieve 
and understand information effortlessly.

**Motivation:** The motivation stemmed from the challenges faced by professionals in fields like engineering, IT, and academia, 
where quick and precise access to information is critical. The project aims to reduce the cognitive load and time required to 
navigate through complex documentation.
""")

# Add personal details
st.header("Project By")
st.write("**Name:** Parva J Shah")
st.write("**NUID:** 002916822")

# Add footer or any other information you'd like to include
st.write("For more information, explore the different sections of this application.")
