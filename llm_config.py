"""One place to choose the models - like application.properties in Spring.
Every course file imports from here, so you switch models by editing only this file.
"""

# Chat model: llama3.2 (3B) on your laptop's CPU.
# num_gpu 0 stops Ollama using the graphics chip, which produced garbled answers on your laptop.
MODEL = "llama3.2"
OPTIONS = {"num_gpu": 0}

# Embedding model (Chapter 2): turns text into a list of numbers. Small: about 270 MB.
# Get it once with:  ollama pull nomic-embed-text
EMBED_MODEL = "nomic-embed-text"
