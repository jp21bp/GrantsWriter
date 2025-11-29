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


##### General setup
#### Importing libraries
from dotenv import load_dotenv
import os
import operator
import pickle
import sqlite3
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AnyMessage,\
    HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from pydantic import BaseModel
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from IPython.display import Image

##### Setting up environment
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")






























##### Setting up pickle and sqlite helper
#### Saving data
def save_data(db_name, data, id_counter: int):
    pickled_data = pickle.dumps(data)
    with sqlite3.connect(db_name) as conn:
        conn.execute(
            'CREATE TABLE IF NOT EXISTS data (id INTEGER, content BLOB)'
        )
        conn.execute(
            'INSERT INTO data (id, content) VALUES (?,?)',
            (id_counter, sqlite3.Binary(pickled_data))
        )
        conn.commit()
        return id_counter + 1

#### Retrieving data from sqlite
def retrieve_data(db_name, index):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            'SELECT content FROM data WHERE id = ?',
            (index,)
        )
        row = cursor.fetchone()
        if row:
            unpickled_data = pickle.loads(row['content'])
            return unpickled_data
        else:
            print('Error: content not found')
            return

#### Setting global DB name
DB_NAME = 'output.db'




##### Creating models
# base_llm = ChatMistralAI(
#     api_key= mistral_api_key,
#     model_name= 'mistral-small'
# )

fake_llm = None



















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
is to unite previously created drafts of the grant. The \
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
Generate critique and recommendations for the user's submission. \
Provide detailed recommendations, including requests for length, \
depth, style, etc.\
"""
# The current draft submission is: {draft}

INVESTIGATION_PROMPT = """\
You are an experienced mentor in providing support for writing grant \
proposal for non-profit organizations. Your task is to create a simple \
rag prompt that will look into the applicant organizational documents. \
You goals is to retrieve more contextual documents that will help improve \
the current grant draft based on provided techniques.

<Current draft>
{draft}
</Current draft>
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




























##### Creating pydantic model
#### For Planning node
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




































##### Create Agent state
class AgentState(TypedDict):
    # Note: ALL "Annotated" attrs WILL show up in results
        # Even if they're empty, the will be initialized and shown
    # General fields
    msgs: Annotated[List[AnyMessage], operator.add]
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
    draft: str
    critique: str
    rag_context: Annotated[List[str], operator.add]
        # REQUIRES inputs to be in [] bc of "List"
    # random: Annotated[List[int], operator.add]





















##### Sampling and playing with Agent graph and db integrations
    #NOte: both "####" sections work
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

#         graph.add_edge('sample', END)
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

### Execute the graph
# abot = Agent(fake_llm)
# result = abot.graph.invoke({})
# print('psot execution')
# # print(type(result))
# # print(result)
# for k,v in result.items():
#     print(f"Key: {k}")
#     print(f"value: {v}")
#     print('\n'*2)


































##### Create node functionalities
    # Note: these nodes are placed here for ease of access
    # BUT, they will end up being integrated DIRECTLY into the graph
        #Since this will make it easier to pass a single, base LLM to all nodes
#### Temp sample node - to test graph and proper usage
def sample_node_outside(state: AgentState, llm):
    prompt = 'hola!'
    response = llm.invoke(prompt)
    id_counter = state['id_counter']
    print(response)
    print(f'index for sample response is {id_counter}')
    id_counter = save_data(DB_NAME, response, id_counter)
    print(f'new counter: {id_counter}')
    return {'msgs': response, 'id_counter': id_counter}
#### Planner node
def plan_node(state: AgentState, llm):
    prompts = ChatPromptTemplate.from_messages([
        ('system', PLAN_PROMPT),
        ("user", "Write all section outlines for the following theme: {theme}.")
    ]) 

    msgs = prompts.invoke({
        "requirements": state['doner_requirements'],
        "theme": state['theme'],
    })

    model = llm.with_structured_output(SectionOutlines)
    plan = model.invoke(msgs)
    print(f"'Plan' DB data is with index: {state['id_counter']}")
    print(plan)
    id_counter = save_data(DB_NAME, plan, state['id_counter'])
    return {"plan" : plan, 'id_counter' : id_counter}





































