###### Main Grants Writer File
    # This file will contain the graph of the grant writer agent
    # It will also integrate the following files:
        #"rag_clean.py"
        #"mini_agents_clean.py"
    ### AFter baseline grant writer, should I 
            # incorporate long-term memory?
    # The following agents will be made:
        # Planner: RAG -> 2 Summarizer agents
            # RAG = extract content related to a theme/query
            # Planner = create a plan to write the grant
            # Summarizers = use the plan and create the grant halves
        # Draft : 2 summarizers -> draft
            # It'll unite the 2 halves of grant
            # Results in full working draft of grant
        # Critique: Draft -> critique
            # Analyzes the draft 
            # Creates way to make th draft better
            # Note: There will be a conditional loop here
                # If revisions > max_revision : goto END
        # Web/RAG : critique -> new info
            # WIll retrieve new info based on critique
            # Still deciding b/w the following:
                # Use the Web to get new info?
                # Use the RAG again from organizations?
                    # It would get new context info from organizations


#####Important notes
####Concurrent node execution
    # All concurrent nodes w.in a single "super-step" share and 
            #upate a SINGLE, UNIFIED snapshot
    # All nodes executing in parallel receive the SAME CURRENT state
            # as input
    # Once all nodes finish, LG SYNCH their outputs
        # Updates are then merged back into the single, global state
    # If multiple concurrent nodes attempt to update the same state key,
            # you MUST define a reducer fc (ex: "operator.add")

##### General setup
#### Importing libraries
from dotenv import load_dotenv
import os
import operator
# import pickle
# import sqlite3
# import threading
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
# from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AnyMessage,\
    HumanMessage, AIMessage, SystemMessage
from langchain_core.messages.utils import merge_message_runs
from pydantic import BaseModel
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
# from IPython.display import Image
from langchain_google_genai import ChatGoogleGenerativeAI
# from rag_clean import RAG
from mini_agents_dirty import MiniAgent, SystemPrompts
from utilities_clean import *

##### Setting up environment
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")






























# ##### Setting up pickle and sqlite helper
# #### Saving data
# def save_data(db_name, data, id_counter: int):
#     pickled_data = pickle.dumps(data)
#     with sqlite3.connect(db_name) as conn:
#         # "data" = table's name
#         conn.execute(
#             'CREATE TABLE IF NOT EXISTS data (id INTEGER, content BLOB)'
#         )
#         conn.execute(
#             'INSERT INTO data (id, content) VALUES (?,?)',
#             (id_counter, sqlite3.Binary(pickled_data))
#         )
#         conn.commit()
#         return id_counter + 1

# #### Retrieving data from sqlite
# def retrieve_data(db_name, index):
#     with sqlite3.connect(db_name) as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute(
#             'SELECT content FROM data WHERE id = ?',
#             (index,)
#         )
#         row = cursor.fetchone()
#         if row:
#             unpickled_data = pickle.loads(row['content'])
#             return unpickled_data
#         else:
#             print('Error: content not found')
#             return





##### Intialize agent components
#### Model
# llm = ChatMistralAI(
#     api_key= mistral_api_key,
#     model_name= 'mistral-small'
# )

# llm = ChatGoogleGenerativeAI(
#     api_key=google_api_key,
#     model="gemini-2.5-flash-lite",
#     # max_tokens=128
# )

# base_llm = llm
fake_llm = None
#### RAG
# base_rag = RAG()
fake_rag = None






















##### PLaying with llm Cohere API
#### Simple invocation
# result = llm.invoke('hi')
# print(result)
# with open('output.pkl', 'wb') as file:
#     pickle.dump(result, file)
# print('success')

#### Trying out db helper fcns
### Ssaving data
# result = llm.invoke('hi!')
# print(result)
# id_counter = 1
# id_counter = save_data(DB_NAME, result, id_counter)
# print(id_counter)

### REtrieving saved data 
# data = retrieve_data(DB_NAME, 1)
# print(type(data))
# print(data)
# print(data.content)
# print(data.response_metadata)
# print(data.response_metadata['model_name'])
























##### Creating agent prompts
PLAN_PROMPT = """\
You are an expert writer tasked with writing \
a high level outline of a grant proposal. The \
grant outline will contain eight sections: Cover \
letter, Executive summary, Statement of Need, \
Goals and objectives, Methods and strategies, \
Plan of evaluation, Budget information, and \
Organizational background. You will be given a \
Pydantic model with fields corresponding to each one \
of these sections, where you will place the section \
outline.  Take into consideration the doner \
requirements, which are: {requirements}.\
"""
# Write the section outline for the following 
    # theme: {theme}.
DRAFT_PROMPT = """\
You are an experienced, senior grant writer. Your task \
is to unite previously created proposal components of the grant. The \
first half of the grant is:

<First half of grant>
{first_half}
</First half of grant>

The second half of the grant is:

<Second half of grant>
{second_half}
</Secon half of grant>

The doner requirements are: {requirements}\
"""
    # Using these halves, create a complete grant proposal for the 
    # following theme: {theme}. 

CRITIQUE_PROMPT = """\
You are a senior Grants officer reviewing a grant propsal from \
a non-profit organization for the following theme: {theme}. \
Your task is to generate critique and recommendations for the user's submission draft. \
Provide detailed recommendations, including requests for length, \
depth, style, etc.

<User Submission Draft>
{draft}
</User Submission Draft>\
"""
# The current draft submission is: {draft}

INVESTIGATION_PROMPT = """\
You are an experienced mentor in providing support for writing grant \
proposal for non-profit organizations. Your task is to create a simple \
RAG prompt that will look into the applicant's organizational documents. \
You goals is to retrieve more contextual documents that will help improve \
the current grant draft based on provided techniques.

<Current draft>
{draft}
</Current draft>\
"""
# The critique for this draft is: {critique}. Execute and complete
# your task.

































##### Testing out diff. langchain "Messages"
#### Investigating "SystemMessage" object
# for attr in dir(SystemMessage):
#     if attr.startswith("_"): continue
#     print(attr)
#     try: print(SystemMessage.__getattribute__(attr))
#     except: continue
#     print('\n'*2)

#### PLaying with "ChatPromptTemplate"
### Replacing placeholders
# prompt = ChatPromptTemplate.from_messages([
#     ("system", PLAN_PROMPT),
#     ("user", "Write the section outline for the following theme: {theme}.")
# ])
# print(prompt.invoke({'theme': 'UNO', 'requirements': 'DOS'}))

### Checking out missing placeholder replacements
# prompts = ChatPromptTemplate.from_messages([
#     ('system', PLAN_PROMPT),
#     ("user", "Write all section outlines for the following theme: {theme}.")
# ])

### Working with different ordering of the placeholders
# msgs = prompts.invoke({
#     "requirements": 'UNO',
#     "theme": 'DOS',
# })
# print(msgs)








































##### Sampling and playing with Agent graph and db integrations
    #NOte: both "####" sections work
#### Create Agent state
# class AgentState(TypedDict):
#     # Note: ALL "Annotated" attrs WILL show up in results
#         # Even if they're empty, the will be initialized and shown
#     # General fields
#     msgs: Annotated[List[AnyMessage], operator.add]
#         # Needed to store the LC "Messages" from agents
#         # REQUIRES inputs to be in [] bc of "List"
#     theme: str
#     doner_requirements: str
#     num_revisions: int
#     max_revisions: int
#     id_counter: int 
#         #DB Index field
#     ## Node related fields
#     # plan: SectionOutlines
#     draft: str
#     critique: str
#     rag_context: Annotated[List[str], operator.add]
#         # REQUIRES inputs to be in [] bc of "List"
#     # random: Annotated[List[int], operator.add]

#### Create Sample Agent graph for testing invocation and saving to DB
### Create class
# class Agent:
#     def __init__(self, llm):
#         graph = StateGraph(AgentState)
#         graph.add_node('sample', self.sample_node)

#         graph.add_edge('sample', END)
#         graph.set_entry_point('sample')
#         self.graph = graph.compile(
#             # checkpointer= memory,   #FOr short-term memory
#             # store= store,   # For long-term memory
#         )
#         self.llm = llm

#     def sample_node(self, state: AgentState):
#         prompt = 'hola!'
#         response = self.llm.invoke(prompt)
#         id_counter = state['id_counter']
#         print(response)
#         print(f'index for sample response is {id_counter}')
#         id_counter = save_data(DB_NAME, response, id_counter)
#         print(f'new counter: {id_counter}')
#         return {'msgs': [response], 'id_counter': id_counter}
        
### Create visual of graph
# abot = Agent(base_llm)
# print(abot.graph.get_graph().draw_mermaid()).
# print(abot.graph.get_graph().draw_ascii())

### Execute the graph
# result = abot.graph.invoke({'id_counter': 2})
# print('psot execution')
# print(type(result))
# print(result)
# for k,v in result.items():
#     print(f"Key: {k}")
#     print(f"value: {v}")
#     print('\n'*2)



#### Create sample class to test interactions from db data retrieved
### Create class
# class Agent:
#     def __init__(self, llm):
#         graph = StateGraph(AgentState)
#         graph.add_node('sample', self.sample_node)
#         graph.add_node('sample_2', self.sample_node)
#         graph.add_edge('sample', 'sample_2')
#         graph.add_edge('sample_2', END)
#         graph.set_entry_point('sample')
#         self.graph = graph.compile(
#             # checkpointer= memory,   #FOr short-term memory
#             # store= store,   # For long-term memory
#         )
#         self.llm = llm

#     def sample_node(self, state: AgentState):
#         data = retrieve_data(DB_NAME, 2)
#         print(type(data))
#         return {'msgs': [data]}
#         # return {'rag_context': [data]}

# ### Visualize graph
# abot = Agent(fake_llm)
# print(abot.graph.get_graph().draw_ascii())

# ### Execute the graph
# result = abot.graph.invoke({})
# print('psot execution')
# # print(type(result))
# # print(result)
# for k,v in result.items():
#     print(f"Key: {k}")
#     print(f"value: {v}")
#     print(len(v))
#     print('\n'*2)

























##### Creating main agent graph
#### Creating pydantic models
### For Planning node
class SectionOutlines(BaseModel):
    """Stores the outline for each section of the grant proposal"""
    cover_letter: str
    executive_summary: str
    statement_of_need: str
    goals_and_objective: str
    methods_and_strategies: str
    plan_of_evaluation: str
    budget_information: str
    organizational_background: str


#### Create Agent state
    # SAme as sample agent state
class AgentState(TypedDict):
    # Note: I'm going to change all the "str" to "AIMEssage"
        # This will be useful when trying to calculatre the tokens
                # that are consumed per ai call
        # They can be used to create a metriccs function to guage the 
                # cost of running that particulat prompt for that 
                # particular model
            # This will help gauge how much it would be to use the 
                    # other models
            # Especially since the input tokens will remain the same
            # The only thing that changes per model is the output tokens
                #But this canb be limited when initialiizing the model
    # Note: ALL "Annotated" attrs WILL show up in results
        # Even if they're empty, the will be initialized and shown
    # General fields
    messages: Annotated[List[AnyMessage], operator.add]
        # Needed to store the LC "Messages" from agents
        # REQUIRES inputs to be in [] bc of "List"
    theme: str
    doner_requirements: str
    num_revisions: int
    max_revisions: int
    id_counter: int 
        #DB Index field
    # Node related fields
    plan: SectionOutlines
        # Lo voy a dejar con SectionOutlines
            # Por que el resto del codigo esta formateado con esta base
    summarizer_sections: Annotated[dict[str, AIMessage], operator.or_]
    mini_sections_first_half: Annotated[dict[str, AIMessage], operator.or_]
    mini_sections_second_half: Annotated[dict[str, AIMessage], operator.or_]
        #Use to store all the mini agent outputs    
    draft: Annotated[List[AIMessage], operator.add]
    critique: Annotated[List[AIMessage], operator.add]
    rag_context: Annotated[List[str], operator.add]
        # REQUIRES inputs to be in [] bc of "List"
        # Will NOT be an "AIMessage" bc "rag.invoke" returns a str

#### Setting up utilites
DB_NAME = 'output.db'
TABLE_NAME = 'main'
DATA_ID = 1
storage = Storage(DB_NAME, TABLE_NAME)

# analyzer = Analyzer()
    #IF it's needed


#### Create graph
    #Proceso general para los nodes:
        # Hacer una invocacion
        # Salvar los reusltados en un DB
        # Analizar los metrics/token usados
class Agent:    #GrantsAgent
    def __init__(self, llm, rag, mini_sys_prompts: dict):
        graph = StateGraph(AgentState)
        ## Creating nodes
        graph.add_node('rag', self.rag_node)
        graph.add_node('planner', self.plan_node)
        graph.add_node('cover_sec', self.cover_node)
        graph.add_node('executive_sec', self.executive_node)
        graph.add_node('need_sec', self.need_node)
        graph.add_node('goal_sec', self.goal_node)
        graph.add_node('methods_sec', self.methods_node)
        graph.add_node('eval_sec', self.eval_node)
        graph.add_node('budget_sec', self.budget_node)
        graph.add_node('background_sec', self.background_node)
        graph.add_node('summarizer_one', self.summarizer_one)
        graph.add_node('summarizer_two', self.summarizer_two)
        graph.add_node('draft', self.draft_node)
        graph.add_node('critique', self.critique_node)
        graph.add_node('investigation', self.investigation_node)         

        graph.set_entry_point('rag')
        graph.add_edge('rag', 'planner')
        graph.add_edge('planner', 'cover_sec')
        graph.add_edge('planner', 'executive_sec')
        graph.add_edge('planner', 'need_sec')
        graph.add_edge('planner', 'goal_sec')
        graph.add_edge('planner', 'methods_sec')
        graph.add_edge('planner', 'eval_sec')
        graph.add_edge('planner', 'budget_sec')
        graph.add_edge('planner', 'background_sec')

        graph.add_edge('cover_sec','summarizer_one')
        graph.add_edge('executive_sec','summarizer_one')
        graph.add_edge('need_sec','summarizer_one')
        graph.add_edge('goal_sec','summarizer_one')
        graph.add_edge('methods_sec','summarizer_two')
        graph.add_edge('eval_sec','summarizer_two')
        graph.add_edge('budget_sec','summarizer_two')
        graph.add_edge('background_sec','summarizer_two')

        graph.add_edge('summarizer_one', 'draft')
        graph.add_edge('summarizer_two', 'draft')

        graph.add_conditional_edges(
            'draft',
            self.should_continue,
            {END: END, 'critique': 'critique'}
        )

        graph.add_edge('critique', 'investigation')
        graph.add_edge('investigation', 'draft')


        self.graph = graph.compile(
            # checkpointer= memory,   #FOr short-term memory
            # store= store,   # For long-term memory
        )

        # self.lock = threading.Lock()
        self.llm = llm
        self.rag = rag
        self.mini_sys_prompts = mini_sys_prompts
        self.metrics = Metrics()
        # print(self.mini_sys_prompts)
        # for k,v in self.mini_sys_prompts.items():
        #     print(k)
        #     print(v)
        #     print('\n'*3)
        # print(self.mini_sys_prompts['first_half'])



    def should_continue(self, state: AgentState):
        # print('CONDITION')
        #Recall: first draft starts at revision 0
        if state['num_revisions'] >= state['max_revisions']:
            return END
        return 'critique'




    def rag_node(self, state: AgentState):    #Original
        ### Invocation
        name = 'rag_node'
        user_query = state['messages'][0]
        id_counter = state['id_counter']
        rag_result, id_counter, rag_metrics = self.rag.invoke(user_query, id_counter,name)
            #NOte: "rag_result" will NOT be an "AIMessage"
            # It'll be a string
        print(f"'rag' db index at index: {id_counter}")
        print(rag_result)
        ### SAving the rag string data
        id_counter = storage.save_data(rag_result, id_counter, name)
        ### Analyzing the metrics used
        self.metrics = self.metrics | rag_metrics
        print('Rag metrics')
        print(self.metrics.history)
        return {"rag_context": [rag_result], 
                "id_counter": id_counter,
                "messages": AIMessage(content='RAG')}


    # def rag_node(self, state:AgentState):
    #     # print('ONE')
    #     # USing retrieve from db, to avoid api usage
    #     data = retrieve_data(DB_NAME, 1)
    #     # print(type(data))
    #     # print(data)
    #     # return {'msgs': [data]}
    #     # print(state)
    #     return {'rag_context': [data]}
    






    def plan_node(self, state: AgentState):   #Original
        ### Invocacion
        name = 'plan_node'
        USER_PROMPT = \
"""\
Write all section outlines for the following theme: {theme}. \
The organizational context regarding this proposal and theme is:
<Organizational Context>
{context}
</Organizational Context>\
# """
#         print(USER_PROMPT)
#         return
        prompts = ChatPromptTemplate.from_messages([
            ('system', PLAN_PROMPT),
            ("user", USER_PROMPT)
        ]) 

        msgs = prompts.invoke({
            "requirements": state['doner_requirements'],
            "theme": state['theme'],
            "context": state['rag_context'][-1] #Es una lista
        })
        # print(msgs)
        # return

        model = self.llm.with_structured_output(SectionOutlines, include_raw=True)
        plan = model.invoke(msgs)
            # Va a regresar un dict con el siguiento syntax:
                #{'parsed': SectionOutline, 'raw': AIMessage, 'otro':... }
        print(f"'Plan' DB data is with index: {state['id_counter']}")
        print(plan)
        ### Salvar los resultados
        id_counter = state['id_counter']
        id_counter = storage.save_data(plan, id_counter, name)
            # Vamos a salvar el objeto/dict completo
                #Con {'parsed':..., 'raw': ..., 'otro': ...}
        ### Analizar los metricos
        extract = self.metrics.extract_tokens_used(plan['raw'], name)
        self.metrics = self.metrics.aggregate(extract)
        print('plan metrics')
        print(self.metrics.history)
        return {"plan" : plan['parsed'], 
                'id_counter' : id_counter,
                'messages': plan['raw']}


    # def plan_node(self, state:AgentState):
    #     # id_counter = state['id_counter']
    #     # print(f'START: {id_counter}')
    #     # id_counter += 1
    #     # state['id_counter'] = id_counter
    #     # new_id = state['id_counter']
    #     # print(f'AFTER: {new_id}')

    #     # print(state['rag_context'])
    #     # print('TWO')
    #     data = retrieve_data(DB_NAME, 2)
    #     # print(type(data))
    #     # print(data.cover_letter)
    #     # print(data.organizational_background)
    #     # print(type(data).model_fields.items())
    #     # print(dir(data))
    #     # print(data.__getattribute__('cover_letter'))
    #     overview = type(data).model_fields
    #         # This is a dictionary
    #         # Syntax: {key = fieldName, value = fieldRequirements}
    #     # print(items)
    #     details = data.model_dump()
    #         #This is also dictionary
    #         # Syntax: {key = fieldName, vluew = attribute values}
    #     # print(details)
    #     # for k,v in details.items():
    #     #     print(k)
    #     #     print(v)
    #     #     print('\n'*2)
    #     return {'plan': data}




    def mini_agent_template(self, state: AgentState, key: str):
        ### Invocacion
        replacements = {
            'plan': state['plan'].__getattribute__(key),
            'theme': state['theme'],
            'requirements': state['doner_requirements'],
        }
        sys_prompt = self.mini_sys_prompts[key]
        agent = MiniAgent(sys_prompt, replacements)
        print(f'Prompt for {key}: {agent.system}' + '\n' * 4)
        response = agent()
            # Sera de tipo "AIMessage"

        ### Guardar los resultados
            # Por el hecho de concurencia con estos nodos,
                    # se hara despues
        
        ### Analizar los metricos
            # Esta es una parte donde no se cual sera la ejecucion final
            # Si trabajo como es esperado, lo dejamos asi
            # Si no trabajo, pondremos el "self.metrics" en "AgentState"
                # PERO con esto tendre que cambiar TODOS los otros nodes
        extract = self.metrics.extract_tokens_used(response, key)
        self.metrics = self.metrics.aggregate(extract)
        print(f'metrics for {key}')
        print(self.metrics.history)

        ### Para hacer debug
        # response = AIMessage(content=f'This is for section {key}')# Tryout
        # messages = [    #Just to try out
        #     SystemMessage(content=key),
        #     HumanMessage(content=key),
        #     AIMessage(content=key)
        # ]

        ### Para mejor cuadrar cada AIMEssage con su node
        section_annotation = AIMessage(content=key)
        response = merge_message_runs([section_annotation, response], chunk_separator = " -- ")[0]
            #REturns an AIMessage
        return response
            # Regresando ".content" pq se va a utilizar directamente
                    # en los summarizers
            # O, LO QUE SE PUEDE HACER, es justamente guardar con AIMessage
                    # y despues extraer los contenidos cuando se van a usar
                    # con los summarizers
                # Esto se va hacer mejor para poder verificar los resultados de 
                        # self.metrics


    def print_sys(self, key: str, prompt: str):
        # to_print = f'Prompt for {key}:\n{prompt}' + '\n' * 4
        # print(to_print)
        return

    def cover_node(self, state: AgentState):
        # key = "cover_letter"
        # replacements = {
        #     'plan': state['plan'].__getattribute__(key),
        #     'theme': state['theme'],
        #     'requirements': s .....ate['doner_requirements'],
        # }
        # sys_prompt = self.mini_sys_prompts[key]
        # agent = MiniAgent(sys_prompt, replacements)
        key = 'cover_letter'
        # print('HERE')
        response = self.mini_agent_template(state, key)
        return {'mini_sections_first_half': {'section_one': response}, 
                'messages': [response]}

    def executive_node(self, state: AgentState):
        # key = 'executive_summary'
        # replacements = {
        #     'plan': state['plan'].__getattribute__(key),
        #     'theme': state['theme'],
        #     'requirements': state['doner_requirements'],
        # }
        # sys_prompt = self.mini_sys_prompts[key]
        # agent = MiniAgent(sys_prompt, replacements)
        key = 'executive_summary'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_first_half': {'section_two': response}, 
                'messages': [response]}
    
    def need_node(self, state: AgentState):
        key = 'statement_of_need'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_first_half': {'section_three': response}, 
                'messages': [response]}
    
    def goal_node(self, state: AgentState):
        key = 'goals_and_objective'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_first_half': {'section_four': response}, 
                'messages': [response]}
    
    def methods_node(self, state: AgentState):
        key = 'methods_and_strategies'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_second_half': {'section_one': response}, 
                'messages': [response]}
    
    def eval_node(self, state: AgentState):
        key = 'plan_of_evaluation'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_second_half': {'section_two': response}, 
                'messages': [response]}
    
    def budget_node(self, state: AgentState):
        key = 'budget_information'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_second_half': {'section_three': response}, 
                'messages': [response]}
    
    def background_node(self, state: AgentState):
        key = 'organizational_background'
        response = self.mini_agent_template(state, key)
        return {'mini_sections_second_half': {'section_four': response}, 
                'messages': [response]}






    def summarizer_agent_template(self, state: AgentState, key: str):
        ### Invocacion
        replacements = {
            'section_one': state[f'mini_sections_{key}']['section_one'].content,
            'section_two': state[f'mini_sections_{key}']['section_two'].content,
            'section_three': state[f'mini_sections_{key}']['section_three'].content,
            'section_four': state[f'mini_sections_{key}']['section_four'].content,
            'theme': state['theme'],
            'requirements': state['doner_requirements'],
        }
            #Recordar extraer el "content" de "AIMessage"
        sys_prompt = self.mini_sys_prompts[f'{key}']
        # return sys_prompt
        agent = MiniAgent(sys_prompt, replacements)
        print(f'Prompt for {key}: {agent.system}' + '\n' * 4)
        response = agent()


        ### Guardar los resultados
            # Como los otros MiniAgents, esto se va hacer todo en
                    #uno para evitar conflictos de concurencia

        ### Analizando los metricos
        extract = self.metrics.extract_tokens_used(response, key)
        self.metrics = self.metrics.aggregate(extract)
        print(f'metrics for {key}')
        print(self.metrics.history) 



        ### Para hacer debug
        # response = AIMessage(content=f'This is the {key} part')# Tryout
        # messages = [    #Just to try out
        #     SystemMessage(content=key),
        #     HumanMessage(content=key),
        #     AIMessage(content=key)
        # ]
        

        ### Para cuadrar node con AIMessage
        section_annotation = AIMessage(content = key)
        response = merge_message_runs([section_annotation, response], chunk_separator = " -- ")[0]

        return response
            # "agent" return only needed to check syst prompt

    def summarizer_one(self, state: AgentState):
        key = 'first_half'
        # print(state[f'mini_sections_{key}_half'])
        # print(self.mini_sys_prompts[f'{key}_half'])
        # print(state[f'mini_sections_{key}_half']['section_four'].content)
        # print(self.summarizer_agent_template(state, key))
        response = self.summarizer_agent_template(state, key)
        return {'summarizer_sections': {f'{key}': response}, 
                'messages': [response]}
    
    def summarizer_two(self, state: AgentState):
        key = 'second_half'
        # print(self.mini_sys_prompts[f'{key}_half'])
        # print(self.summarizer_agent_template(state, key))
        # print(' HERE')
        response = self.summarizer_agent_template(state, key)
        return {'summarizer_sections': {f'{key}': response}, 
                'messages': [response]}





    def minis_to_db(self, state: AgentState):
        # This fcn will save the results from the 8 minis and
                #2 summarizers into the DB
        # This is done to avoid working with the concurrency threads
                # that are executed when the 10 minis are 
                # executed in parallel
        # This is fcn is only going to be called ONCE, during the 
                # first iteration of the draft
            # Since the minis won't be executed more than once
        # print('saving minis')
        id_counter = state['id_counter']
        to_save = [
            'mini_sections_first_half',
            'mini_sections_second_half',
            'summarizer_sections',
        ]
        for keys in to_save:
            for name, AiMsg in state[keys].items():
                id_counter = storage.save_data(AiMsg, f'{keys}_{name}')
        return id_counter
        


    def draft_node(self, state: AgentState):
        ### SAving previous miniagents
        id_counter = state['id_counter']
        if state['num_revisions'] == 0:
            id_counter = self.minis_to_db(state)

        ### Invocacion
        name = f"draft_{state['num_revisions']}"
        replacements = {
            'first_half': state['summarizer_sections']['first_half'].content,
            'second_half': state['summarizer_sections']['second_half'].content,
            'requirements': state['doner_requirements'],
        }
        sys_prompt = DRAFT_PROMPT.format(**replacements)

        all_context = ''
        for context in state['rag_context']:
            all_context += context

        user_prompt = f"""\
Using the information above, create a full grant proposal draft for \
the following theme: {state['theme']}. Consider the following context, \
retrieved from the organization's webpage using RAG, when completing your task:

<RAG Organizational Context>
{all_context}
</RAG Organizational Context>\
"""
        prompts = ChatPromptTemplate.from_messages([
            ('system', sys_prompt),
            ("user", user_prompt)
        ]) 
        # print(prompts.invoke({}))
        draft = self.llm.invoke(prompts)
            # Sera un "AIMEssage"

        ### Guardar los resultados
        id_counter = storage.save_data(draft, id_counter, name)

        ### Analizar los metricos
        extract = self.metrics.extract_tokens_used(draft, name)
        self.metrics = self.metrics.aggregate(extract)
        print(f'{name} metrics')
        print(self.metrics.history)


        ### Para hacer debug
        # response = AIMessage(content='this is the draft')
        # draft = response.content
        # print('DRAFT DONE')
        # for i, context in enumerate(state['rag_context']):
        #     print(f"context {i}: ")
        #     print(context)
        #     print('\n' * 2)
        # print(f"this is revision: {state['num_revisions']}")


        return {
            'messages': [draft],
            'draft': [draft], 
            'num_revisions': state['num_revisions'] + 1,
            'id_counter' : id_counter,
        }


        # print(f"'Draft' DB data is with index: {state['id_counter']}")
        # print(draft)
        # id_counter = save_data(DB_NAME, draft, 3)
        # # id_counter = save_data(DB_NAME, plan, state['id_counter'])
        # return {"draft" : draft, 'id_counter' : id_counter}






    def critique_node(self, state: AgentState):
        ### Invocacion
        name = f"critique_{state['num_revisions']}"
        replacements = {
            'theme': state['theme'],
            'draft': state['draft'][-1].content,
        }
        sys_prompt = CRITIQUE_PROMPT.format(**replacements)
        # print(sys_prompt)
        prompts = ChatPromptTemplate.from_messages([
            ('system', sys_prompt),
            ("user", 'Execute your task.')
        ])
        # print(prompts.invoke({}))
        critique = self.llm.invoke(prompts)
            # Will be an AIMessage

        ### GUardar los resultados
        id_counter = state['id_counter']
        id_counter = storage.save_data(critique, id_counter, name)


        ### Analizar los metricos
        extract = self.metrics.extract_tokens_used(critique, name)
        self.metrics = self.metrics.aggregate(extract)
        print(f'{name} metrics')
        print(self.metrics.history)



        # ### Para hacer debug
        # response = AIMessage(content='this is a critique')
        # critique = response.content
        

        return {
            'messages': [critique],
            'critique': critique, 
            'id_counter': id_counter
        }
    


    def investigation_node(self, state: AgentState):
        # Note: this will perform TWO "save_data"
            # One for the rag prompt created
            # Other for the info retrieved from using that rag prompt
        
        ### Primera invocacion
        base_name = f"investigation_{state['num_revisions']}"
        name = base_name + '_new_rag_prompt'
        replacements = {
            'draft': state['draft'][-1].content,
        }
        sys_prompt = INVESTIGATION_PROMPT.format(**replacements)
        user_prompt = f"""\
The draft above has been given the following critique: \
{state['critique'][-1].content}. Create the RAG prompt, which will be fed \
to the organizational's website RAG agent.\
"""
        prompts = ChatPromptTemplate.from_messages([
            ('system', sys_prompt),
            ("user", user_prompt)
        ])
        # print(prompts.invoke({}))

        new_rag_prompt = self.llm.invoke(prompts)
            # SEra un AIMessage

        ### Guardar resultados
        id_counter = state['id_counter']
        id_counter = storage.save_data(new_rag_prompt, id_counter, name)

        ### Analizar los metricos
        extract = self.metrics.extract_tokens_used(new_rag_prompt, name)
        self.metrics = self.metrics.aggregate(extract)
        print(f'{name} metrics')
        print(self.metrics.history)




        ### Segunda invocacion
        name = base_name + '_new_rag_context'
        user_query = new_rag_prompt.content
        rag_result, id_counter, rag_metrics = self.rag.invoke(user_query, id_counter, name)
            #"Rag_result" = string

        print(f"{name} db index at index: {id_counter}")
        print(rag_result)

        ### Guardar los resultados
        id_counter = storage.save_data(rag_result, id_counter, name)

        ### Analizar los metricos
        self.metrics = self.metrics | rag_metrics
        print(f'{name} metrics')
        print(self.metrics.history)


        # ### Para hacer debug
        # response = AIMessage(content='this is a RAG response')
        # rag_prompt = response.content
        # human_query = HumanMessage(content=rag_prompt)
        # # rag_result = self.rag.invoke(human_query)
        # rag_result = 'this is a sample rag context retrieved'

        return {
            'messages': [new_rag_prompt, AIMessage(content=f'{name}')],
            'rag_context': [rag_result],
            'id_counter': id_counter,
        }









#### Initialize agent and visualize
sys_prompts_mini = SystemPrompts().create_prompts()
# agent = Agent(fake_llm, base_rag)
# agent = Agent(base_llm, base_rag)
# agent = Agent(base_llm, fake_rag)
agent = Agent(fake_llm, fake_rag, sys_prompts_mini)
print(agent.graph.get_graph().draw_ascii())

start_state = {
    'theme': 'educational projects',
    'doner_requirements': 'none',
    'num_revisions': 0,
    'max_revisions': 2,
    'id_counter': 3,
}
# result = agent.graph.invoke(start_state)

### Checking the response "AgentState", which is a "TypedDict" dict
# for k,v in result.items():
#     print(k)
#     print(v)
#     print('\n'*2)

### Checking the items that were saved in the DB
# for i in range(1,3):
#     print(f"Sowing index {i}")
#     print(storage.retrieve_data(DB_NAME, i))
#     print('\n' + '=' * 30 + '\n')









#### Invoking the agent
    # WIll requiring turning a user query into "HumanMessage"
    # That way it can be appended to "state['msgs']"
        #THis can later be used in the nodes themselves
### TRying out with ChatPromptTemplate
# prompt = ChatPromptTemplate.from_messages([
#     ("system", PLAN_PROMPT),
#     ("user", "Write the section outline for the following theme: {theme}.")
# ])
    #Doesn't quite work for what we want
        #THis sets up a prompts to be fed into a model
        # BUT we want to simply get a "HumanMessage" to fed into grpah state
    # The "type(prompt)" is "<class 'langchain_core.prompts.chat.ChatPromptTemplate'>'"
        #This won't be able to be appended to "state['msgs]"
            #Since this expects a list of "AnyMessage"
    # Technically it can be done if we INVOKE "ChatPromptTemplate"




### Trying out with HumanMessage
# user_query = [HumanMessage(content="what are current educational projects?")]
#     # Also going to need to provide id_counter
# starting_state = {
#     "msgs": user_query,
#     'id_counter': 1,
#     'theme': 'educational projects',
#     "doner_requirements": 'none',
#     'num_revisions': 0,
#     'max_revisions': 2,
# }
# result = agent.graph.invoke(starting_state)
#     # WORKS! Accepts inputs, tranlsates to user qury, adn returns rag output
















































