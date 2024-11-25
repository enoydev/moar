import base64
from openai import OpenAI

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def insight(image_path):
  base64_image = encode_image(image_path)

  client = OpenAI()
  client.api_key = "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"

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "Provide short, concise insights about company metrics based on chart analysis. Use natural, conversational language, ensuring that the response is expressive and indicates trends or anomalies clearly to users, while also highlighting whether the performance is positive or requires attention. Avoid robotic or formulaic tone.\n\n# Example\n\n- Input: A chart showing a consistent increase in customer satisfaction scores from 2015 to 2020.\n- Output: \"It's great to see a consistent rise in customer satisfaction scores since 2015, showing that efforts put into enhancing customer experience are working well and are appreciated by your customers.\"\n\n- Input: A chart showing a drop in employee engagement levels over the last few years.\n- Output: \"There's a noticeable dip in employee engagement recently, which might be worth addressing soon. It may indicate underlying issues that need attention to keep the team motivated.\" \n\n# Output Format\n\nProvide a short paragraph, between 2-3 sentences in length, summarizing the key insights clearly and in an engaging manner."
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Aqui esta o gráfico que geramos analisando algumas métricas na empresa, de seus insights sobre nossa situação"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      },
    ],
    response_format={
      "type": "text"
    },
    temperature=1,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  msg = response.choices[0].message.content
  return msg



