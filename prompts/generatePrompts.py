fewShot_prompt = ""
from dotenv import load_dotenv

load_dotenv()
from google import genai
client = genai.Client()


def generatePrompts(numPairs: int, examples) -> str:
    prompt = f'''

    You are an assistant in a research project. You are now tasked to write prompts to test a model's 
    Examples: {examples}

    Create {numPairs} of such prompts. Return the prompts as a json file. 
   
    '''

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    print(response.text)

generatePrompts(5)