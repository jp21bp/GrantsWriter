##### Utilities file
    # Contains the following 2 utility classes:
        # Metrics = used to calculate the token usage of model invocations
        # Storage = used to save/retrieve data to a local DB


#### General libraries
from langchain_core.messages import AnyMessage
from copy import deepcopy
import pickle, sqlite3, json



















#### Metrics class
    # Keeps tracks of token usage
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
        
        #First, turn the "AnyMessage" into a dict
        message = dict(message)

        # Second, extract the needed component from the dictionary
        metadata = message['usage_metadata']

        # Third, format the extraction dictionary
        if metadata:
            extraction = {
                f"{name}":{
                    "input_tokens": metadata['input_tokens'],
                    "output_tokens": metadata['output_tokens'],
                    "total_tokens": metadata['total_tokens'],
                }
            }
        elif not metadata:
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

        #First, create a copy of the 'tokens_dict'
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

        # Second, extract the inner dictionary
        inner_dict = list(copy.values())[0]

        # Third, sum up the used tokens
        for category, amount in inner_dict.items():
            self.history['sum'][category] += amount

        # Fourth, insert the "tokens_dict" into the history
        self.history = self.history | copy

        # Fifth, delete the deepcopy
        del copy
        return self
























##### Storage class
    # Save and retrieve data to a local db
class Storage():
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

    #### Saving data to sqlite
    def save_data(self, data, data_id: int, data_name: str = "NoneGiven"):
        pickled_data = pickle.dumps(data)
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                f'CREATE TABLE IF NOT EXISTS {self.table_name} (data_id INTEGER, data_name VARCHAR(255), content BLOB)'
            )
            conn.execute(
                f'INSERT INTO {self.table_name} (data_id, data_name, content) VALUES (?,?,?)',
                (data_id, data_name, sqlite3.Binary(pickled_data))
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




























##### General Utilities
    # This class will contain all the fcns necessary for general usage
class Utilities():
    def __init__(self):
        self.finializer = '\n' + '=' * 50 + '\n'
            #For fomatting purposes
    def disect(self, message: AnyMessage, indent: int = 2, finish: bool = True):
        # Will printout "message" in a nice JSON format
        print(f'JSON disection of LC Message' + '\n')
        # First: turn the AIMEsage into a dicationary
        msg_dict = dict(message)
        # Second: turn the dict into json
        json_str = json.dumps(msg_dict, indent=indent)
        # Third: print json string with desired indentation
        print(json_str)
        if finish: print(self.finializer)


    def analyze_attrs(self, variable, num_spaces : int = 1, finish: bool = True):
        print(f'Analyzing attributes of {variable}' + '\n\n')
        for attr in dir(variable):
            if attr.startswith("_"): continue
                # These are dunder methods
            print(f"Data Type: {type(attr)}")
            print(f"Name of attr: {attr}")
            print(f"Attribute details: {variable.__getattribute__(attr)}")
            print('\n'* num_spaces)
        if finish: print(self.finializer)

    def analyze_mro(self, variable, num_spaces: int = 1, finish: bool = True):
        print(f'Analyzing MRO of {variable}' + '\n\n')
        print(f"Data Type: {type(variable)}")
        for clase in type(variable).mro():
            print(f"Class:{clase.__module__}")
            print(f"Name: {clase.__name__}")
            print('\n'*num_spaces)
        if finish: print(self.finializer)

    def multi_analysis(self, variable, num_spaces: int = 1):
        print(f'Full analysis on {variable}')
        self.analyze_attrs(variable, num_spaces, False)
        self.analyze_mro(variable, num_spaces, False)
        print(self.finializer)





