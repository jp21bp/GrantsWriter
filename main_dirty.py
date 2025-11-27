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
import operator
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AnyMessage,\
    HumanMessage, AIMessage, ToolMessage





##### Creating agent prompts










