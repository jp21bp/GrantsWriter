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
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AnyMessage,\
    HumanMessage, AIMessage, ToolMessage, SystemMessage
from pydantic import BaseModel
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI

##### Setting up environment
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")



##### Creating models
# llm = ChatMistralAI(
#     api_key= mistral_api_key,
#     model_name= 'mistral-small'
# )

# result = llm.invoke('hi')
# print(result)
# with open('output.pkl', 'wb') as file:
#     pickle.dump(result, file)
# print('success')





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
    # General fields
    theme: str
    doner_requirements: str
    num_revisions: int
    max_revisions: int
    # Node related fields
    plan: SectionOutlines
    draft: str
    critique: str
    rag_context: Annotated[List[str], operator.add]


##### Testing out diff. langchain "Messages"
# for attr in dir(SystemMessage):
#     if attr.startswith("_"): continue
#     print(attr)
#     try: print(SystemMessage.__getattribute__(attr))
#     except: continue
#     print('\n'*2)





# prompt = ChatPromptTemplate.from_messages([
#     ("system", PLAN_PROMPT),
#     ("user", "Write the section outline for the following theme: {theme}.")
# ])

# print(prompt.invoke({'theme': 'UNO', 'requirements': 'DOS'}))



# prompts = ChatPromptTemplate.from_messages([
#     ('system', PLAN_PROMPT),
#     ("user", "Write all section outlines for the following theme: {theme}.")
# ])

# msgs = prompts.invoke({
#     "requirements": 'UNO',
#     "theme": 'DOS',
# })

# print(msgs)


##### Create node functionalities
def plan_node(state: AgentState):
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
    print(plan)
    return {"plan" : plan}


##### Create Agent graph



























