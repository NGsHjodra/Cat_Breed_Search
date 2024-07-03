import torch
from transformers import CLIPProcessor, CLIPModel
import faiss
import os
from PIL import Image
import streamlit as st

device = None
model = None
processor = None
index = None
image_paths = []
titles = []

def boot():
    global device, model, processor, index, image_paths, titles
    # Load the CLIP model and processor
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    # Load Faiss index
    index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'faiss_index.bin'))
    index = faiss.read_index(index_path)
    
    # Load image paths and titles
    image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'images'))
    for breed in os.listdir(image_dir):
        breed_dir = os.path.join(image_dir, breed)
        if os.path.isdir(breed_dir):
            for img_file in os.listdir(breed_dir):
                if img_file.endswith(('.jpg', '.jpeg', '.png')):
                    image_paths.append(os.path.join(breed_dir, img_file))
                    titles.append(breed)
    print("Model and data loaded")

def query(text_input, k=5):
    global device, model, processor, index, image_paths, titles

    print("Querying...")

    # Process text input with CLIP processor
    text_inputs = processor(text=[text_input], return_tensors="pt", padding=True).to(device)
    text_features = model.get_text_features(**text_inputs).cpu().detach().numpy()
    
    # Search for the top k most relevant images in the Faiss index
    D, I = index.search(text_features, k=k)

    # return the top k image paths
    return [image_paths[i] for i in I[0]]