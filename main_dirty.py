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
from langchain_google_genai import ChatGoogleGenerativeAI
# from rag_clean import RAG
from mini_agents_dirty import MiniAgent, SystemPrompts

##### Setting up environment
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")






























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




##### Intialize agent components
#### Model
# llm = ChatMistralAI(
#     api_key= mistral_api_key,
#     model_name= 'mistral-small'
# )

# llm = ChatGoogleGenerativeAI(
#     api_key=google_api_key,
#     model="gemini-2.0-flash-lite",
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
    first_half: str     #?
    second_half: str    #?
    draft: str
    critique: str
    rag_context: Annotated[List[str], operator.add]
        # REQUIRES inputs to be in [] bc of "List"
    # random: Annotated[List[int], operator.add]


#### Create graph
class Agent:    #GrantsAgent
    def __init__(self, llm, rag, mini_sys_prompts: dict):
        graph = StateGraph(AgentState)
        ## Creating nodes
        graph.add_node('rag', self.rag_node)
        graph.add_node('planner', self.plan_node)
        graph.add_node('cover_sec', self.cover_node)
        graph.add_node('executive_sec', self.executive_node)

        graph.set_entry_point('rag')
        graph.add_edge('rag', 'planner')
        graph.add_edge('planner', 'cover_sec')
        graph.add_edge('planner', 'executive_sec')
        graph.add_edge('cover_sec', END)
        graph.add_edge('executive_sec', END)


        self.graph = graph.compile(
            # checkpointer= memory,   #FOr short-term memory
            # store= store,   # For long-term memory
        )
        self.llm = llm
        self.rag = rag
        self.mini_sys_prompts = mini_sys_prompts
        # print(self.mini_sys_prompts)

    # def rag_node(self, state: AgentState):    #Original
    #     user_query = state['msgs'][0]
    #     id_counter = state['id_counter']
    #     rag_result = self.rag.invoke(user_query)
    #     print(f"'rag' db index at index: {id_counter}")
    #     print(rag_result)
    #     id_counter = save_data(DB_NAME, rag_result, id_counter)
    #     return {"rag_context": [rag_result], "id_counter": id_counter}

    def rag_node(self, state:AgentState):
        # print('ONE')
        # USing retrieve from db, to avoid api usage
        data = retrieve_data(DB_NAME, 1)
        # print(type(data))
        # print(data)
        # return {'msgs': [data]}
        # print(state)
        return {'rag_context': [data]}
#     def plan_node(self, state: AgentState):   #Original
#         USER_PROMPT = \
# """\
# Write all section outlines for the following theme: {theme}. \
# The organizational context regarding this proposal and theme is:
# <Organizational Context>
# {context}
# </Organizational Context>\
# # """
# #         print(USER_PROMPT)
# #         return
#         prompts = ChatPromptTemplate.from_messages([
#             ('system', PLAN_PROMPT),
#             ("user", USER_PROMPT)
#         ]) 

#         msgs = prompts.invoke({
#             "requirements": state['doner_requirements'],
#             "theme": state['theme'],
#             "context": state['rag_context']
#         })
#         # print(msgs)
#         # return

#         model = self.llm.with_structured_output(SectionOutlines)
#         plan = model.invoke(msgs)
#         print(f"'Plan' DB data is with index: {state['id_counter']}")
#         print(plan)
#         id_counter = save_data(DB_NAME, plan, 2)
#         # id_counter = save_data(DB_NAME, plan, state['id_counter'])
#         return {"plan" : plan, 'id_counter' : id_counter}

    def plan_node(self, state:AgentState):
        # print(state['rag_context'])
        # print('TWO')
        data = retrieve_data(DB_NAME, 2)
        # print(type(data))
        # print(data.cover_letter)
        # print(data.organizational_background)
        # print(type(data).model_fields.items())
        # print(dir(data))
        # print(data.__getattribute__('cover_letter'))
        overview = type(data).model_fields
            # This is a dictionary
            # Syntax: {key = fieldName, value = fieldRequirements}
        # print(items)
        details = data.model_dump()
            #This is also dictionary
            # Syntax: {key = fieldName, vluew = attribute values}
        # print(details)
        # for k,v in details.items():
        #     print(k)
        #     print(v)
        #     print('\n'*2)
        return {'plan': data}

    def cover_node(self, state: AgentState):
        key = "cover_letter"
        replacements = {
            'plan': state['plan'].__getattribute__(key),
            'theme': state['theme'],
            'requirements': state['doner_requirements'],
        }
        sys_prompt = self.mini_sys_prompts[key]
        agent = MiniAgent(sys_prompt, replacements)
        #TODO: execute agent
        return

    def executive_node(self, state: AgentState):
        key = 'executive_summary'
        replacements = {
            'plan': state['plan'].__getattribute__(key),
            'theme': state['theme'],
            'requirements': state['doner_requirements'],
        }
        sys_prompt = self.mini_sys_prompts[key]
        agent = MiniAgent(sys_prompt, replacements)
        #Todo: execute agent
        return




#### Initialize agent and visualize
sys_prompts_mini = SystemPrompts().create_prompts()
# agent = Agent(fake_llm, base_rag)
# agent = Agent(base_llm, base_rag)
# agent = Agent(base_llm, fake_rag)
agent = Agent(fake_llm, fake_rag, sys_prompts_mini)
# print(agent.graph.get_graph().draw_ascii())

start_state = {
    'theme': 'educational projects',
    'doner_requirements': 'none',
}
result = agent.graph.invoke(start_state)
# for k,v in result.items():
#     print(k)
#     print(v)
#     print('\n'*2)

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
# }
# result = agent.graph.invoke(starting_state)
#     # WORKS! Accepts inputs, tranlsates to user qury, adn returns rag output
















































