from Models.ProviderBank import ProviderBank
import re
class ProviderSicoob(ProviderBank):
    def __init__(self, pattern_inicial=None, group_words_clear=None):
        super().__init__()  
        self.pattern_inicial = pattern_inicial
        self.group_words_clear = group_words_clear

    
    def create_discount(self, transaction):
        item_for_convert_to_discount = []
        words_payment = ['DEB','DÉB','VISA','COMP']
        if self._verify_discount(transaction):
               
               payment_form = self._verify_payment_form(transaction[0],words_payment)
               if payment_form == words_payment[-2]:
                  payment_form ='CR'
               if payment_form ==  None or payment_form == words_payment[-1]:
                  payment_form ='DEB'
              

               item_for_convert_to_discount =[
                transaction[0][0],
                payment_form,
                ' '.join(transaction[0][1:-1]),
                transaction[0][-1][:-1],
                'Pagamento',
                '',
                '',
                '',
                '']
               
               if len(transaction)>2:
                 item_for_convert_to_discount[-1] = ' '.join(transaction[-2])
                   
               return item_for_convert_to_discount
        else:
                pass
            
    def create_credit_entrace(self, transaction):
       if self._verify_credit_entrance(transaction):
            item_for_convert = []
            words_payment = ['DEB','DÉB','Deb']
            payment_form = self._verify_payment_form(transaction[1],words_payment)
            if payment_form == None:
                payment_form = 'CR'

            item_for_convert=[
                transaction[0][0],
                payment_form,
                ' '.join(transaction[0][1:-1]),
                transaction[0][-1][:-1],
                'Recebimento',
                '',
                '',
                '',
                ' '.join(transaction[1])]
            return item_for_convert
       else:
            pass

    def create_pix_entrace(self, transaction):
        item_for_convert = []
        if self._verify_pix(transaction):
            item_for_convert=[
                transaction[0][0],
                transaction[0][1],
                ' '.join(transaction[0][1:-1]),
                transaction[0][-1][:-1],
                transaction[1][0],
                '',
                '',
                '',
                '']
            if self._verify_if_comment_exists(transaction,'DOC.:'):
                  item_for_convert[-1]=' '.join(transaction[-2])
            if(self._verify_pix_is_cnpj(transaction)):
                  item_for_convert[7]=''.join(transaction[2])
            if(self._verify_pix_is_cpf(transaction)):
                if(self._verify_word_key_exists(transaction,"Recebimento")):
                      item_for_convert[5]=' '.join(transaction[2])
                      item_for_convert[6]=' '.join(transaction[3])
                else: 
                      item_for_convert[6]=' '.join(transaction[2])
                      
            return item_for_convert
        else:
            pass

    def create_ted_entrace(self, transaction):
        item_for_convert = []
        if self._verify_ted(transaction):
             item_for_convert=[
                transaction[0][0],
                'TED',
                ' '.join(transaction[0][1:-1]),
                transaction[0][-1][:-1],
                'Pagamento',
                '',
                '',
                '',
                '']
             if self._verify_pix_is_cnpj(transaction):
                 item_for_convert[7]=''.join(transaction[2]) 
             return item_for_convert
        else:
            pass


    def _verify_pix(self, transaction):
        for sub_array in transaction:
            if 'PIX' in sub_array or '.OUTR' in sub_array or 'Pix' in sub_array:
                return True
        return False

    def _verify_discount(self, transaction):
        if len(transaction) <= 2:
            return True 
        if len(transaction) <4:
            first_item = transaction[0]
            if first_item[1].startswith('DÉB') or first_item[1].startswith('DEB') or first_item[1].startswith('COMP'):
                return True 
            if not first_item[1].startswith('CR'):
                return True
        return False
    
    def _verify_credit_entrance(self, transaction):
        first_item = transaction[0]
        second_item = transaction[1]
        if len(transaction) >= 2:
            if 'CR' in first_item and 'SIPAG' in second_item[0]:
                return True
        
        return False

    def _verify_pix_is_cpf(self, transaction):
        transaction_str = ''.join(''.join(sublist) + ' ' for sublist in transaction)
        cpf_pattern = re.compile(r'\*\*\*\.(\d{3}\.\d{3}-\*\*)')
        match = cpf_pattern.search(transaction_str)

        if match:
            return True
        return False

    def _verify_pix_is_cnpj(self, transaction):
        transaction_str = ''.join(''.join(sublist) + ' ' for sublist in transaction)
        cnpj_pattern = re.compile(r'\b\d{2}\.\d{3}\.\d{3}\d{4}-\d{2}\b')
        match = cnpj_pattern.search(transaction_str)

        if match:
            return True
        return False

    def _verify_if_comment_exists(self, transaction,word_key):
        if len(transaction) >= 3:
            antepenultimate_item =''.join( transaction[-3])
            last_item = transaction[-1]

            if word_key in last_item:
                if self._verify_pix_is_cpf([antepenultimate_item]) or self._verify_pix_is_cnpj([antepenultimate_item]):
                    return True
        return False


    def _verify_ted(self, transaction):
        if len(transaction)>= 4:
            fist_item =''.join(transaction[0])
            code_ted_item=''.join(transaction[-1])
            if 'TED' in fist_item or 'TED' in code_ted_item:
                  return True
            else:
                  return False
        else:
            return False

    def _verify_word_key_exists(self,transaction,word):
        transaction_str = ''.join(''.join(sublist) + ' ' for sublist in transaction)
        if word in transaction_str:
          return True
        return False
    
    def _verify_payment_form(self,transaction, words):
        transaction_str = ''.join(''.join(sublist) + '' for sublist in transaction)
        
        for word in words:
            if word in transaction_str:
                return word    
        return None


           