from transformers import LlamaForCausalLM, CodeLlamaTokenizer

tokenizer = CodeLlamaTokenizer.from_pretrained("/home/pcl_poc/yizx/codellama-main/CodeLlama-7b-Python-HF")
model = LlamaForCausalLM.from_pretrained("/home/pcl_poc/yizx/codellama-main/CodeLlama-7b-Python-HF")
# PROMPT = '''def remove_non_ascii(s: str) -> str:
# """ <FILL_ME>
#     return result
# '''
PROMPT="""can you generate the AST for the following Python code snippet? Please take it step by step, 
    and check the programming logic at each step. Then, generate the whole AST as the final output at the very end, warping it
    with ###<<<AST>>>###from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\"\"\"\" Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"\"\"\"
    """
 
    
    
input_ids = tokenizer(PROMPT, return_tensors="pt")["input_ids"]
generated_ids = model.generate(input_ids, max_new_tokens=128)

filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]
print(PROMPT.replace("<FILL_ME>", filling))

