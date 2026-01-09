def render_prompt(prompt_pair, context) -> str:
    """
    Formats the prompt for experiments

    Returns:
        str: Formatted string for LLM prompting
    """
    pass

def call_LLM(model, prompt) -> str:
    """
    Calls LLM to run experiments
 
    Returns:
        str: Response from LLM
    """
    pass

# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import google.generativeai as genai

# ############################################
# # GEMINI SETUP
# ############################################

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def call_gemini(prompt: str, model_name: str = "gemini-1.5-flash") -> str:
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content(prompt)
#     return response.text.strip()

# ############################################
# # HUGGING FACE / LOCAL MODELS
# ############################################

# _MODEL_CACHE = {}

# def load_hf_model(model_name: str):
#     """
#     Load and cache Hugging Face / local models
#     """
#     if model_name not in _MODEL_CACHE:
#         tokenizer = AutoTokenizer.from_pretrained(model_name)
#         model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#             device_map="auto"
#         )
#         model.eval()
#         _MODEL_CACHE[model_name] = (tokenizer, model)

#     return _MODEL_CACHE[model_name]

# def call_hf_model(prompt: str, model_name: str, max_new_tokens: int = 128) -> str:
#     tokenizer, model = load_hf_model(model_name)

#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=max_new_tokens,
#         do_sample=False,
#         temperature=0.0
#     )

#     return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# ############################################
# # UNIFIED DISPATCH FUNCTION
# ############################################

# def call_llm(model_name: str, prompt: str) -> str:
#     """
#     Unified interface for all models.
#     """

#     model_name_lower = model_name.lower()

#     if model_name_lower.startswith("gemini"):
#         return call_gemini(prompt, model_name)

#     elif "qwen" in model_name_lower:
#         return call_hf_model(prompt, model_name)

#     elif "llama" in model_name_lower:
#         return call_hf_model(prompt, model_name)

#     elif "deepseek" in model_name_lower:
#         return call_hf_model(prompt, model_name)

#     else:
#         raise ValueError(f"Unsupported model: {model_name}")

# ############################################
# # EXAMPLE USAGE (DELETE LATER)
# ############################################

# if __name__ == "__main__":
#     prompt = "If all bloops are razzies and all razzies are lazzies, are all bloops lazzies?"

#     models = [
#         "gemini-1.5-flash",
#         "Qwen/Qwen2.5-7B-Instruct",
#         "meta-llama/Llama-3.1-8B-Instruct",
#         "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
#     ]

#     for m in models:
#         print(f"\n--- {m} ---")
#         print(call_llm(m, prompt))


