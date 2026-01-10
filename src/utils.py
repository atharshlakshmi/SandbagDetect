import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from google import genai
from typing import Dict, List

############################################
# GEMINI SETUP
############################################

def call_gemini(prompt: str, model_name: str) -> str:
    try:
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # Initialize client with API key
        client = genai.Client(api_key=api_key)
        
        # Generate content using the new API
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No response generated"
    except Exception as e:
        print(f"Error calling Gemini model: {e}")
        return f"Error: {str(e)}"

############################################
# HUGGING FACE / LOCAL MODELS
############################################

_MODEL_CACHE = {}

def load_hf_model(model_name: str):
    """
    Load and cache Hugging Face / local models
    """
    if model_name not in _MODEL_CACHE:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Set padding token if not present
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
            model.eval()
            _MODEL_CACHE[model_name] = (tokenizer, model)
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            raise
    
    return _MODEL_CACHE[model_name]

def call_hf_model(prompt: str, model_name: str, max_new_tokens: int = 128) -> str:
    """
    Call Hugging Face model with error handling
    """
    try:
        if model_name not in _MODEL_CACHE:
            tokenizer, model = load_hf_model(model_name)
        
        else: 
            tokenizer, model = _MODEL_CACHE[model_name]

        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

        # Decode only the generated part
        input_length = inputs.input_ids.shape[1]
        generated_tokens = outputs[0][input_length:]
        return tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    except Exception as e:
        print(f"Error calling Hugging Face model {model_name}: {e}")
        return f"Error: {str(e)}"
    
############################################
# UNIFIED DISPATCH FUNCTION
############################################

def call_llm(model_name: str, prompt: str, max_new_tokens: int = 128) -> str:
    """
    Unified interface for all models.
    """
    model_name_lower = model_name.lower()

    if model_name_lower.startswith("gemini"):
        return call_gemini(prompt, model_name)
    elif "qwen" in model_name_lower or "llama" in model_name_lower or "deepseek" in model_name_lower:
        return call_hf_model(prompt, model_name, max_new_tokens)
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    
def render_prompt(pair: Dict, context_type: str) -> str:
    """
    Render a prompt from a question pair and context type.
    """
    if context_type == "evaluation_context":
        context = pair.get("evaluation_context", "")
        question = pair.get("question", "")
        
        prompt = f"""{context}

            Question: {question}

            Answer in one sentence only. Be concise and direct."""
    
    elif context_type == "casual_context":
        context = pair.get("casual_context", "")
        question = pair.get("question", "")
        
        # More casual phrasing
        prompt = f"""{context}

            What do you think? Answer in one sentence only."""
    
    else:
        raise ValueError(f"Unknown context type: {context_type}")
    
    return prompt