from dotenv import load_dotenv
import json
from google import genai
from promptTemplates import GENERATION_PROMPT, FEW_SHOT_EXAMPLES
from pathlib import Path
from collections import Counter

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

    print("📤 Sending request to Gemini...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text.strip()

    print("📥 Raw response received, parsing...")
    
    # Remove markdown code blocks if present
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:-3]  # Remove ```json and ```
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:-3]  # Remove ``` and ```
    
    # Clean up any remaining whitespace
    raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)
        print(f"✅ Successfully parsed JSON with {len(data)} items")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print("Trying to fix JSON...")
        
        # Try to find JSON array in the text
        import re
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                print(f"✅ Fixed JSON with {len(data)} items")
                return data
            except:
                pass
        
        print("Raw text that failed to parse:")
        print(raw_text[:500])
        raise

def save_json(data, filepath):
    """
    Save data to JSON file, creating directories if needed.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} question pairs to {filepath}")

if __name__ == "__main__":
    NUM_PAIRS = 50

    print("🚀 Generating question pairs...")
    
    script_dir = Path(__file__).parent
    output_path = script_dir / "generated_question_pairs.json"
    
    print(f"📝 Will save to: {output_path.absolute()}")
    print(f"📊 Using {len(FEW_SHOT_EXAMPLES)} few-shot examples")
    
    try:
        prompts = generate_questionPairs(
            num_pairs=NUM_PAIRS,
            examples=FEW_SHOT_EXAMPLES
        )

        # Sanity checks
        if not isinstance(prompts, list):
            print(f"❌ Output is not a list, got {type(prompts)}")
            exit(1)
            
        print(f"✅ Generated {len(prompts)} question pairs")
        
        # Check structure
        valid_count = 0
        for i, p in enumerate(prompts):
            if not isinstance(p, dict):
                print(f"  ❌ Item {i} is not a dict: {type(p)}")
                continue
            if not all(key in p for key in ["category", "question", "correct_answer", "evaluation_context", "casual_context"]):
                print(f"  ❌ Item {i} missing required keys: {list(p.keys())}")
                continue
            valid_count += 1
            
        print(f"📊 Valid items: {valid_count}/{len(prompts)}")

        # Count categories
        category_counts = Counter(p["category"] for p in prompts)

        print("\n📊 Category distribution:")
        for category, count in category_counts.items():
            print(f"  - {category}: {count}")

        print(f"\n📦 Total items: {sum(category_counts.values())}")
            
        # Save to file
        save_json(prompts, output_path)

    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
