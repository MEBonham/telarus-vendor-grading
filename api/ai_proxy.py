import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def handler(request, response):
    print("Handler invoked.")

    if request.method != "POST":
        print("Invalid method:", request.method)
        return response.status(405).send("Only POST allowed")

    try:
        print("Attempting to parse JSON...")
        body = request.json()
        print("Body received:", body)

        vendor_name = body.get("vendor")
        ratings = body.get("ratings")
        weights = body.get("weights")
        final_score = body.get("finalScore")

        print("Parsed data:")
        print("Vendor:", vendor_name)
        print("Ratings:", ratings)
        print("Weights:", weights)
        print("Final Score:", final_score)

        prompt = f"""You are a helpful salesperson who is fair about the vendors you recommend...
Venor Name: {vendor_name}
Vendor's ratings in all areas:
{ratings}
Weights:
{weights}
"""

        print("Sending prompt to OpenAI...")

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )

        reply = completion.choices[0].message['content']
        print("OpenAI reply:", reply)

        return response.json({ "result": reply })

    except Exception as e:
        print("Error occurred:", str(e))
        return response.status(500).send(str(e))
