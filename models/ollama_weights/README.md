# Model Weights Directory

This directory is for storing pretrained model weights when using local models.

## Ollama Models

When using Ollama, models are typically stored in Ollama's cache directory, not here.
This directory serves as a placeholder for custom model weights if needed.

## Usage

1. If using Ollama (recommended), no files are needed here
2. For custom models, place your model files here:
   - config.json (model configuration)
   - tokenizer.model (tokenizer)
   - model.bin or model.safetensors (model weights)

## Note

Large model files (*.bin, *.safetensors) are excluded from git via .gitignore.
