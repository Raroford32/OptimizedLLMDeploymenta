import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import sanitize_input, format_cpp_code
import os
import gc
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load a smaller model
model_name = "EleutherAI/gpt-neo-1.3B"  # Using a smaller model for demonstration
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Implement model loading with memory optimization and model parallelism
def load_model():
    try:
        # Initialize an empty model
        with init_empty_weights():
            model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
        
        # Load the model weights and distribute across available GPUs
        model = load_checkpoint_and_dispatch(
            model,
            model_name,
            device_map="auto",
            no_split_module_classes=["GPTNeoBlock"],
            dtype=torch.float16
        )
        print("Model loaded with Accelerate in half precision")
    except Exception as e:
        print(f"Error loading model with Accelerate: {e}")
        print("Loading full model without optimization")
        model = AutoModelForCausalLM.from_pretrained(model_name)
    return model

model = load_model()

# Implement GPU memory management
def clear_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()
    print(f"Current GPU memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

def generate_code(project_description, max_tokens=500):
    clear_gpu_memory()
    
    # Sanitize input
    sanitized_description = sanitize_input(project_description)
    
    # Prepare the prompt
    prompt = f"Generate a C++ project based on the following description:\n{sanitized_description}\n\nC++ code:"
    
    # Tokenize the input
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    
    # Create attention mask
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=device)
    
    # Generate the code
    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=input_ids.shape[1] + max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the generated text
    generated_code = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Extract and format the C++ code
    cpp_code = generated_code.split("C++ code:")[1].strip() if "C++ code:" in generated_code else generated_code
    formatted_code = format_cpp_code(cpp_code)
    
    clear_gpu_memory()
    return formatted_code

# Set the number of GPUs to use (if available)
os.environ["CUDA_VISIBLE_DEVICES"] = ",".join([str(i) for i in range(torch.cuda.device_count())])

print("LLM integration module loaded successfully with advanced hardware optimization")
