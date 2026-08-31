# Rawi AI

AI-powered digital storyteller for exploring Jordanian landmarks.

## Project Overview

Rawi AI is an AI-powered tourism project designed to help users discover and explore Jordanian landmarks through:

- Image recognition
- AI-generated tourism stories
- Multilingual support
- RAG-based question answering
- Query rewriting for conversational questions
- Text-to-speech (TTS)
- Landmark facts and visitor information

The system identifies a Jordanian landmark from an image and provides the user with an interactive tourism experience based on the available knowledge and facts.

# Dataset

Rawi AI uses a 11-class Jordanian landmark object detection dataset.

- Platform: Roboflow
- Version: v2
- Images: 9,224
- Task: Object Detection
- Classes: 11

The dataset is versioned and maintained on Roboflow.

[Access the dataset on Google Drive](https://drive.google.com/drive/folders/1pDovvJ5REy389dnDrNwFO1loHhx2XX0j?usp=sharing)


## Preprocessing

The dataset was preprocessed using Roboflow.

### Preprocessing

- Auto-Orient: Applied
- Resize: Stretch to 640x640
- Grayscale: Applied

### Augmentations

- Outputs per training example: 3
- Flip: Horizontal
- Crop: 0% Minimum Zoom, 20% Maximum Zoom
- Rotation: -15° to +15°
- Grayscale: Applied to 15% of images
- Hue: -15° to +15°
- Exposure: -10% to +10%
- Blur: Up to 3px
- Noise: Up to 1% of pixels
- Mosaic: Applied

### Bounding Box Augmentations

- Flip: Horizontal
- Crop: 0% Minimum Zoom, 20% Maximum Zoom
- Rotation: -15° to +15°
- Brightness: -15% to +15%
- Exposure: -10% to +10%
- Blur: Up to 2.5px
- Noise: Up to 0.1% of pixels

## AI Components

### Object Detection

The object detection model identifies the selected Jordanian landmark from an input image.

### Story Generation

Rawi generates a natural tourism narration using the available landmark facts.

Stories support:
- Arabic
- English
- French

Three story lengths are available:

- Short: 60–90 words
- Medium: 100–140 words
- Long: 180–250 words

The story generation prompt is available in:

`prompts/generate_story_facts.md`

### RAG Question Answering

Rawi uses a Retrieval-Augmented Generation (RAG) system to answer user questions about the detected landmark.

The RAG knowledge base is stored in:

`knowledge_rag.md`


### Query Rewriting

The system can rewrite conversational questions into standalone questions before retrieving information.

For example, a follow-up question such as:

> When was it built?

can be rewritten into a complete question referring to the detected landmark.
The query rewriting prompt is stored in:

`prompts/query_rewriting.md`

### Answer Generation

After retrieving relevant information, Rawi generates the final answer using the retrieved context.

The answer generation prompt is stored in:

`prompts/answer_generation.md`


### Text-to-Speech

Generated stories and responses can be converted into speech using the project's TTS component.

## Knowledge and Facts

The project separates different types of information:
- `knowledge_rag.md` — human-readable RAG knowledge base.
- `generate_story_facts.md` — documentation of the facts used for story generation.
- `info_labels.py` — multilingual labels used to display landmark information.

## Prompt Files

The prompts are organized separately under:

```text
prompts/
├── generate_story_facts.md
├── query_rewriting.md
└── answer_generation.md
```

## Project Status

Under development — 2026
