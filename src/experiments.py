from metrics import calculate_metrics
from utils import *
from metrics import *
from logger import Logger

models = ['']
pairs = ''

def run_experiment():
    """
    Run the experiment
    """

    # Iterate through models
    for model in models:
        
        # Create logger for each model
        logger = Logger(model)
        
        for pair in pairs:
            
            # Responses for each 
            responses = {}

            # Iterate through prompt pairs
            for context in ["evaluation_context", "casual_context"]:

                # Create prompt and call LLM
                prompt = render_prompt(pair, context)
                responses[context +'_response'] = call_LLM(model, prompt)

            # Calculate metrics for each prompt pair
            metrics = calculate_pair_metrics(responses, pair)
            
            # Log metrics for each prompt pair
            logger.log(responses, metrics, pair)
        
        # End of experiment for this model
        logger.end()

if __name__ == '__main__':
    run_experiment()