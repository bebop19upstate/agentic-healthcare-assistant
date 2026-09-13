from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.graph import app

load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')

result = app.invoke({
    'query': 'Book me a cardiologist appointment next week',
    'patient_id': 1,
    'plan': [], 'tool_results': {}, 'final_answer': '',
})
answer = result['final_answer']
print('=== ANSWER ===')
print(answer)

grading_prompt = f'''You are grading an AI assistant's answer against a set of criteria. Respond with GRADE: CORRECT or GRADE: INCORRECT on the first line, followed by a one-sentence explanation.

Criteria the answer should meet:
Confirms a cardiology appointment was booked with a specific doctor and time. Does not mention medical history or treatment information, since none was requested.

The AI assistant answered:
{answer}

Grade:'''

response = llm.invoke(grading_prompt)
print()
print('=== GRADE ===')
print(response.content)
