Avaliando o enfrentamento político à crise climática nas eleições municipais do Brasil em 2024
==========

Este repositório contém os dados para a reprodução das análises dos programas de governo para as eleições de 2024 às prefeituras das cidades brasileiras mais vulneráveis a eventos climáticos extremos.

## Uso

O script de análise utiliza um grande modelo de linguagem (LLM) para a verificação página a página dos programas de governo. O acesso ao LLM se dá pelo uso da ferramenta [Ollama](https://ollama.com) (instruções de instalação na página da ferramenta). Certifique-se da disponibilidade do serviço Ollama e do modelo llama3.1:70b.

O script utliiza Python 3. Verifique a presença da instalação do Python e instale as bibliotecas necessárias listadas no arquivo requirements.txt (via pip: `pip install -r requirements.txt`).

Execute o script diretamente:

```bash
python analise-programas.py
```

## Resultados

O diretório `out` contém um arquivo de log com a saída obtida pelo LLM para cada página dos arquivos PDF. O resumo dos resultados está disponível como arquivo JSON.
