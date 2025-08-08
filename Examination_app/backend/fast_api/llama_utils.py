import ollama


def get_llama_feedback(score: int, incorrect_questions: list) -> str:
    if not incorrect_questions:
        return "Excellent work! You answered all questions correctly."

    question_list = "\\n".join(f"- {q}" for q in incorrect_questions)
    prompt = f"""
You are an AI tutor helping a student understand their quiz performance.

The student scored {score}/10. Here are the questions they got wrong:
{question_list}

Based on this, provide personalized feedback and suggest areas to review.
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error generating feedback: {str(e)}"



import ollama
convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.2', messages=convo, stream=True)
    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    convo.append({'role': 'assistant', 'content': response})
    return response


