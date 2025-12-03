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
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_cohere import ChatCohere


#### Setting up environment
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")

















#### Setting up model
# llm = ChatCohere(
#     cohere_api_key=cohere_api_key,
#     model='command-r-08-2024',
# )
llm = None

##### Playing with model API integration with pickle
# result = llm.invoke("Hi!")
# print(result)
# with open('output.pkl', 'wb') as file:
#     pickle.dump(result, file)
# with open('output.pkl', 'rb') as file:
#     res = pickle.load(file)
# print(res)
# print(res.content)

























##### Creating system prompts
#### Mini agents
mini_section_prompts = {}   #Used to store prompts in one place
COVER_SECTION = """\
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
</Cover letter components>\
"""
mini_section_prompts['cover_letter'] = COVER_SECTION

EXECUTIVE_SECTION = """\
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
</Executive summary components>\
"""
mini_section_prompts['executive_summary'] = EXECUTIVE_SECTION

NEED_SECTION = """\
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
</Statement of need components>\
"""
mini_section_prompts['statement_of_need'] = NEED_SECTION

GOALS_SECTION = """\
Goals and objectives section, with the following:
<Goals and objectives components>
* Explain the achievable plan of action
    - Outline what you're looking for and how to get there
    - Detail the logic in a holistic way
* Keep the goals short and holistic
    - Stay concise with how much money you're asking
* Include collaborations with other entities and institutions
</Goals and objectives components>\
"""
mini_section_prompts['goals_and_objective'] = GOALS_SECTION

METHODS_SECTION = """\
Methods and strategies section, with the following:
<Methods and strategies components>
* Execution plan and measurable steps
    - Describe clear tasks, timeline, and responsible staff
    - Describe metrics (outputs/outcomes) that show how goals will be achieved and tracked
* Need, evidence, and impact
    - Summarize the problem with key facts or statistics
    - Explain who is harmed and how grant will change outcomes for them
    - State specific short- and long-term impacts the funding will produce
</Methods and strategies components>\
"""
mini_section_prompts['methods_and_strategies'] = METHODS_SECTION

EVALUATION_SECTION = """\
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
</Plan of evaluation components>\
"""
mini_section_prompts['plan_of_evaluation'] = EVALUATION_SECTION

BUDGET_SECTION = """\
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
</Budget information components>\
"""
mini_section_prompts['budget_information'] = BUDGET_SECTION

BACKGROUND_SECTION = """\
Organizational background section, with the following:
<Organizational background components>
* Explain your organization in a comprehensive manner
    - Why did the organization come into existence?
    - What does the organization hope to accomplish in the future?
* Share a brief history of the organization
    - Include overcomed obstacles
    - Include staff members who have contributed significantly
</Organizational background components>\
"""
mini_section_prompts['organizational_background'] = BACKGROUND_SECTION

# for prompt in mini_section_prompts:
#     print(prompt)
#     print('\n'*2)




#### Mini summarizer agents
summarizer_section_prompts = {}
SECTIONS_ONE = "Cover letter, Executive summary, Statement of Need, \
Goals and Objectives"
summarizer_section_prompts['first_half'] = SECTIONS_ONE

SECTIONS_TWO = "Methods and strategies, Plan of evaluation, \
Budget information, Organizational background"
summarizer_section_prompts['second_half'] = SECTIONS_TWO

























##### Configuring general system prompt
#### For Mini agents
GENERAL_MINI_PROMPTS = """\
You are a senior grant writing expert for non-profit organizations. \
You're role in the grant's writing process will focus on {mini_section}.
The organization LAFF is applying for the grant in order to support \
a community project focused on {theme}. The grant donaters have the \
following requirements for their grant: {requirements}. Your task is \
to write your section of the grant by using the following plan:

<Section plan>
{plan}
</Section plan>\
"""

#### For Summarizer agents
GENERAL_SUMMARIZER_PROMPT = """\
You are a senior grant writing expert for non-profit organizations. \
Your task is to unite four different grant sections, which were previously \
created, in a concise and coherent style. The four sections are: \
{summarizer_sections}. The work done in each of these sections is as follows: \

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

Unite these four sections to create a draft of half of the first \
part of the application. Do not write the whole aplication. Only \
use the info provided above. The theme of the aplication is {theme}. \
The grant doners have the following requirements: {requirements}. \
"""






















##### Playing with prompt formatting
#### Regular substitution with ".format"
general_prompt = GENERAL_MINI_PROMPTS.format(
    mini_section = 'ONE',
    theme = 'TWO',
    requirements = 'THREE',
    plan = 'FOUR',
)
# print(general_prompt)

####REg susbtitution with '.format' and dictionary
replacements = {
    'mini_section': 'UNO',
    'theme': "DOS",
    'requirements': 'TRES',
    'plan': 'CUATRO',
}
gen_prompt = GENERAL_MINI_PROMPTS.format(**replacements)
# print(gen_prompt)


#### Trying to replace some placeholders and leave others untouchec
    # Doesn't work, requires a custom function
# print(GENERAL_MINI_PROMPTS)
# mini_main_prompts = []
# for prompt in mini_section_prompts:
#     formatted = GENERAL_MINI_PROMPTS.format(
#         mini_section = prompt,
#         theme = 'Educational projects',
#         requirements = 'None',
#         # plan = 'FOUR',
#     )
#     mini_main_prompts.append(formatted)

# for prompt in mini_main_prompts:
#     print(prompt)
#     print('\n' * 2)


#### Creating custom function
    #Used to replace some placeholders and leave others untouched
class FormatDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

### Using custom function
template = "Hello {name}, today is {day}. Your score is {score}."
data = FormatDict(name="Alice", day="Monday")
result = template.format_map(data)
# print(result)    

### Replacing untouched placeholder in another run
    # Outcome: it works
new_result = result.format(score="ten")
# print(new_result)
















##### Replaceing general prompt placeholders
#### Using custom fcn to replace section prompts
mini_main_prompts = []
for prompt in mini_section_prompts:
    formats = FormatDict(
        mini_section = prompt,
        theme = 'Educational projects',
        requirements = 'None',
        # plan = 'FOUR',
    )
    formatted = GENERAL_MINI_PROMPTS.format_map(formats)
    mini_main_prompts.append(formatted)

# for prompt in mini_main_prompts:
#     print(prompt)
#     print('\n'*2)


#### Using custom fcn to replace summarizer prompts
summarizer_main_prompts = []
for prompt in summarizer_section_prompts:
    formats = FormatDict(
        theme = 'Educational projects',
        requirements = 'None',
        summarizer_sections = prompt
    )
    formatted = GENERAL_SUMMARIZER_PROMPT.format_map(formats)
    summarizer_main_prompts.append(formatted)

# for prompt in summarizer_main_prompts:
#     print(prompt)
#     print('\n'*2)















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





















##### Creating Agent Class
#### USing (role, content) tuples
class MiniAgent:
    def __init__(self, system_prompt: str = '', replacements: dict = {}):
        self.system = system_prompt.format(**replacements)
        # print(f'BEFORE:\n{system_prompt}\n\nAFTER:\n{self.system}\n' + '=' * 70)
        self.messages = []
        if self.system:
            self.messages.append({
                "role": "system",
                "content": self.system,
            })
    def __call__(self):    #def __call__(self, message):
        self.messages.append({
            "role": "user",
            "content": 'Execute your task.',
        })
        result = self.execute()
        self.messages.append({
            "role": "assistant",
            "content": result,
        })
        return result
    def execute(self):
        completion = llm.invoke(self.messages)
        return completion

#### USing "Message" types
    # This is better, since LG intenrally does the conversion ANYWAYS
class MiniAgent:
    def __init__(self, system_prompt: str = '', replacements: dict = {}):
        self.system = system_prompt.format(**replacements)
        # print(f'BEFORE:\n{system_prompt}\n\nAFTER:\n{self.system}\n' + '=' * 70)
        self.messages = []
        if self.system:
            self.messages.append(
                SystemMessage(content=self.system)
            )
    def __call__(self):    #def __call__(self, message):
        self.messages.append(
            HumanMessage(content="Execute your task.")
        )
        result = self.execute() #Will be an "AIMessage" type
        self.messages.append(result)
        return result
    def execute(self):
        completion = llm.invoke(self.messages)
        return completion





##### Creating class for system prompts
class SystemPrompts:
    # I need to find a way to gather ALL agents into one class
        # mini and sumamriezers
    # BUT I also need to find a way to leave them SEMI-UNINITIALIZED
        #So that I can integrate the main agent's plan into the mini agents
            #I.e., replace the missing placeholders
    # def __init__(self, section_plan_list):
        #I dont think i need a custom init
    
    def create_prompts(self) -> dict:
        syst_prompts = {}
        for section, prompt in mini_section_prompts.items():
            formats = FormatDict(
                mini_section = prompt,
                # theme = 'Educational projects',
                # requirements = 'None',
                # plan = 'FOUR',
            )
            formatted = GENERAL_MINI_PROMPTS.format_map(formats)
            syst_prompts[section] = formatted
        for half, prompt in summarizer_section_prompts.items():
            formats = FormatDict(
                # theme = 'Educational projects',
                # requirements = 'None',
                summarizer_sections = prompt
            )
            formatted = GENERAL_SUMMARIZER_PROMPT.format_map(formats)
            syst_prompts[half] = formatted
            # print(f'prompt for {half}:\n{syst_prompts[half]}' + '\n' * 3)
        return syst_prompts

# sys_prompts = SystemPrompts().create_prompts()
# for k,v in sys_prompts.items():
#     print(k)
#     print(v)
#     print('\n'*2)

























































