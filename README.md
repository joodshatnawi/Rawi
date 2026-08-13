# Rawi AI

AI-powered digital storyteller for exploring Jordanian landmarks.

## Project Overview

Rawi AI is an AI-powered tourism project designed to help users discover and explore Jordanian landmarks through interactive stories, fun facts, image recognition, and AI-powered conversations.

# Dataset

Rawi AI uses a 9-class Jordanian landmark object detection dataset.

- Platform: Roboflow
- Version: v2
- Images: 9,224
- Task: Object Detection
- Classes: 9
Preprocessing

The dataset was preprocessed using Roboflow.

Preprocessing
Auto-Orient: Applied
Resize: Stretch to 640x640
Grayscale: Applied
Augmentations
Outputs per training example: 3
Flip: Horizontal
Crop: 0% Minimum Zoom, 20% Maximum Zoom
Rotation: -15° to +15°
Grayscale: Applied to 15% of images
Hue: -15° to +15°
Exposure: -10% to +10%
Blur: Up to 3px
Noise: Up to 1% of pixels
Mosaic: Applied
Bounding Box Augmentations
Flip: Horizontal
Crop: 0% Minimum Zoom, 20% Maximum Zoom
Rotation: -15° to +15°
Brightness: -15% to +15%
Exposure: -10% to +10%
Blur: Up to 2.5px
Noise: Up to 0.1% of pixels

## Project Status

Under development —  2026
