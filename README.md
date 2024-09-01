# Doctok
DocTok: Creating Chatbots for Technical Documentation

[APP](https://ability-forge-doctok.streamlit.app/)

## Overview

**DocTok** is an innovative solution designed to improve the way users interact with technical documentation. Traditional methods of searching through manuals, guides, or extensive documentation often prove time-consuming and inefficient. DocTok addresses this challenge by transforming static documents into a dynamic conversational experience, allowing users to query documents as they would in a natural conversation.

## Table of Contents

- [Project Overview](#overview)
- [Objectives and Motivation](#objectives-and-motivation)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Architecture](#project-architecture)
- [Developer Information](#developer-information)
- [Future Development](#future-development)

## Objectives and Motivation

### Primary Objective

The primary objective of DocTok is to provide real-time, conversational access to dense technical documents. This allows users to effortlessly retrieve and understand information, significantly reducing the cognitive load and time required to navigate through complex documentation.

### Motivation

The motivation for this project stemmed from the challenges faced by professionals in fields like engineering, IT, and academia, where quick and precise access to information is critical. DocTok aims to bridge the gap between vast technical data and user accessibility.

## Features

- **Conversational AI**: DocTok simulates human-like conversations, understanding the context of a user’s query and generating appropriate responses based on the content of the document.
- **Generative AI and RAG Mechanism**: Utilizes advanced Generative AI and Retrieval-Augmented Generation (RAG) techniques to ensure responses are accurate and grounded in the actual content of the documents.
- **Integration with LLMs and LangChain**: Leverages Large Language Models (LLMs) and integrates with LangChain to handle complex technical language and dynamic querying.
- **User-Friendly Interface**: A web-based UI developed using Streamlit, offering a seamless and intuitive experience for querying technical documents.

## Installation

### Prerequisites

- Python 3.7+
- Pip

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/doctok.git
   cd doctok
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run Home.py
   ```

## Usage

After running the Streamlit application, the DocTok home page will be accessible through your web browser. The home page provides an introduction to the project and its objectives. Users can interact with the chatbot by inputting document URLs for processing and querying specific technical information through the conversational interface.

## Project Architecture

The architecture of DocTok includes the following components:

- **Frontend**: Developed using Streamlit, providing an intuitive interface for users to interact with the chatbot and manage documents.
- **Backend**: Handles document ingestion, preprocessing, and response generation using fine-tuned GPT-4 models.
- **Database**: Utilizes Pinecone for vector storage, enabling quick retrieval of relevant document sections during conversations.



## Future Development

Future plans for DocTok include:

- Expanding the range of documents covered by the chatbot.
- Adding support for multiple languages.
- Integrating with additional AI tools, such as voice assistants, to further enhance user interaction.
- Improving the accuracy and efficiency of response generation through continuous model fine-tuning.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

