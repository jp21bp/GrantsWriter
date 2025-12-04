##### Utilities file
    # Contains the following 2 utility classes:
        # Metrics = used to calculate the token usage of model invocations
        # Storage = used to save/retrieve data to a local DB


#### General libraries
from langchain_core.messages import AnyMessage
from copy import deepcopy
import pickle, sqlite3




#### Metrics class
    # Keeps tracks of token usage
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





