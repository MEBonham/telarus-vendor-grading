import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def handler(request, response):
    if request.method == "POST":
        return response.status(405).send("Only POST allowed")
    
    try:
        body = request.json()
        vendor_name = body.get("vendor")
        ratings = body.get("ratings")
        weights = body.get("weights")
        final_score = body.get("finalScore")

        prompt = f"""You are a helpful salesperson who is fair about the vendors you recommend. Write a short (maybe 3 lines) paragraph about this particular vendor's strengths and weaknesses and why they received the overall score that they did.
Be specific about the areas where the vendor excelled and those where they struggled, especially if those areas are heavily weighted.

Venor Name: {vendor_name}

Vendor's ratings in all areas:
{ratings}

Weights:
{weights}
"""

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = completion.choices[0].message['content']
        return response.json({ "result": reply })

    except Exception as e:
        return response.status(500).send(str(e))
        