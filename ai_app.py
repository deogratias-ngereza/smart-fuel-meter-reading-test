import os
import openai
import json
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langsmith import wrappers, traceable
from dotenv import load_dotenv

load_dotenv()

LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_TRACING_V2')
OPENAI_API_KEY = os.getenv('LANGCHAIN_TRACING_V2')


os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Set up OpenAI API key (Make sure to replace with your actual key)
openai.api_key = OPENAI_API_KEY

client = openai.Client(api_key=openai.api_key) 

# Initialize LangChain model with OpenAI GPT-4 Turbo Vision
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Function to analyze meter reading from an image
def analyze_meter_reading(image_path):
    try:
        # Open the image in binary mode
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Call OpenAI GPT-4 Turbo Vision API with image upload
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI trained to extract meter readings from fuel meters."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract the values for Sale, Litre, and Price from this meter reading."},
                    {"type": "image", "data": image_data}  # Direct image upload as binary data
                ]}
            ],
            temperature=0
        )

        # Extract response content
        extracted_data = response.choices[0].message.content

        return {"image_path": image_path, "meter_readings": extracted_data}

    except Exception as e:
        return {"error": str(e)}

def xanalyze_meter_reading(image_path):
    try:
        # Open image file in binary mode
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Correct OpenAI Vision API request format
        response = llm.invoke([
            HumanMessage(content=[
                {"type": "text", "text": "Extract the values from this fuel meter: Sale, Litre, and Price."},
                {"type": "image_url", "image_url": {"url": f"file://{os.path.abspath(image_path)}"}}
            ])
        ])

        return {"image_path": image_path, "meter_readings": response.content}

    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    image_path = os.getcwd()+"/sample1.jpeg"  # Replace with the actual meter image file
    result = analyze_meter_reading(image_path)

    # Print the extracted meter readings
    print(json.dumps(result, indent=4))
