import re

def group_transactions(transactions,default_header_transaction,pattern_inicial):
    grouped_transactions = []
    current_transaction = []

    for line in range(len(transactions)):
        if len(transactions[line]) >= default_header_transaction and re.match(pattern_inicial, transactions[line][0]):
            if current_transaction:  
                grouped_transactions.append(current_transaction)
                current_transaction = []  
            current_transaction.append(transactions[line])
        else:
            current_transaction.append(transactions[line])
    if current_transaction:
        grouped_transactions.append(current_transaction)

    return grouped_transactions

def filter_transactions(transactions, exclusion_words):
    filtered_transactions = [transaction for transaction in transactions if not any(word in transaction for word in exclusion_words)]
    return filtered_transactions

def process_transactions(grouped_transactions, bank_provider):
    list_discounts = []

    for line in grouped_transactions:
        data = bank_provider.create_transf_entrace(line)
        if data:
            list_discounts.append(data)
            continue

        data = bank_provider.create_dep_entrace(line)
        if data:
            list_discounts.append(data)
            continue
        

        data = bank_provider.create_pix_entrace(line)
        if data:
            list_discounts.append(data)
            continue
        
        data = bank_provider.create_discount(line)
        if data:
            list_discounts.append(data)
            continue
        
        data = bank_provider.create_credit_entrace(line)
        if data:
            list_discounts.append(data)
            continue
        
        data = bank_provider.create_ted_entrace(line)
        if data:
            list_discounts.append(data)
            continue
     
    
    return list_discounts
