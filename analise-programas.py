from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 
from ollama import ResponseError
import pymupdf
import os
import json
from tqdm import tqdm
import logging

h = logging.FileHandler(filename='llm-prefeitos.log')
h.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(h)
logger.setLevel(logging.INFO)

logger.info('Iniciando execução.')

model = OllamaLLM(model="llama3.1:70b")

resultados = {}

top_dir = './pdfs'

prompt_template = """O texto a seguir, delimitado por triplos parênteses, foi extraído do plano de governo de um candidato a prefeito.
O texto contém alguma referência a uma proposta de plano de prevenção ou mitigação de riscos relacionados a eventos climáticos extremos (e.g.: inundações, deslizamentos, secas)?
Caso o texto não mencione o assunto, responda apenas NÃO
Caso o texto aborde o assunto, responda: SIM. trecho:<citação>
onde <citação> deve ser substituído por um trecho da frase que referencia o assunto.
Ignore eventuais erros na formatação do texto e responda apenas como pedido.
(((
    {texto}
)))
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

chain = prompt | model

lista_cidades = os.listdir(top_dir)
try:
    for cidade in lista_cidades:
        res_cidade = {}
        print(f"Avaliando cidade de {cidade}")
        for pdf in os.listdir(os.path.join(top_dir, cidade)):
            refs_clima = []
            print(f'Avaliando "{pdf}":') 
            for page in tqdm(pymupdf.open(os.path.join(top_dir, cidade, pdf))):
                text = page.get_text()
                retries = 0
                while True:
                    try:
                        response = chain.invoke({'texto': text})
                        break
                    except ResponseError as e:
                        retries += 1
                        if retries > 2:
                            raise e
                logger.info(f"{cidade}/{pdf}/{page.number + 1}:{response}")
                if "SIM" in response:
                    refs_clima.append(page.number + 1)
            res_cidade[pdf] = refs_clima
        resultados[cidade] = res_cidade
finally:
    h.close()
    json.dump(resultados, fp=open("resultados.json", "w"), ensure_ascii=False)
