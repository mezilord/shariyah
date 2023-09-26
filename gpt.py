import openai
openai.api_key = "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"
# openai.api_key = "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"
# openai.api_key = "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"

def get_completion(prompt, rules, model="gpt-3.5-turbo-16k"):
    messages = [
        {"role": "system", "content": "Given the provided [UserText] and [RuleText], \
         your task is to meticulously analyze whether the [UserText] violates any of the\
          rules laid out in the [RuleText].\n\nThe format of the [UserText] is as follows:\
         \n'File Name: {doc_name}\n{doc_text}\n\n'\n\nIn case of no violations, \
         return nothing.\n\nIf you find any violations, respond with an array that consists\
          of three elements and is in this format:\
         \n[**FileName**, **ExactText**, **Cause**]\n\n\
         **FileName**: The name of the file where the violation occurred at the first index.\
         \n\n**ExactText**: The Exact piece of text within [UserText] causing the \
         violation (include only sentences or parts of sentences directly related to the\
          violation, but it should also not be too short that we're unable to understand\
          the violation) at the second index.\n\n**Cause**: An explanation of why this\
          text constitutes a violation on the third index.\n\nEnsure that you avoid making\
          up violations in the text. Additionally, refrain from making assumptions and \
         thoroughly examine both the [UserText] and [RuleText]. An example for the [UserText]\
          and the response given for the [UserText] while analysing [RuleText] is given below:\n\n[UserText] => [UserText]: \
         File Name: Document (1).pdf\n\nThis is the start of the document. This is the start of the document. This standard does not cover the Murabahah transaction and its various stages, nor does it address the issues relating to guarantees before concluding a Murabahah deal such as promise, Hamish Jiddiyyah (security deposit), and issues relating to guarantees for recovery of the debt created by the Murabahah transaction. This standard covers deferred payment sales that take place on a basis other than that of Murabahah. It also covers other trust and bargaining sales. When there is acceptance by the customer of an offer from the supplier that is either addressed to him personally, or that has no addressee, then the sale is not concluded with the customer, and it is permissible for the Institution to carry out Murabahah on the same item. It is not essential to exclude any prior contractual relationship between the customer who is the purchase orderer and the original supplier of the item ordered. It is not a requirement of Murabahah that the transaction between the two parties must genuinely, not fictitiously, exclude any prior contractual relationship. It is permissible to assign a contract that has been executed between the customer and the supplier of the ordered item to the Institution. This Is the end of the document. Zafar \
         \n\nResponse => This is the start of the document. This standard does not cover the Murabahah transaction and its various stages, nor does it address the issues relating to guarantees before concluding a Murabahah deal such as promise, Hamish Jiddiyyah (security deposit), and issues relating to guarantees for recovery of the debt created by the Murabahah transaction. This standard covers deferred payment sales that take place on a basis other than that of Murabahah. It also covers other trust and bargaining sales. When there is acceptance by the customer of an offer from the supplier that is either addressed to him personally, or that has no addressee, then the sale is not concluded with the customer, and it is permissible for the Institution to carry out Murabahah on the same item. It is not essential to exclude any prior contractual relationship between the customer who is the purchase orderer and the original supplier of the item ordered. It is not a requirement of Murabahah that the transaction between the two parties must genuinely, not fictitiously, exclude any prior contractual relationship. It is permissible to assign a contract that has been executed between the customer and the supplier of the ordered item to the Institution.', '']"},
        
        {"role": "user", "content": rules},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
    model=model, messages=messages, temperature=0)
    return response.choices[0].message["content"]


# def get_completion(prompt, rules, model="gpt-3.5-turbo-16k"):
#     messages = [{"role": "system", "content": "Given the provided [UserText] and [RuleText], your task is to \
#                  meticulously analyze whether the [UserText] violates any of the rules laid out \
#                  in the [RuleText]. The format of the [UserText] is as follows: \
#                  'File Name: {doc_name}\n{doc_text}\n\n' \
#                  In case of no violations return nothing. \
#                  If you find any violations, respond with an array which consists of three elements \
#                   and is in this format: [**FileName**, **SpecificText**, **Cause**] \
#                  **FileName**: The name of the file where the violation occurred at first index. \
#                  **SpecificText**: The specific piece of text within [UserText] causing the violation \
#                  (include only sentences or parts of sentences directly related to the violation, but it should also not be too short that we're unable to understand the violation) \
#                   at second index. **Cause**: An explanation of why this text constitutes a \
#                  violation on the third index. Ensure that you avoid making up violations in the text. \
#                  Additionally, refrain from making assumptions and thoroughly examine both the [UserText] and [RuleText]."},

#                 {"role": "user", "content": rules},
#                 {"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model, messages=messages, temperature=0)
#     return response.choices[0].message["content"]

def is_compliant(UserText, RuleText):
    prompt = f"[UserText]: {UserText}"
    rulesPrompt = f"[RuleText]: {RuleText}"
    # prompt = f"""
    # [UserText]: '''{UserText}'''

    # [RuleText]: '''{RuleText}'''
    # """
    response = get_completion(prompt, rules=rulesPrompt)
    return response
