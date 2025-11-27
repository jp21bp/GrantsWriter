# Overview
This project consists of creating an agent that will help write grants.

## Grants Proposal Template
* Source: https://technicalwriterhq.com/writing/grant-writing/grant-writing-templates/
* There are 8 sections:
  1. Cover letter
      * Introduction - who you are, what you do.
      * What you're applying for and why you're qualified to do so
      * Explain purpose of grant proposal
        - How will it benefit the organization?
        - Past work experience and qualifications
  2. Executive summary
      * The problem you're trying to solve and why
      * How this will affect stakeholders
      * Implementation plan
      * Timeline to achieve measurable results
      * Nonprofit's vision and purpose of your project
      * Organization's strengths
      * Problem you're trying to solve
      * Why this particular organization is best for carrying out your idea
      * Timeline and budget of the project
      * Names of any other funding resources
      * Why it's important to take action
      * Organization:
        - First sentence: introducing reason behind grant application
        - Followed by supporting sentences
          * Including SPECIFIC info about what will be accomplished
        - Describes entire project
        - Should be 4-6 paragraphs long
  3. Statement of need
      * Make the reader interested in benefits project will bring
      * Program's outputs should be compelling enough for funding
      * What is the problem in your community that you are passionate about fixing?
        - Answer this in a STRAIGHTFORWARD sentence
      * Provide quantifiables about project output
      * Convince funder that project will help overall community
        - Ex: Give specific numbers about how much waste they'll be able to cut from their budget
      * 1 page or less
      * Explain how project will help community
      * Provide a timeline and ensure project has data points at regular intervals (so progress can be recorded)
        - The MORE detailed the section, the better
      * Make it clear: what needs to change? Why should ppl care?
  4. Goals and objectives
      * Explain the achievable plan of action
        - Outline what you're looking for and how to get there
        - Detail the logic, in a holistic way
      * DON'T make promises you CAN'T KEEP
      * Keep goals short and holistic
      * Stay concise with how much money you're asking for
      * Include collabs with other entities/institutions
  5. Methods and strategies
      * Outlines HOW you'll execute the goals
      * Must be clear, well-organized, and accessible
      * Give brief but detailed answer as to why grant would help the organization/community
        - How will it make a difference for those who are most affect by the issue you're trying to solve
      * Show that there is something wrong
        - Point out statistics, numbers, facts
      * Risk factors: identify potential risks associated with getting grant funding from sources outside grants
      * What will funding from this grant writing accomplish?
        - TAlk about specific impact and how it will change thingss
  6. Plan of evaluation
      * MAke sure that plan is measurable
      Have quantifiable goals and objectives
      * Mention how you're going to measure success for your project
        - How often (monthly, quarterly, yearly)?
        - How much data will be needed before change can be statistically significant?
      * Who needs to sign off on each step of the process/project?
      * Who provides resources (time, money) after approval?
      * Provide a date for evaluation
        - Very important to continuing good relations
  7. Budget information
      * Breakdown how money will be spent, in a timeline
      * How will budget change over time, based on what you anticipate happening with your project?
      * What expenses are variable and which ones are static?
      * What would make this a successful program is the budget is tight?
      * How will budget proposal change based on how well your fundraising efforts go?
      * What are long-term goals for grant funding?
      * Organize your budget from beggining to end
  8. Organizational background
      * Explain your organization in a comprehensive manner
      * Why did organization come into existence in the first place?
      * What does the organization hope to accomplish in the future?
      * Share a brief history of organization, including overcomed obstacles
      * INclude staff members who have contributed significantly
      * Include infor about number of people on full-time, part-time, and volunteer basis


## Agents overview
This section outlines the agents involved in the MAS.

There will be a total of 15 agents created:
* 1 RAG agent
* 1 Planner agent
* 8 agents, 1 for each section of the grant template
* 2 agents to create the first half and second half of the proposal
* 1 agent to combine the created halves
* 1 agent to critique the draft proposal
* 1 agent to do more research based on critiques

The graph outline is slightly as follows:

RAG -> Planner -> (8 section agents) -> (2 half agents) -> 1 uniter agent -> 1 critique agent -> 1 agent to invesitgate critique

There will be a loop between the last 3 agents. Loop will continue for a number of "max_revisions" times.

The agent state will contain the following attributes:
* draft: str
* context: str (will be the context from the first agent RAG)
* message: list[AnyMessage]
* num_revision: int
* max_revision: int
* topic: str
* funder_requirements: str
* first_half_draft: str
* second_half_draft: str

## Thought bubble: Web search vs Web scraper
The RAG agent above will need to search a folder of directories.

This search can be done in 2 ways:
  1. Using an online search tool, such as Tavily
      * Pros:
        - Tavily will be in charge of searching an retrieving the information from the web search
      * Cons:
        - ALL info will be fed into the LLM context, which can be token-consuming
        - The search MUST be done on every new startup of the program, which will take some time in the long run
        - The info won't be stored locally, which means it won't be able to benefit from the embeddings
  2. Using a web scraper, to bring the information into the local machine
      * Pros:
        - Since info will be local, it won't need to run the web search on every run
        - The info can be stored in embedded vector store
        - RAG can easily search the embedding vectore store, which means NOT ALL info will be fed into the LLM
      * Cons:
        - Information will be static, which means new updated info won't be reflected in the RAG agent
        - The info MUST be formatted from HTML into readible text

Thus, the second option will be used in this project, especially since any new documents the organization will provide can easily be infcorporated into the RAG agent.

New documents can be integrated using the same method that was used in the Jopara RAG (~/Documents/Comeplexify/LAngGraph/Course1_6/JoparaRAG).


## Web scraper gameplan

General steps:
  1. Setup a search fcn to retrieve relevant URLs
      * Can be done with any search f'cn, ex: `duckduckgo_search`
      * If the website of the organization is known, then this step can be replaced with HARD coded URLs
  2. Set up scraping fcn to get URL contents
      * This can be done with `bs4.BeautifulSoup`
      * Note, this will return HTML syntax, which is NOT human readible
  3. Cleanup HTML to make it more human readible
      * This will make use of many methods from `BeautifulSoup`
  4. Save the human readible info into a separate folder
      * This will contain all the info needed to do a RAG search of the organization's info
      * After this step, the same steps of `JoparaRAG` can be followed

Note, this web scraper will be SEPARATE from the `main.py` file
 * Since it's function will be a ONE-TIME run, where the info will be stored into the folder
    - Once the info is scraped, the web search WON'T need to be run again
  * Thus the web scraper will be in a pythin file of it's own: `scraper.py`

















