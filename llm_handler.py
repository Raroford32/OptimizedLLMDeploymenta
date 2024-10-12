from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Initialize the model and tokenizer
model_name = "distilgpt2"  # A smaller model that can run on CPU
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # -1 means CPU

def generate_code(prompt):
    # Generate text based on the prompt
    generated_text = generator(prompt, max_length=500, num_return_sequences=1)[0]['generated_text']

    # Parse the generated text into multiple files
    files = {}
    current_file = None
    current_content = []

    for line in generated_text.split('\n'):
        if line.startswith('## file:'):
            if current_file:
                files[current_file] = '\n'.join(current_content)
            current_file = line[8:].strip()
            current_content = []
        else:
            current_content.append(line)

    if current_file:
        files[current_file] = '\n'.join(current_content)

    return files
