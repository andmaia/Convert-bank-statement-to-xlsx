from Data import get_data
from Functions.Func_aux import group_transactions,filter_transactions,process_transactions
from Functions.Func_aux_excel import create_dataframe,save_as_excel
from Models.ProviderSicoob import ProviderSicoob 
from Functions.Func_aux_pdf import extract_text_between_keywords,extract_text_pdf,verify_pattern_returned_from_pdf

exclusion_words = ["SALDO", "DO", "DIA"]
pattern = r"\d{2}/\d{2}"
first_item='SALDO BLOQ.ANTERIOR'
last_item='RESUMO'
caminho_arquivo=r'C:\Users\DELL\Downloads\Sicoob comprovante (27-12-2023 13-32-05).pdf'
text = extract_text_pdf(caminho_arquivo) 
text_verify=verify_pattern_returned_from_pdf(text) 
transactions= extract_text_between_keywords(text_verify,"BLOQ.ANTERIOR",'RESUMO') 
filtered_transactions = filter_transactions(transactions,exclusion_words) 
grouped_transactions = group_transactions(filtered_transactions,3,pattern) 
sicoob_provider = ProviderSicoob(pattern,exclusion_words)
list_discounts = process_transactions(grouped_transactions,sicoob_provider) 
dataframe = create_dataframe(list_discounts)
save_as_excel(dataframe,'dados_mawa_manaus.xlsx')




