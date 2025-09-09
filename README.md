# Telarus Vendor Grading

This is a simple web app that allows you to upload a CSV file of vendor ratings, and then generates a final score for each vendor based on their ratings.

You can see the deployed webpage at https://telarus-vendor-grading.vercel.app

## How it works

You must have a CSV file with ratings (out of five stars) for each vendor. The categories should be in the following order:

1. Price
2. Cost Transparency & Contract Flexibility
3. Reliability & Uptime
4. Service Performance
5. Innovation & Technology Adoption
6. Security & Privacy
7. Regulatory Compliance
8. Reputation & Customer Reviews
9. Customer Support Quality
10. Environmental & Social Impact

You can use the provided CSV file as a template.

Go to the "Upload Vendors" page and select your CSV file. Once uploaded, you will be redirected to the "Grades" page, where you can view the scores for each vendor.

## Explanations

I tried to use a call to ChatGPT to generate explanations for each vendor's score. It's not quite working yet. Vercel isn't recognizing the python function used to call ChatGPT as part of my deployment.

## What Is Working

The main page shows a list of vendors, with their final scores, sorted from best to worst. Clicking on a vendor's name SHOULD show a detailed explanation of their score, including the areas where they excelled and those where they struggled. But it does display their ratings in each specific area.

# Setup

I used SvelteKit to build the app. You can run the front end (not the API call) by putting in `npm run dev` in the terminal while in the `vendorScore` directory.

# Assumptions

I assumed that the vendor ratings are out of five stars, and that the weights could be adjusted to suit your needs. I did not have time to make an interface for admins to dynamically adjust the weights.

# Scoring Logic

The final score for each telecom vendor is calculated by combining their ratings across all 10 evaluation factors, with each factor contributing a different amount of weight to the total. First, every factor (like Price, Reliability, Security, etc.) is scored on a scale from 1 to 5, where 1 means very poor and 5 means excellent. Each score is then converted into a percentage by dividing it by 5 (so a 5 equals 100%, a 3 equals 60%, etc.) and multiplied by the weight assigned to that factor (for example, Price might count for 15% of the total). Once all these weighted contributions are calculated, they are added together to get a single final score out of 100. This way, the most important factors influence the overall score more heavily, while less critical factors still play a role but have less impact.

Here's how the weights are distributed across the 10 factors in the scoring model: Price (15%), Cost Transparency & Contract Flexibility (8%), Reliability & Uptime (15%), Service Performance (12%), Innovation & Technology Adoption (8%), Security & Privacy (12%), Regulatory Compliance (8%), Reputation & Customer Reviews (7%), Customer Support Quality (8%), and Environmental & Social Impact (5%). Together, these add up to 100%.

# Next Steps

1. Get the python function's deployment on Vercel working.
2. Add a way to dynamically adjust the weights.
3. Ask for feedback!!!!
4. 