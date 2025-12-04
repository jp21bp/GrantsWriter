###### This file will contain all the metrics that will be used to 
# test the tokens that are sused by the models when they are exeuting 
# on their given prompts
from langchain_core.messages import AnyMessage, AIMessage


class Metrics():
    def __init__(self):
        self.history: dict[str,dict[str,int]] = {
            "sum":{
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }
        }
            #Syntax:
            # {
            #     "first_chain":{
            #         "prompt_tokens": x,
            #         "completion_tokens": y,
            #         "total_tokens": z,
            #     },
            #     "second_chain":{
            #         "prompts_tokens": a,
            #         "completions_tokens": b,
            #         "total_tokens": c,
            #     },
            #     "sum":{
            #         "prompts_tokens": a+x,
            #         "compeltions_tokens": b+y,
            #         "total_tokens": c+z,
            #     }
            # }
    
    def extract_tokens_used(self, msg: AnyMessage, name: str) -> dict:
        # Will extract that tokens that were used in a given model executioon
        # Should be in format {'prompt': x, 'completion': y, 'total': z}
        metadata = msg.response_metadata
        if metadata:
            # In here the metadata is not empty
            extraction = {
                f"{name}":{
                    "prompt_tokens": metadata['token_usage']['prompt_tokens'],
                    "completion_tokens": metadata['token_usage']['completion_tokens'],
                    "total_tokens": metadata['token_usage']['total_tokens'],
                }
            }
        elif not metadata:
            # In here the metada is empty
            print(f"Error extracting '{name}' - creating negative values")
            extraction = {
                f"{name}":{
                    "prompt_tokens": -1,
                    "completion_tokens": -1,
                    "total_tokens": -1,
                }
            }
        return extraction

    def aggregate(self, tokens_dict: dict) -> dict:
        # Will aggregate the tokens from a given "tokens_dict" into 
                # "self.history" dict
        # Will also sum up the tokens into the "sum" section of the
                # "self.history" dictionary
        inner_dict = list(tokens_dict.values())[0]
        for category, amount in inner_dict.items():
            self.history['sum'][category] += amount
        self.history = self.history | tokens_dict
        return self.history



#### Test cases
new = Metrics()

# first_chain = {
#     'first_chain': {
#         'prompt_tokens': 3, 
#         'completion_tokens': 3, 
#         'total_tokens': 3
#     }
# }

# second_chain = {
#     'second_chain':{
#         'prompt_tokens': 4,
#         'completion_tokens': 5,
#         'total_tokens': 6
#     }
# }

# print(new.aggregate(first_chain))
# print(new.aggregate(second_chain))

ai_empty = AIMessage(content = "hello")

print(new.extract_tokens_used(ai_empty, 'empty'))


