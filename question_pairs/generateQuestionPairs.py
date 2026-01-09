
from dotenv import load_dotenv
import json
from google import genai
from question_pairs.promptTemplates import GENERATION_PROMPT, FEW_SHOT_EXAMPLES

# Load environment variables
load_dotenv()

# Initialize Gemini client
try:
    from google import genai
    client = genai.Client()
    GEMINI_AVAILABLE = True
    print("✅ Google Gemini API available")
except ImportError:
    print("❌ Google Generative AI not installed. Please run: pip install -q -U google-genai")
    GEMINI_AVAILABLE = False
except Exception as e:
    print(f"❌ Error initializing Gemini: {e}")
    GEMINI_AVAILABLE = False

client = genai.Client()

def generate_questionPairs(num_pairs: int, examples: list) -> list:
    """
    Generates sandbagging question pairs using specified model.
    Returns parsed JSON (list of dicts).
    """

    prompt = GENERATION_PROMPT.format(
        num_pairs=num_pairs,
        examples=json.dumps(examples, indent=2)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()
    
    # Remove markdown code blocks if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:-3]  # Remove ```json and ```
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:-3]  # Remove ``` and ```
    
    # Clean up any remaining whitespace
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        print("❌ Model did not return valid JSON.")
        print("Cleaned response:", raw_text[:200])
        raise

def save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} question pairs to {filepath}")

if __name__ == "__main__":
    NUM_PAIRS = 50

    print("🚀 Generating question pairs...")
    prompts = generate_questionPairs(
        num_pairs=NUM_PAIRS,
        examples=FEW_SHOT_EXAMPLES
    )

    # Optional sanity check
    assert isinstance(prompts, list), "Output is not a list"
    assert all("question" in p for p in prompts), "Malformed question detected"

    save_json(prompts, "question_pairs/generated_question_pairs.json")