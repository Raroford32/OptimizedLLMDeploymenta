import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import sanitize_input, format_cpp_code

# Load the model and tokenizer
model_name = "gpt2"  # Using GPT-2 as a smaller, publicly available model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_code(project_description, max_tokens=500):
    # Sanitize input
    sanitized_description = sanitize_input(project_description)
    
    # Prepare the prompt
    prompt = f"Generate a C++ project based on the following description:\n{sanitized_description}\n\nC++ code:"
    
    # Tokenize the input
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Create attention mask
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
    
    # Generate the code
    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=input_ids.shape[1] + max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=model.config.eos_token_id  # Set pad_token_id to eos_token_id
        )
    
    # Decode the generated text
    generated_code = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Extract and format the C++ code
    cpp_code = generated_code.split("C++ code:")[1].strip() if "C++ code:" in generated_code else generated_code
    formatted_code = format_cpp_code(cpp_code)
    
    return formatted_code
