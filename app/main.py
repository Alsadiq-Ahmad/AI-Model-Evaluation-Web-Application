from flask import Flask, request, jsonify, render_template
from flask_sse import sse
from app import app
from app.querying import query_models, query_vector_db, create_prompts, query_gpt_3_5_turbo, query_gpt_4, query_llama_2_70b_chat, query_falcon_40b_instruct
import concurrent.futures #Execute tasks asynchronously

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_query = request.json['query']
    search_results = query_vector_db(user_query)

    def send_responses(model, prompt):
        with app.app_context(): # to ensure the Flask application context is available within the function
            if model == 'gpt-3.5-turbo':
                response = query_gpt_3_5_turbo(prompt)
            elif model == 'gpt-4':
                response = query_gpt_4(prompt)
            elif model == 'llama-2-70b-chat':
                response = query_llama_2_70b_chat(prompt)
            elif model == 'falcon-40b-instruct':
                response = query_falcon_40b_instruct(prompt)
            sse.publish({"model": model, "response": response}, type='response') #data send it to frontend

    prompts = create_prompts(user_query, search_results)#Creates prompts for each model
    models_prompts = [ 
        ('gpt-3.5-turbo', prompts['gpt-3.5-turbo']),
        ('gpt-4', prompts['gpt-4']),
        ('llama-2-70b-chat', prompts['llama-2-70b-chat']),
        ('falcon-40b-instruct', prompts['falcon-40b-instruct'])
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor: #Execute the send_responses function asynchronously for each model-prompt pair.
        futures = [executor.submit(send_responses, model, prompt) for model, prompt in models_prompts]

    return jsonify({"status": "processing"})

if __name__ == '__main__':
    app.run(debug=True)
