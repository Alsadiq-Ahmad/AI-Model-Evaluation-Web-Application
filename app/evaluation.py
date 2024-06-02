# app/evaluation.py
def evaluate_responses(responses):
    best_response = determine_best_response(responses)
    return best_response

def determine_best_response(responses):
    # Assuming the best response is the one with the longest length
    return max(responses, key=lambda x: len(x[1]))
