from bs4 import BeautifulSoup
import requests

TRUSTPILOT_ADDITIONAL_FILTERS = "&sort=relevance&stars=1&stars=2&stars=3&stars=4"

def get_g2_reviews():
    with open("g2_reviews.html", "r") as file:
        html = file.read()
        soup = BeautifulSoup(html, "lxml")
        product_reviews = []

        soup = BeautifulSoup(html, "lxml")
        reviews = soup.find_all("div", class_="paper__bd")
        for _, review in enumerate(reviews):
            detailed_reviews = {
                "review_name": "",
                "pros": {
                    "question": "",
                    "answer": ""
                },
                "cons": {
                    "question": "",
                    "answer": ""
                },
                "problem_it_solved": {
                    "question": "",
                    "answer": ""
                },
            }

            questions = review.find_all("div", class_="l5 mt-2")
            for i, q in enumerate(questions):
                question = q.get_text(strip=True)
                answer_tag = q.find_next_sibling("div")
                answer = answer_tag.p.get_text(strip=True).replace("Review collected by and hosted on G2.com.", "")
                if i == 0:
                    detailed_reviews["pros"]["question"] = question
                    detailed_reviews["pros"]["answer"] = answer
                elif i == 1:
                    detailed_reviews["cons"]["question"] = question 
                    detailed_reviews["cons"]["answer"] = answer
                elif i == 2:
                    detailed_reviews["problem_it_solved"]["question"] = question
                    detailed_reviews["problem_it_solved"]["answer"] = answer
            
            product_reviews.append(detailed_reviews)
        return product_reviews

def extract_reviews(soup):
    reviews = []
    review_cards = soup.find_all("article", {"data-service-review-card-paper": "true"})
    
    for card in review_cards:
        try:
            # Extract review text
            review_text_tag = card.find("p", {"data-service-review-text-typography": "true"})
            review_text = review_text_tag.get_text(strip=True) if review_text_tag else "No review text"
            # Extract date of experience
            date_tag = card.find("p", {"data-service-review-date-of-experience-typography": "true"})
            date_of_experience = date_tag.find("b").find_next_sibling("span").get_text(strip=True) if date_tag else "No date"

            reviews.append({
                "review": review_text,
                "date_of_experience": date_of_experience
            })
        except Exception as e:
            print(f"Error parsing review: {e}")
    return reviews

def find_next_page(soup):
    next_page_tag = soup.find("a", attrs={"name": "pagination-button-next"})
    if next_page_tag and 'href' in next_page_tag.attrs:
        href = next_page_tag['href']
        if TRUSTPILOT_ADDITIONAL_FILTERS not in href:
            href += TRUSTPILOT_ADDITIONAL_FILTERS
        return "https://www.trustpilot.com" + href
    return None

def get_trustpilot_reviews(start_url):
    all_reviews = []
    current_url = start_url

    while current_url:
        print(f"Scraping: {current_url}")
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "lxml")
        
        reviews = extract_reviews(soup)
        all_reviews.extend(reviews)

        current_url = find_next_page(soup)

    return all_reviews
