import re
import pdfplumber


def extract_text_pdf(caminho_arquivo):
    texto_completo = ''
    with pdfplumber.open(caminho_arquivo) as pdf:
        for page in pdf.pages:
            texto_completo += page.extract_text()
    return texto_completo

def extract_text_between_keywords(text, start_keyword, end_keyword):
    pattern = re.compile(f'{start_keyword}.*?{end_keyword}', re.DOTALL)
    match = re.search(pattern, text)
    if match:
        extract = match.group()
        lines = extract.split('\n')
        transactions = [line.split(' ') for line in lines if line]
        transactions=transactions[1:-1]
        return transactions



def verify_pattern_returned_from_pdf(texto):
    padrao = r'(\d+[.,]?\d{0,2})([CD])(\w)'

    # Substitui o padrão encontrado por preço + C/D + próxima letra por preço + C/D + quebra de linha + próxima letra
    texto_corrigido = re.sub(padrao, r'\1\2\n\3', texto)

    return texto_corrigido

   

