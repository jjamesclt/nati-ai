from transformers import pipeline

try:
    chatbot = pipeline("text-generation", model="models/falcon-rw-1b", device=0)
except Exception as e:
    import traceback
    print("Model failed to load:")
    traceback.print_exc()
    chatbot = None

def get_bot_response(message):
    if chatbot is None:
        return "Model failed to load."
    prompt = f"""You are NATI, a Network Analytics and Telemetry Interface.

User: {message}
NATI:"""
    result = chatbot(prompt, max_length=240, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].split("NATI:")[-1].strip()
