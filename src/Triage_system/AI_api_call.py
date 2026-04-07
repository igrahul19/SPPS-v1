from google import genai
import os
import json
from typing import Any
GEMINI_API_KEY = "AIzaSyDR1N69pDpYuFLrs5Gmly5SZsfxCRG1mXw" 
PROMPT = '''You are a hospital receptionist responsible for organizing patients based on the severity of their condition.

Your task is to carefully analyze each patient’s symptoms and assign a **risk score (risk_range)** between **0 and 1**, where:

* **0** = No immediate risk (minor or routine case)
* **1** = Critical, life-threatening condition requiring immediate attention

### Instructions:

1. Evaluate the patient’s symptoms based on:

   * Severity (mild, moderate, severe)
   * Urgency (sudden onset, chronic, worsening)
   * Vital indicators (e.g., chest pain, breathing difficulty, unconsciousness, bleeding)
   * Patient factors (age, existing conditions if provided)

2. Assign a **risk_range value** (0 to 1) using logical reasoning:

   * 0.0 – 0.3 → Low risk (can wait)
   * 0.3 – 0.6 → Moderate risk (needs timely attention)
   * 0.6 – 0.8 → High risk (priority case)
   * 0.8 – 1.0 → Critical (immediate attention required)

3. Provide output in the following dictionary format:
   {
    Risk Score: <value>
    Priority Level: <Low / Moderate / High / Critical>
   }
4. Be consistent, unbiased, and prioritize life-threatening symptoms over all others.

5. If symptoms are unclear or insufficient, assign a moderate risk and mention uncertainty in reasoning.

Your goal is to ensure that patients with the highest risk are prioritized first in the queue.

The User Info is :'''

def jsonify(string: str):
    encoded = json.loads(string)
    return encoded

def ask_gemini(prompt: str):
    """Call Gemini and return a plain Python dict representing the response.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        contents = str(prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents
        )
    except Exception as e:
        exception = Exception(f"error: request_failed, message: {str(e)}")
        print(exception)

    return response # type: ignore

def calculate_risk_score(user_info: dict[str, Any] ):
    '''Calculates the risk range of the patient
    '''
    prompt = PROMPT
    prompt += str(user_info)
    
    response = ask_gemini(prompt)
    response = response.text # pyright: ignore[reportCallIssue, reportOptionalCall]

    response_dict = jsonify(str(response))
    return response_dict["Risk Score"]

def calculate_token_reduction(current_token_number:int, risk_score:float) -> int:
    token_reduction = 1+(current_token_number-1) * (1-risk_score)
    reduction = current_token_number - token_reduction
    new_reduction = int(reduction // 1) 
    if 0 < reduction < 3 and risk_score < 0.5:
        return 0 
    return new_reduction

