import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone





load_dotenv()








with st.sidebar:
    # Input for OpenAI API Key
    openai_api_key = (st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")) or (os.getenv("OPENAI_API_KEY"))

    # Input for Pinecone API Key
    pinecone_api_key = (st.text_input("Pinecone API Key", key="pinecone_api_key", type="password")) or (os.getenv("PINECONE_API_KEY"))

    # Input for Chatbot ID
    chatbot_id = (st.text_input("Chatbot ID", key="chatbot_id")) or (os.getenv("CHAT_BOT_ID"))

    # Links
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[Get a Pinecone API key](https://app.pinecone.io/)"
    "[![Open GitHub](https://img.shields.io/badge/Open-GitHub-blue?logo=github)](https://github.com/JPsToolbox/Doctok)"








st.title("DocTok Chatbot: Chat Interface")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am your DocTok Chatbot. How can I help?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not pinecone_api_key:
        st.info("Please add your Pinecone API key to continue.")
        st.stop()

    if not chatbot_id:
        st.info("Please add your Chatbot ID to continue.")
        st.stop()

    
    client = OpenAI(api_key=openai_api_key)                    
    st.session_state.messages.append({"role": "user", "content": f"{prompt}"})
    st.chat_message("user").write(prompt)

    index_name = "doctok-index"
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(index_name)  

    with st.chat_message("assistant"):
        embeded_prompt = OpenAIEmbeddings(model="text-embedding-ada-002").embed_query(prompt)
        contexts = index.query(
                                vector=embeded_prompt,
                                top_k=3,
                                include_values=False,
                                include_metadata=True
                            )
        context_matches =[match['metadata']['content'] for match in contexts['matches']]
        context_str = "\n".join(context_matches)

        prompt_template = f"""
                            Context:
                            {context_str}

                            Please provide clear, easy-to-understand, and accurate information for the 
                            following question/request, refer to the context given above if necessary. :

                            {prompt}

                            
                            """
        

        
        completion = client.chat.completions.create(model=chatbot_id,
                                                    messages=[
                                                        {
                                                            "role": "user",
                                                            "content": f"{prompt_template}",
                                                        }
                                                    ])
        response = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)


    