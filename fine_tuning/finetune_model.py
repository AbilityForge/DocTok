from openai import OpenAI
import os
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class FineTuningPipeline:
    def __init__(self, api_key):
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key)


    def upload_training_file(self, jsonl_file_path):
        """Uploads the JSONL file to OpenAI's servers for fine-tuning."""
        with open(jsonl_file_path, "rb") as file:
            response = self.client.files.create(
                file=file,
                purpose="fine-tune"
            )
        # Get the file ID from the upload response
        return response.id

    def create_fine_tuning_job(self, file_id, model, n_epochs=4):
        """Creates a fine-tuning job using the uploaded file."""
        fine_tune_response = self.client.fine_tuning.jobs.create(
            training_file=file_id,
            model=model,
            hyperparameters={
                "n_epochs": n_epochs,
                "batch_size": 4
            }
        )
        # Get the fine-tuning job ID
        return fine_tune_response.id

    def get_fine_tune_job_status(self, job_id):
        """Retrieves the status of the fine-tuning job."""
        job = self.client.fine_tuning.jobs.retrieve(job_id)
        return job.status

    def monitor_fine_tune_job(self, job_id):
        """Monitors the fine-tuning job until it is finished."""
        while True:
            status = self.get_fine_tune_job_status(job_id)
            st.write(f"Job Status: {status}")
            if status in ["succeeded", "failed"]:
                break
            time.sleep(30)  # Wait for 30 seconds before checking again

        # Retrieve the model ID from the completed job
        fine_tune_job = self.client.fine_tuning.jobs.retrieve(job_id)
        return fine_tune_job.fine_tuned_model

    def fine_tune(self, model="gpt-4o-mini-2024-07-18", n_epochs=4):
        """The main pipeline to upload, fine-tune, and return job ID."""
        # Step 1: Upload the JSONL file
        file_id = self.upload_training_file("dataset/data/output.jsonl")
        
        # Step 2: Create a fine-tuning job
        job_id = self.create_fine_tuning_job(file_id, model, n_epochs)
        
        finetuned_model = self.monitor_fine_tune_job(job_id)

        # Step 3: Return the job ID
        return finetuned_model

# Example usage:

# jsonl_file_path = "dataset/data/output.jsonl"

# pipeline = FineTuningPipeline(api_key)
# job_id = pipeline.fine_tune(jsonl_file_path)
# print("Fine-Tuning Job ID:", job_id)

# If you want to monitor the job:
# fine_tuned_model_id = pipeline.monitor_fine_tune_job(job_id)
# print("Fine-Tuned Model ID:", fine_tuned_model_id)

# completion = client.completions.create(
#     model=fine_tuned_model,
#     prompt="Translate English to French: 'What time is it?'",
# )

# print("Response:", completion.choices[0].text.strip())

# pipeline.monitor_fine_tune_job(job_id)