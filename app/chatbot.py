import os
import torch
from nati.config_manager import ConfigManager

# Try importing both backends
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

try:
    from ctransformers import AutoModelForCausalLM
except ImportError:
    AutoModelForCausalLM = None

# Load model name from config
config = ConfigManager()
model_name = config.get('ai.chat_model')
model_path = os.path.join('models', model_name)
print(f"Model path: {model_path}")

# Determine device safely
try:
    if torch.cuda.is_available():
        device = 0
        print("CUDA is available. Using GPU.")
    else:
        device = -1
        print("CUDA not available. Using CPU.")
except Exception as e:
    print(f"Error checking CUDA availability: {e}")
    device = -1
    print("Defaulting to CPU.")

chatbot = None
backend = None

# Helper to detect if a path contains a GGUF file
def is_gguf_model(path):
    for filename in os.listdir(path):
        if filename.endswith('.gguf'):
            return filename
    return None

# Try loading model
try:
    gguf_file = is_gguf_model(model_path)
    if gguf_file:
        print(f"Detected GGUF model: {gguf_file}")
        if AutoModelForCausalLM is None:
            raise ImportError("ctransformers not installed. Cannot load GGUF models.")

        chatbot = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_file=gguf_file,
            model_type="falcon",  # default fallback; you can adjust per model type later
            gpu_layers=50 if device == 0 else 0  # use GPU if available
        )
        backend = 'ctransformers'
    else:
        print(f"Detected Huggingface model structure.")
        if pipeline is None:
            raise ImportError("transformers not installed. Cannot load Huggingface models.")

        chatbot = pipeline("text-generation", model=model_path, device=device)
        backend = 'transformers'

except Exception as e:
    print(f"Model load failed: {e}")
    chatbot = None
    backend = None

# Chatbot response function
def get_bot_response(message):
    if chatbot is None:
        return "Model failed to load."

    prompt = f"""You are NATI, a helpful assistant for infrastructure, AI, and tooling.

User: {message}
NATI:"""

    try:
        if backend == 'transformers':
            result = chatbot(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
            return result[0]['generated_text'].split("NATI:")[-1].strip()
        elif backend == 'ctransformers':
            result = chatbot(prompt, max_new_tokens=150, temperature=0.7)
            return result
        else:
            return "Unknown backend."

    except Exception as e:
        print(f"Error during chatbot generation: {e}")
        return "Error generating response."
