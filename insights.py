# #todo
# #botar para o gpt
# #chamar na app.py
# #baixar graph imprimir insight


# from ollama import Client
# client = Client(host='http://localhost:11434')
# system_prompt = "Você é um cientista de dados especializado em análise de métricas e gráficos. Responda com insights claros e objetivos, sempre em até 100 caracteres. Foco em relevância e precisão."
# x = "grafico de barras"
# y = "consultorias"
# z = "300"
# x2 = "150"
# response = client.chat(model='llama3.2', messages=[
#   {'role': 'system', 'content': system_prompt},
#   {
#     'role': 'user',
#     'content': f'fizemos um grafico {x} e notamos a variavel {y} no valor de {z}, mes passado tivemos uma media de {x2} por dia, Devemos nos precupar com isso?',
#   },
  
# ])
# print(response['message']['content'])