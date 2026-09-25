# Rawi AI - The Jordanian Digital Storyteller

**AI-powered smart tourist guide for exploring Jordanian landmarks.**

Rawi AI is an AI-powered tourism application designed to help visitors discover and explore Jordanian landmarks through computer vision, generative AI, Retrieval-Augmented Generation (RAG), multilingual support, and text-to-speech.

The system identifies a landmark from an input image, provides an AI-generated tourism story, presents factual visitor information, and allows users to ask questions through Rawi Chat.

---

## Project Overview

Rawi AI integrates multiple AI technologies into a single tourism-oriented application:

* Image recognition using YOLO11m
* AI-generated tourism stories
* Multilingual support in Arabic, English, and French
* Retrieval-Augmented Generation (RAG)
* Conversational question answering
* Query rewriting
* Text-to-speech (TTS)
* Interactive maps and landmark locations
* Landmark facts and visitor information
* Hybrid story generation using cached and dynamically generated stories

The system is designed to provide visitors with an interactive digital guide that combines landmark recognition, factual information, contextual storytelling, and conversational assistance.

---

## Supported Jordanian Landmarks

Rawi AI currently recognizes 11 Jordanian landmarks:

1. Ajloun Castle
2. Al-Maghtas
3. Dead Sea
4. Jerash
5. Karak Castle
6. Petra
7. Qasr Amra
8. Umm Al-Jimal
9. Umm Qais
10. Wadi Mujib
11. Wadi Rum

---

## System Workflow

```text
User
  |
  v
Upload / Capture Image
  |
  v
YOLO11m Landmark Detection
  |
  v
Detected Landmark
  |
  +-------------------------+
  |                         |
  v                         v
Landmark Information    Story Generation
                              |
                        +-----+-----+
                        |           |
                        v           v
                     Cache      GPT-OSS 120B
  |                         |
  +------------+------------+
               |
               v
          Result Page
               |
       +-------+-------+-------+
       |               |       |
       v               v       v
     Story           Facts    Map
       |
       v
      TTS
       |
       v
    Audio Guide


Rawi Chat
    |
    v
User Question
    |
    v
Query Rewriting
    |
    v
FAISS Retrieval
    |
    v
Retrieved Context
    |
    v
GPT-OSS 20B
    |
    v
Generated Answer
```

---

## Object Detection

Rawi AI uses a YOLO11m object detection model to identify Jordanian landmarks from input images.

The trained model contains:

* **20,038,513 parameters**
* **67.8 GFLOPs**
* **50 training epochs**
* **Tesla T4 GPU**
* Approximately **5.27 hours** of training time

The model detects the landmark present in the input image and returns the corresponding landmark class and detection confidence.

---

## Dataset

The Rawi AI object detection dataset contains **14,494 images** and **38,186 object instances** across 11 Jordanian landmark classes.

| Split      |     Images | Object Instances |
| ---------- | ---------: | ---------------: |
| Train      |     12,990 |           36,682 |
| Validation |        941 |              941 |
| Test       |        563 |              563 |
| **Total**  | **14,494** |       **38,186** |

### Dataset Preprocessing

The dataset was prepared using the following preprocessing steps:

* Auto-Orient: Applied
* Resize: Stretch to 512 × 512
* Grayscale: Applied

### Data Augmentation

The training dataset includes:

* 3 outputs per training example
* 90° clockwise and counter-clockwise rotation
* Crop with 0% minimum zoom and 20% maximum zoom
* Hue adjustment from -15° to +15°
* Exposure adjustment from -10% to +10%
* Blur up to 2.5 px
* Noise up to 0.1% of pixels
* Mosaic augmentation

Bounding-box augmentations include:

* 90° rotation
* Exposure adjustment
* Blur
* Noise

### Dataset Access

[Access the Rawi AI Dataset](https://drive.google.com/drive/folders/1S6GLnbYDp-BcjjlVQ6u5d5s5VXLlDUgT?usp=sharing)

---

## Model Evaluation

The final YOLO11m model was evaluated on a validation set containing **941 images and 941 object instances**.

| Metric    |     Score |
| --------- | --------: |
| Precision | **98.1%** |
| Recall    | **96.4%** |
| mAP@50    | **98.7%** |
| mAP@50-95 | **98.6%** |

### Per-Class Performance

| Landmark      | Precision | Recall | mAP@50 | mAP@50-95 |
| ------------- | --------: | -----: | -----: | --------: |
| Ajloun Castle |     94.6% |  96.3% |  98.4% |     98.1% |
| Al-Maghtas    |     98.9% |  95.7% |  99.4% |     99.2% |
| Dead Sea      |     98.2% | 100.0% |  99.5% |     99.5% |
| Jerash        |     98.7% |  99.2% |  99.5% |     99.0% |
| Karak Castle  |     98.2% |  94.0% |  98.1% |     98.1% |
| Petra         |    100.0% |  97.1% |  99.5% |     99.5% |
| Qasr Amra     |     97.7% |  97.9% |  99.3% |     98.5% |
| Umm Al-Jimal  |     99.9% |  96.9% |  99.2% |     99.2% |
| Umm Qais      |     97.2% |  89.5% |  95.8% |     95.8% |
| Wadi Mujib    |     98.8% |  94.3% |  98.0% |     98.0% |
| Wadi Rum      |     96.4% |  99.1% |  99.4% |     99.4% |

> Note: The reported metrics are validation results. The test set contains 563 images and has not been used for the metrics reported above.

### Confusion Matrix

The normalized confusion matrix presents the detection behavior across the 11 landmark classes and highlights classification errors and missed detections.

![YOLO11m Confusion Matrix](evaluation/confusion_matrix_normalized.png)

---

## AI Story Generation

After detecting a landmark, Rawi AI generates a tourism-oriented story describing the location.

The story generation system uses:

**`openai/gpt-oss-120b`**

Stories are available in:

* English
* Arabic
* French

### Story Lengths

| Length | Target        |
| ------ | ------------- |
| Short  | 70-80 words   |
| Medium | 110-130 words |
| Long   | 160-190 words |

The story-generation prompts are designed to produce:

* Natural tourism narration
* Factual landmark information
* Text-to-speech-friendly content
* Language-specific output
* No unsupported facts
* No unnecessary speculation

---

## Hybrid Story Generation

Rawi AI uses a hybrid approach to improve response speed and reliability.

Pre-generated stories are stored in:

```text
stories_cache.json
```

The cache contains:

```text
11 landmarks
× 3 languages
× 3 story lengths
= 99 pre-generated stories
```

When a matching story is available, Rawi AI can use the cached version instead of generating a new response.

If a suitable cached story is unavailable, the system can generate a new story dynamically.

---

## Rawi Chat

Rawi Chat allows users to ask questions about Jordanian landmarks using natural language.

The chatbot uses a Retrieval-Augmented Generation architecture.

### RAG Pipeline

```text
User Question
      |
      v
Query Rewriting
      |
      v
FAISS Retrieval
      |
      v
Relevant Landmark Context
      |
      v
Answer Generation
      |
      v
Final Answer
```

The RAG system uses:

* FAISS for vector retrieval
* `intfloat/multilingual-e5-base` for embeddings
* `openai/gpt-oss-20b` for answer generation

The knowledge base is organized into landmark-specific information including:

* Overview
* History
* Facts
* Landmarks
* Landmark Details
* Tourism information

The current RAG knowledge base contains **420 indexed chunks** covering the supported landmarks.

---

## Query Rewriting

Before retrieval, the user's question is processed through a query-rewriting stage.

This transforms conversational questions into retrieval-friendly queries and helps maintain context across follow-up questions.

For example:

```text
User:
What about its history?

        |
        v

Query Rewriting

        |
        v

Retrieval query related to
the history of the current landmark
```

This approach helps the retrieval system handle conversational references such as pronouns and follow-up questions.

---

## Retrieval-Augmented Generation

The RAG system retrieves relevant information from the project's local knowledge base before generating an answer.

This allows Rawi Chat to ground its responses in the project's curated tourism data.

The answer-generation prompt instructs the model to:

* Use the retrieved context
* Answer in the requested language
* Avoid unsupported information
* Avoid guessing
* Avoid inventing facts
* Return a fallback response when sufficient information is unavailable

---

## Multilingual Support

Rawi AI supports three languages:

| Language | Support |
| -------- | :-----: |
| English  |   Yes   |
| Arabic   |   Yes   |
| French   |   Yes   |

The selected language affects:

* Landmark names
* AI-generated stories
* Chat responses
* Information labels
* Text-to-speech output

---

## Text-to-Speech

Rawi AI converts generated stories into audio using Text-to-Speech technology.

This allows users to listen to landmark stories while exploring the application.

The feature supports the project's goal of providing an interactive digital tourism-guide experience.

---

## Landmark Information and Maps

After detecting a landmark, Rawi AI displays additional information such as:

* Landmark description
* Historical information
* Construction or historical period
* Governorate
* UNESCO information where applicable
* Best time to visit
* Suggested visit time
* Fun facts
* Historical eras
* Geographic location

An interactive map is also provided to display the landmark's location.

---

## User Interface

Rawi AI is implemented as a Streamlit web application.

The application provides three main experiences.

### Home

Users can:

* Upload an image
* Capture an image
* Select the desired language
* Start exploring a Jordanian landmark

### Result

After detection, users can access:

* Detected landmark
* Detection confidence
* AI-generated story
* Landmark facts
* Location
* Interactive map
* Audio narration

### Rawi Chat

Users can ask questions about Jordanian landmarks and receive context-grounded answers through the RAG pipeline.

---

## Technologies Used

| Component            | Technology                    |
| -------------------- | ----------------------------- |
| Web Application      | Streamlit                     |
| Object Detection     | YOLO11m                       |
| Deep Learning        | PyTorch                       |
| Computer Vision      | Ultralytics                   |
| Story Generation LLM | OpenAI GPT-OSS 120B           |
| RAG LLM              | OpenAI GPT-OSS 20B            |
| Vector Search        | FAISS                         |
| Embeddings           | intfloat/multilingual-e5-base |
| Text-to-Speech       | Edge TTS                      |
| Maps                 | Folium                        |
| Programming Language | Python                        |
| Dataset Platform     | Roboflow                      |
| Deployment           | Streamlit Cloud               |

---

## Project Structure

```text
Rawi/
|
├── app.py
├── model_rawi.py
├── home_page.py
├── result_page.py
├── chat_page.py
├── chat_labels.py
├── info_labels.py
├── rag.py
|
├── facts.json
├── stories_cache.json
|
├── generate_all_stories.py
|
├── best.pt
|
├── prompts/
|   ├── generate_story_facts.md
|   ├── query_rewriting.md
|   └── answer_generation.md
|
├── rag_data/
|   ├── *.index
|   └── *.pkl
|
├── evaluation/
|   └── confusion_matrix_normalized.png
|
└── README.md
```

---

## Configuration

API credentials are stored outside the source code using environment variables.

For example:

```text
GROQ_API_KEY=your_api_key
```

The API key should never be committed to GitHub.

For local development, environment variables can be stored in a `.env` file.

---

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/joodshatnawi/Rawi.git
```

Move into the project directory:

```bash
cd Rawi
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## Deployment

Rawi AI is deployed as a Streamlit web application.

### Live Demo

https://rawi-ai.streamlit.app/

The deployed application provides the Rawi AI experience, including landmark recognition, AI storytelling, multilingual support, RAG-based conversational question answering, landmark information, maps, and text-to-speech.

---

## Project Objectives

The main objectives of Rawi AI are to:

1. Make information about Jordanian landmarks more accessible.
2. Combine computer vision and generative AI in a practical tourism application.
3. Provide multilingual tourism assistance.
4. Deliver contextual and grounded answers through RAG.
5. Provide an interactive alternative to traditional tourism information.
6. Demonstrate the integration of modern AI technologies into a real-world application.

---

## Future Improvements

Potential future improvements include:

* Expanding the number of recognized Jordanian landmarks
* Increasing dataset diversity with additional real-world images
* Further evaluating the model on the unseen test set
* Improving landmark-specific retrieval
* Expanding the multilingual knowledge base
* Adding richer tourism recommendations
* Improving mobile usability
* Adding additional accessibility features
* Exploring advanced deployment and MLOps workflows

---

## Project Status

**Current status: Functional prototype and deployed AI tourism application.**

The current system supports landmark detection across 11 Jordanian landmarks, multilingual AI storytelling, RAG-based conversational question answering, landmark information, interactive maps, and text-to-speech.

---

## Project

**Rawi AI - The Jordanian Digital Storyteller**

Rawi AI combines:

```text
Computer Vision
        +
Generative AI
        +
Retrieval-Augmented Generation
        +
Multilingual NLP
        +
Text-to-Speech
        +
Interactive Web Application
```

The project demonstrates how modern AI technologies can be integrated into a practical application for exploring Jordanian cultural and historical landmarks.
