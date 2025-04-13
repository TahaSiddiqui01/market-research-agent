from product_reviews.product_reviews import get_g2_reviews, get_trustpilot_reviews
import json
TRUSTPILOT_BASE_URL = "https://www.trustpilot.com/review/vizard.ai?page=1"
TRUSTPILOT_ADDITIONAL_FILTERS = "&sort=relevance&stars=1&stars=2&stars=3&stars=4"



def get_product_reviews() -> str:
    g2_reviews = get_g2_reviews()
    trustpilot_reviews = get_trustpilot_reviews(TRUSTPILOT_BASE_URL + TRUSTPILOT_ADDITIONAL_FILTERS)
    reviews = {
        "g2_reviews": [],
        "trustpilot_reviews": []
    }

    for review in g2_reviews:
        review_data = {
            "pros": {
                "question": review["pros"]["question"].strip(),
                "answer": review["pros"]["answer"].strip()
            },
            "cons": {
                "question": review["cons"]["question"].strip(),
                "answer": review["cons"]["answer"].strip()
            },
            "problem_solved": {
                "question": review["problem_it_solved"]["question"].strip(),
                "answer": review["problem_it_solved"]["answer"].strip()
            }
        }
        reviews["g2_reviews"].append(review_data)

    for review in trustpilot_reviews:
        review_data = {
            "date": review["date_of_experience"].strip(),
            "review_text": review["review"].strip()
        }
        reviews["trustpilot_reviews"].append(review_data)

    return json.dumps(reviews)