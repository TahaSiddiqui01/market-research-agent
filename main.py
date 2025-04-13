from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.product_reviews import get_product_reviews
from textwrap import dedent
import os
import getpass

api_key = getpass.getpass("Please enter your OpenAI API key: ")
os.environ["OPENAI_API_KEY"] = api_key

# The great mistake here is, we should use the agentic approach beacuse we can 
# simply solve the problem by merely using a direct OPENAI api call.

# Note: We should try to make out solution as simple as possible.

class ProductReviewsAgent():


    def review_analysis(self):
        agent = Agent(
            name="G2 Reviews",
            role="Act as a Market Researcher for a New Product",
            model=OpenAIChat(id="gpt-4o"),
            add_name_to_instructions=True,
            tools=[get_product_reviews],
            show_tool_calls=True,
            instructions=dedent( """
            I will give you multiple product reviews that include pros, cons, and the problem the product is solving. 
            The reviews are in the format of an array of objects containing TrustPilot and G2 reviews.
            
            Your job is to:
            1. Extract useful insights from these reviews.
            2. Identify recurring pain points users mention.
            3. Highlight the top features users love and features they hate or wish were better.
            4. Understand what problem the product solves, and how effectively it solves it.
            
            Give a concise summary answering:
            - Should I build a similar product?
            - What features must my version have?
            - What differentiators or improvements would make it stand out?
            
            Only give insights that are actionable and backed by patterns in the reviews. 
            Be objective, avoid fluff, and think like a startup founder validating a new idea.
        """),
        )

        return agent
    
    def trust_pilot_reviews(self):
        pass

if __name__ == "__main__":
    productReviewsAgent = ProductReviewsAgent()
    agent = productReviewsAgent.review_analysis()
    agent.print_response(f"Give me the complete analysis of the product reviews using the tool that is passed to you")



# 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