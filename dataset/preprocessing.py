import pandas as pd
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class DataProcessor:
    def __init__(self, api_key, model_name="gpt-4o-mini", temperature=0):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key)
        self.prompt_template = PromptTemplate.from_template("""
        Given the following heading and text, generate a single question that can be answered using this information:
        
        Heading: {title}
        Text: {text}

        Please provide only the question as the output, without any additional text.
        """)

    def load_data(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.columns = data.columns.str.strip()
            return data
        except Exception as e:
            print(e)

    def generate_question(self, title, text):
        try:
            prompt = self.prompt_template.format(title=title, text=text)
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            return response.content.strip()
        except Exception as e:
            print(e)

    def process_data(self, data):
        processed_data = []
        processed_ds = []
        progress_bar = st.progress(0)  # Initialize the progress bar
        total_rows = len(data)

        for index, row in data.iterrows():
            try:
                question = self.generate_question(row['heading'], row['text'])
                processed_ds.append({
                    "question": question,
                    "heading": f"{row['heading']}",
                    "text": f"{row['text']}"
                }) 
                processed_data.append({
                    "messages": [
                        {"role": "system", "content": "You are an expert programmer with many years of experience"},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": f"{row['heading']} {row['text']}"}
                    ]
                })
                print(f"Processed row successfully: {question}")
            except Exception as e:
                print(f"Failed to process row: {row['heading']}")
                continue

            # Update the progress bar
            progress = (index + 1) / total_rows
            progress_bar.progress(progress)

        progress_bar.empty()  # Remove the progress bar once processing is complete
        return processed_data, processed_ds

    def save_to_jsonl(self, data, output_file_path):
        try:
            with open(output_file_path, 'w') as f:
                for item in data:
                    f.write(json.dumps(item) + '\n')
        except Exception as e:
            print(e)
