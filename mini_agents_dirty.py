###### Mini Agents file
    # This file consists of the 8 + 2 agents needed to create a draft
    # The 8 mini agents correspond to the components of a grant
    # The 2 mini agents will unify each half
    # The draft itself will be created in another file

###### Note: Using pickle library with LG
##### General syntax
    # result = llm.invoke("Hi!")
    # print(result)
    # with open('output.pkl', 'wb') as file:
    #     pickle.dump(result, file)
    # with open('output.pkl', 'rb') as file:
    #     res = pickle.load(file)
    # print(res)


##### General setup
#### Importing libraries
import os
import pickle
from dotenv import load_dotenv
from langchain_cohere import ChatCohere


#### Setting up environment
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

#### Setting up model
# llm = ChatCohere(
#     cohere_api_key=cohere_api_key,
#     model='command-r-08-2024',
# )

# result = llm.invoke("Hi!")

# print(result)

# with open('output.pkl', 'wb') as file:
#     pickle.dump(result, file)

with open('output.pkl', 'rb') as file:
    res = pickle.load(file)

# print(res)

# print(res.content)



##### Creating Agent Class
class Agent:
    def __init__(self, system=''):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({
                "role": "system",
                "content": system,
            })
    def __call__(self, message):
        self.messages.append({
            "role": "user",
            "content": message,
        })
        result = self.execute()
        self.messages.append({
            "role": "assistant",
            "content": result,
        })
        return result
    def execute(self):
        completion = llm.invoke(self.messages)
        return completion.content





##### Creating system prompts
#### Mini agents
COVER_SECTION = """
    Cover letter section, with the following:
    <Cover letter components>
    * Introduction 
        - Who is the organization?
        - What does the organization do?
    * Connection to grant 
        - What you're applying for
        - Why you're qualified to do so.
    * Purpose of the grant proposal
        - How will it benefit the organization?
        - Past work experience and qualifications?
    </Cover letter components>
"""

EXECUTIVE_SECTION = """
    Executive summary section, with the following:
    <Executive summary components>
    * Project summary, problem, and purpose
        - A clear statement of the problem
        - Why it matters to solve the problem
        - The nonprofit's vision
        - The specific outcomes to be delievered
    * Impact and Rationale
        - Who benefits from the project?
        - How will stakeholders be affected?
        - Why is immediate action needed?
        - Why is this organization uniquely qualified?
    * Plan, timeline, and resources
        - High-level implementation steps
        - Measurable timeline for results
        - Top-line budget
        - Key organizational strengths for execution
    </Executive summary components>
"""

NEED_SECTION = """
    Statement of need section, with the following:
    <Statement of need components>
    * Define the problem and why it matters
        - State the community issue in one sentence
        - Explain what needs to change
        - Highlight why people should care
    * Show impact with evidence
        - Present compelling, quanitifiable outputs (numbers, data, measurable benefits)
        - These quantifiables should show how the project will improve the community
        - Justify funding
    * Outline a clear, concise plan
        - Keep it to one page
        - Explain benefits
        - Provide a timeline with regular data points
        - Make the case that the project delivers lasting value
    </Statement of need components>
"""

GOALS_SECTION = """
    Goals and objectives section, with the following:
    <Goals and objectives components>
    * Explain the achievable plan of action
        - Outline what you're looking for and how to get there
        - Detail the logic in a holistic way
    * Keep the goals short and holistic
        - Stay concise with how much money you're asking
    * Include collaborations with other entities and institutions
    </Goals and objectives components>
"""

METHODS_SECTION = """
    Methods and strategies section, with the following:
    <Methods and strategies components>
    * Execution plan and measurable steps
        - Describe clear tasks, timeline, and responsible staff
        - Describe metrics (outputs/outcomes) that show how goals will be achieved and tracked
    * Need, evidence, and impact
        - Summarize the problem with key facts or statistics
        - Explain who is harmed and how grant will change outcomes for them
        - State specific short- and long-term impacts the funding will produce
    </Methods and strategies components>
"""

EVALUATION_SECTION = """
    Plan of evaluation section, with the following:
    <Plan of evaluation components>
    * Measurable plan
        - Define quantifiable goals and objectives
        - Ensure they have clear success metrics
        - Define the measurement method
    * Monitoring and timing
        - State measurement frecuency (monthly/quarterly/yearly)
        - State the required sample/data size for statistical significance
        - State the specific evaluation date
    * Governance and resourcs:
        - List who must sign off at each step
        - List who provides time/money after approval 
    </Plan of evaluation components>
"""

BUDGET_SECTION = """
    Budget information section, with the following:
    <Budget information components>
    * Phased spending timeline
        - Allocate funds by project stage (startup, implementation, scale, closeout)
        - Include dates/milestones and contingency reserves
        - List static (salaries, rent, subscriptions) vs variable (material, travel, outreach) costs per phase
    * Adaptive forecasting and fundraising impact
        - Model budget scnarios (best, expected, worst)
        - Show how priorities shift if fundraising is over- or under-performing
        - Specify automatic triggers for scaling activies
    * Success criteria and long-term funding
        - Define tight budget success metrics (core outputs, cost-per-outcome, minimum viable staffing)
        - Map rant-seeking goals (short-term brdige grants, multi-year sustainability grants)
        - State end-to-end budget organized from launch to closeout
    </Budget information components>
"""

BACKGROUND_SECTION = """
    Organizational background section, with the following:
    <Organizational background components>
    * Explain your organization in a comprehensive manner
        - Why did the organization come into existence?
        - What does the organization hope to accomplish in the future?
    * Share a brief history of the organization
        - Include overcomed obstacles
        - Include staff members who have contributed significantly
    </Organizational background components> 
"""



#### Mini summarizer agents
SECTIONS_ONE = "Cover letter, Executive summary, Statement of Need,\
    Goals and Objectives"

SECTIONS_TWO = "Methods and strategies, Plan of evaluation, \
    Budget information, Organizational background"











##### Configuring general system prompt
#### For Mini agents
GENERAL_MINI_PROMPTS = """
    You are a senior grant writing expert for non-profit organizations.
    YOu're role in the grant's writing process will focus on {mini_section}.
    The organization LAFF is applying for the grant in order to support
    a community project focused on {theme}. The grant donaters have the 
    following requirements for their grant: {requirements}. Your task is 
    to write you're section of the grant by using the following plan:

    <Section plan>
    {plan}
    </Section plan>
"""




#### For Summarizer agents
GENERAL_SUMMARIZER_PROMPT = """
    You are a senior grant writing expert for non-profit organizations.
    Your role is to unite four different grant sections, which were previously
    created, in a concise and coherent style. The four sections are:
    {summarizer_sections}. The work done in each of these sections is as follows:

    <Section one>
    {section_one}
    </Section one>
    
    <Section two>
    {section_two}
    </Section two>

    <Section three>
    {section_three}
    </Section three>

    <Section four>
    {section_four}
    </Section four>

    Unite these four sections to create a draft of half of the first
    part of the application. Do not write the whole aplication. Only
    use the info provided above. The theme of the aplication is {theme}.
    The grant donaters have the following requirements: {requirements}.
"""



##### Creating agents
#### Gathering their names into a list
sections_names = []
sections_names.append('cover')
sections_names.append('executive')
sections_names.append('need')
sections_names.append('goals')
sections_names.append('methods')
sections_names.append('evaluation')
sections_names.append('budget')
sections_names.append('background')


agent_names = []
for i, name in enumerate(sections_names):
    exec(f"agent_names.append('{name}_agent')")
    # print(samples[i])
    # exec(f"{name}_agent = {i}; sample[{i}] = {name}_agent")














