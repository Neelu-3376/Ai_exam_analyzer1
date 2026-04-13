import requests
import markdown


def get_ai_answer(question, lang):

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    # language selection
    if lang == "hindi":
        language = "Write answer in Hindi language."
    elif lang == "hinglish":
        language = "Write answer in Hinglish (Hindi + English mix)."
    else:
        language = "Write answer in simple English."

    content = f"""
You are writing a university exam answer.

{language}

Write a long answer (8–10 marks) in simple language.

Use proper headings and bullet points.

Format strictly:

Definition:
(4-5 lines explanation)

Scope:
- point 1 (2 lines explanation)
- point 2 (2 lines explanation)
- point 3 (2 lines explanation)
- point 4 (2 lines explanation)
- point 5 (2 lines explanation)

Limitations:
- point 1 (2 lines explanation)
- point 2 (2 lines explanation)
- point 3 (2 lines explanation)
- point 4 (2 lines explanation)
- point 5 (2 lines explanation)

Conclusion:
(2-3 lines)

Question: {question}
"""

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": content}
        ],
        "temperature": 0.2
    }

    response = requests.post(API_URL, headers=headers, json=data)

    try:
        answer = response.json()['choices'][0]['message']['content']
        return markdown.markdown(answer)
    except:
        return "AI answer not available"