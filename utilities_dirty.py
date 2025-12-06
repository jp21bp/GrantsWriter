###### This file will contain all the metrics that will be used to 
# test the tokens that are sused by the models when they are exeuting 
# on their given prompts
from langchain_core.messages import AnyMessage, AIMessage
from copy import deepcopy
import pickle, sqlite3, json


##### Metrics class
    # Keep track of token usage
class Metrics():
    def __init__(self):
        self.history: dict[str,dict[str,int]] = {
            "sum":{
                "input_tokens": 0,
                "output_tokens": 0,
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
    
    def extract_tokens_used(self, message: AnyMessage, name: str) -> dict:
        # Will extract that tokens that were used in a given model executioon
        # Should be in format {'prompt': x, 'completion': y, 'total': z}
        
        #First, turn the AIMessage into a dict
        msg = dict(message)
        #Then extract the needed component
        metadata = message['usage_metadata']
            #Where to find the token usage metrics
            # This should be a DICTIONARY 
        if metadata:
            # In here the metadata is not empty
            extraction = {
                f"{name}":{
                    "input_tokens": metadata['input_tokens'],
                    "output_tokens": metadata['output_tokens'],
                    "total_tokens": metadata['total_tokens'],
                }
            }
        elif not metadata:
            # In here the metada is empty
            print(f"Error extracting '{name}' - creating negative values")
            extraction = {
                f"{name}":{
                    "input_tokens": -1,
                    "output_tokens": -1,
                    "total_tokens": -1,
                }
            }
        return extraction

    def aggregate(self, tokens_dict: dict) -> dict:
        # Will aggregate the tokens from a given "tokens_dict" into 
                # "self.history" dict
        # Will also sum up the tokens into the "sum" section of the
                # "self.history" dictionary
        copy = deepcopy(tokens_dict)
            #This is done bc of the following case study:
                # Consider the following:
                    # p1 = Metrics(); p1.history['sum']['prompt_tokens'] = 99
                    # p2 = Metrics(); p3 = deepcopy(p1)
                #Thus
                    #p3.aggregate(p2.history) = {'sum': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}}
                            # = p3.history = p2.history
                    # This makes sense, since p3 | p2 => p2 overrules
                # BUT
                    # p3.aggregate(p1.history) = {'sum': {'prompt_tokens': 99, 'completion_tokens': 0, 'total_tokens': 0}}
                            # = p3.history = p1.history
                            # AND ALSO = p2.history
                    # The p2.history changing does NOT make sense
                        # Why does p2 change when it wasn't invoked in the function?
                            # There must be some lingering connection from the first fcn
                # Using "deepcopy" resolves this issue
        inner_dict = list(copy.values())[0]
        for category, amount in inner_dict.items():
            self.history['sum'][category] += amount
        self.history = self.history | copy
        del copy
        return self



#### Test cases
# new = Metrics()

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

# print(new.aggregate(first_chain).history)
# print(new.aggregate(second_chain).history)

# print(new.aggregate(first_chain).aggregate(second_chain).history)

# ai_empty = AIMessage(content = "hello")

# print(new.extract_tokens_used(ai_empty, 'empty'))

























##### Storage class
    # Save and retrieve data to a local db
class Storage():
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

    #### Saving data to sqlite
    def save_data(self, data, data_id: int):
        pickled_data = pickle.dumps(data)
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} (data_id INTEGER, content BLOB)'
            )
            conn.execute(
                f'INSERT INTO {self.table_name} (data_id, content) VALUES (?,?)',
                (data_id, sqlite3.Binary(pickled_data))
            )
            conn.commit()
            return data_id + 1

    #### Retrieving data from sqlite
    def retrieve_data(self, data_id: int):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                f'SELECT content FROM {self.table_name} WHERE data_id = ?',
                (data_id,)
            )
            row = cursor.fetchone()
            if row:
                unpickled_data = pickle.loads(row['content'])
                return unpickled_data
            else:
                print('Error: content not found')
                return


# #### Test cases

# test1 = "hello"
# test2 = 'hola'

# DB_NAME = 'test.db'
# storage1 = Storage(DB_NAME, 'test1')
#     # Should create "test1" table
# storage2 = Storage(DB_NAME, 'test2')
#     # Should create "test2" table in same db above

# print(storage1.save_data(test1, 2))
# print(storage2.save_data(test2, 5))

# print(storage1.retrieve_data(2))
# print(storage2.retrieve_data(5))



































##### General class
    # This class will contain all the fcns necessary for general usage
class Utilities():
    def __init__(self):
        self.finializer = '\n' + '=' * 50 + '\n'
    def disect(self, message: AIMessage, indent: int = 2, finish: bool = True):
        # This will technically be used to breakdown any complex dict
        # However, it will mainly be used to disect "AnyMessage" 
                #types in langchain
        # NOte: technically I can turn it into JSON and then use
                # one of the fcns associated with JSon
            # BUT i want to try full tweaking abilities of the output
                    # format of these dictionaries
        print(f'JSON disection of LC Message' + '\n')
        #First: turn the AIMEsage into a dicationary
        msg_dict = dict(message)
        # SEcond: turn the dict into json
        json_str = json.dumps(msg_dict, indent=indent)
        # Third: print json string with desired indentation
        print(json_str)
        if finish: 
            print(self.finializer)


    def analyze_attrs(self, variable, num_spaces : int = 1, finish: bool = True):
        # print(dir(variable))
        #     # "dir" gets ALL the attributes of "variable"
        #     # EX: [__init__, ..., __getattribute__,...]
        # print('\n\n')
        print(f'Analyzing attributes of {variable}' + '\n\n')
        for attr in dir(variable):
            if attr.startswith("_"):
                # THese are dunder methods
                continue
            print(f"Data Type: {type(attr)}")
            print(f"Name of attr: {attr}")
            print(f"Attribute details: {variable.__getattribute__(attr)}")
            print('\n'* num_spaces)
        if finish: 
            print(self.finializer)

    def analyze_mro(self, variable, num_spaces: int = 1, finish: bool = True):
        print(f'Analyzing MRO of {variable}' + '\n\n')
        print(f"Data Type: {type(variable)}") # Prints type of "variable"
        for clase in type(variable).mro():
            print(f"Class:{clase.__module__}")
            print(f"Name: {clase.__name__}")
            print('\n'*num_spaces)
        if finish: 
            print(self.finializer)

    def multi_analysis(self, variable, num_spaces: int = 1):
        print(f'Full analysis on {variable}')
        self.analyze_attrs(variable, num_spaces, False)
        self.analyze_mro(variable, num_spaces, False)
        print(self.finializer)





