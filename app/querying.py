import openai
import replicate
from pinecone import Pinecone, ServerlessSpec
from openai.error import RateLimitError
import time

# Initialize the Replicate client with the API token
client = replicate.Client(api_token="r8_E5rw9IjRQv7UKvaIBaqbbn76fTv0PCJ4U7gK3")

def query_vector_db(user_query):
    pc = Pinecone(api_key="6b677b06-9315-4675-9d94-090f47b4ee9b")

    if 'pwc' not in pc.list_indexes().names():
        pc.create_index(
            name='pwc',
            dimension=1536,
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )
    index = pc.Index('pwc')
    query_vector = get_query_vector(user_query)
    search_results = index.query(vector=[query_vector], top_k=5)
    return search_results

def get_query_vector(query):
    # Transform user query into a vector (dummy implementation)
    return [0.0] * 512

def create_prompts(user_query, search_results):
    return {
        'gpt-3.5-turbo': f"{search_results} {user_query}",
        'gpt-4': f"{search_results} {user_query}",
        'llama-2-70b-chat': f"{search_results} {user_query}",
        'falcon-40b-instruct': f"{search_results} {user_query}"
    }

def query_gpt_3_5_turbo(prompt):
    return query_openai(prompt, "gpt-3.5-turbo")

def query_gpt_4(prompt):
    return query_openai(prompt, "gpt-4")

def query_llama_2_70b_chat(prompt):
    return query_replicate(prompt, "meta/llama-2-70b-chat")

def query_falcon_40b_instruct(prompt):
    return query_replicate(prompt, "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173")

def query_openai(prompt, model):
    openai.api_key = "sk-proj-2fO9NG60B4k6ULfSwCJkT3BlbkFJQJ2OHS944xEQI6iwANuK"
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except RateLimitError:
        return "You have exceeded your API quota. Please try again later."
    except openai.error.InvalidRequestError as e:
        return str(e)

def query_replicate(prompt, model):
    try:
        output_iterator = client.run(
            model,
            input={"prompt": prompt}
        )
        # Consume the generator to get the actual output
        output = "".join(list(output_iterator))
        return output
    except replicate.exceptions.ReplicateError as e:
        return f"Replicate Error: {e.title}, {e.detail}"

def query_models(user_query, search_results):
    prompts = create_prompts(user_query, search_results)
    responses = [
        ('gpt-3.5-turbo', query_gpt_3_5_turbo(prompts['gpt-3.5-turbo'])),
        ('gpt-4', query_gpt_4(prompts['gpt-4'])),
        ('llama-2-70b-chat', query_llama_2_70b_chat(prompts['llama-2-70b-chat'])),
        ('falcon-40b-instruct', query_falcon_40b_instruct(prompts['falcon-40b-instruct']))
    ]
    return responses
