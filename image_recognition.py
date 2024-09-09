from helper_functions import encode_base_64

PROMPT = """
What is the product in the image? Identify its model and other specifications as well. 
Provide the answer in the format specified below. 
Product:
Model:
Company: 
Specifications: 
In case you have absolutely no idea about any particular field, specify it as "TBD"."""

def recognize_image(client, image_filepath: str, image_type: str = None):
    messages = []
    messages = [
                    {
                        "role": "user",
                        "content": 
                        [
                            {
                                "type": "text", 
                                "text": PROMPT,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_type};base64,{encode_base_64(image_filepath)}",
                                },
                            },
                        ],
                    }
                ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message.content
