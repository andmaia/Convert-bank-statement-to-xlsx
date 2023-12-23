from Data import get_data
from Functions.Func_aux import group_transactions,filter_transactions,process_transactions
from Functions.Func_aux_excel import create_dataframe,save_as_excel
from Models.ProviderSicoob import ProviderSicoob

extract = get_data()
lines = extract.split('\n')
transactions = [line.split(' ') for line in lines if line]
exclusion_words = ["SALDO", "DO", "DIA"]
pattern = r"\d{2}/\d{2}"

filtered_transactions = filter_transactions(transactions,exclusion_words)
grouped_transactions = group_transactions(filtered_transactions,3,pattern)

sicoob_provider = ProviderSicoob(pattern,exclusion_words)

list_discounts = process_transactions(grouped_transactions,sicoob_provider)
    
dataframe = create_dataframe(list_discounts)

save_as_excel(dataframe,'Teste2.xlsx')




