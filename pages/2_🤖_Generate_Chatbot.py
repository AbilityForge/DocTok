import streamlit as st
from dataset.preprocessing import DataProcessor
from dataset.scrapper import WebScraper
from fine_tuning.finetune_model import FineTuningPipeline
from vector_search.vectordb import PineconeManager
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()



with st.sidebar:
    # Input for OpenAI API Key
    openai_api_key = (st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")) or (os.getenv("OPENAI_API_KEY"))

    # Input for Pinecone API Key
    pinecone_api_key = (st.text_input("Pinecone API Key", key="pinecone_api_key", type="password")) or (os.getenv("PINECONE_API_KEY"))
 
    # Depth of Web Scraper Crawling
    max_depth = (st.number_input("Enter the maximum depth of the web crawling", value=1, min_value=1, step=1)) or (os.getenv("MAX_DEPTH"))

    # Number of epochs
    n_epochs = (st.number_input("Enter the number of epochs to fine-tune", value=1, min_value=1, step=1)) or (os.getenv("EPOCHS_TO_FT"))


    # Links
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[Get a Pinecone API key](https://app.pinecone.io/)"
    "[![Open GitHub](https://img.shields.io/badge/Open-GitHub-blue?logo=github)](https://github.com/JPsToolbox/Doctok)"



# Streamlit UI
st.title("DocTok Chatbot Generator")

# Scraping Section
start_url = st.text_input("Enter the Start URL for Scraping", placeholder="https://langchain-ai.github.io/langgraph")
st.write("This webscrapper is configured for https://langchain-ai.github.io/langgraph & https://docs.smith.langchain.com")



if st.button("Generate ChatBot"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not pinecone_api_key:
        st.info("Please add your Pinecone API key to continue.")
        st.stop()


    scraper = WebScraper(start_url, max_depth=int(max_depth))
    scraped_data = scraper.web_scraping_pipeline()
    if not scraped_data.empty:
        st.success(f"Scraping completed!")
        st.dataframe(scraped_data, use_container_width=True)

        processor = DataProcessor(api_key=openai_api_key)
        processed_data, processed_ds = processor.process_data(scraped_data)

        if processed_data:
            df_processed = pd.DataFrame(processed_ds)
            df_processed['content'] = df_processed['heading'] + " " + df_processed['text']
            st.success("Fine Tuning Dataset Created")
            st.dataframe(df_processed, use_container_width=True)
            processor.save_to_jsonl(processed_data, 'dataset/data/output.jsonl')
            st.write("Creating Vector Database......")
            pinecone_manager = PineconeManager(api_key=pinecone_api_key, openai_key=openai_api_key, index_name='doctok-index')
            pinecone_manager.upsert_dataframe(df_processed)
            st.write("fine-tuning model......")
            pipeline = FineTuningPipeline(api_key=openai_api_key)
            fine_tuned_models = pipeline.fine_tune(n_epochs=n_epochs)
            st.success("Fine Tuning Completed")
            st.write("Fine-tuned model ID: ", fine_tuned_models)
  

        else:
            st.error("Dataset could not be created.")

        

