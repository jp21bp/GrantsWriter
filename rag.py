###### RAG agent
    # Will be used on organization content blob found on main webpage
    # Recall: blob is in one big text file
        # Thus, we'll need a diff strat than Jopara RAG
            # Specifically, we won't need "document_loaders"
        # We'll simply open the file
        # Rest is similar to JoparaRAG
    # There is English and Spanish info, so we'll need Bilingual embed
        # Thus we'll also need an english and spanish chain similar to JoparaRAG
        # BUT, the info WON'T need to be returned in Spanish
            # ASSUMING the grants will be written in English
        # Thus, the spanish chain will be in charge of:
            # Translating initial english query into spanish
            # Finding the spanish related info
            # Turning the retrieved spanish info into enlgish
            # Return the english-translated info to user

##### General setup
#### Importing libraries
### General libraries
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableMap
from langchain_core.output_parsers.string import StrOutputParser
### Model libraries
from langchain_community.embeddings import JinaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
### Embedding libraries
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

#### Setting up environment
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
jina_api_key = os.getenv("JINA_API_KEY")

#### Setting up models
# ### LLM model
#     # Web: https://aistudio.google.com/welcome
# llm = ChatGoogleGenerativeAI(
#     api_key=google_api_key,
#     model="gemini-2.0-flash",
#     # max_tokens=128
# )
### Embedding model
    # Web: https://jina.ai/
embedding_model = JinaEmbeddings(
    api_token=jina_api_key,
    model="jina-embeddings-v2-base-es"
)




##### File Embeddings
    # Note: we'll store all the embeddings in the same file
        # I.e., all diff. docs will be embedded into the same vstore
    # Thus, when loading the docs, we'll use "list.extend" over "list.append"
        # [1,2,3].append([4,5]) = [1,2,3,[4,5]]
        # [1,2,3].extend([4,5]) = [1,2,3,4,5]
#### Loading text file(s)
docs_path = "/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents"

def load_files(docs_path: str) -> list:
    loaded_docs = []
        # Since docs aren't that big, each doc will have its own space
            # I.e., 4 text files => "len(docs)" = 4
    for file in os.listdir(docs_path):
        if not file.endswith(".txt"): continue
            # Skips all non-text files
        file_path = os.path.join(docs_path, file)
        loader = TextLoader(file_path)
        loaded_docs.extend(loader.load())
    return loaded_docs
    
#### Split text into chunks
def split_docs(loaded_docs: list) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1105, chunk_overlap = 0,
    )
        #IMPORTANT NOTE:
            #1105 is needed to make "Chroma.from_docs()" line 99 work
                #Specifically, Jina embed model can only handle 512 chunked docs
            #I.e., if we use a smaller size, then len(split_docs) > 512
    chunked_docs = text_splitter.split_documents(loaded_docs)
    return chunked_docs


## Checking the size of the chunked docs for Jina embed
# sample = split_docs(load_files(docs_path))
# print(len(sample))

#### Creating vector store
directory = "IndexStore"
directory = os.path.join(docs_path, directory)
if not os.path.isdir(directory):
    # Create dir if not existant
    os.mkdir(directory)
if not os.listdir(directory): # Checks is dir is empty or not
    # This path is that dir is empty
    loaded_docs = load_files(docs_path)
        #Load the docs
    chunked_docs = split_docs(loaded_docs)
        #Split the docs
    vstore = Chroma.from_documents(
        chunked_docs, embedding_model,
        persist_directory=directory
    )
        # Store indexes in disk
else: 
    # This path means dir is not empty
    vstore = Chroma(
        persist_directory=directory, 
        embedding_function=embedding_model
    )
        # Load indexes from non-empty dir

#### Setting up retriever
retriever = vstore.as_retriever(
    search_type="similarity",
        #Literal["similarity", "mmr", "similarity_score_threshold"]
    search_kwargs={"k": 3}
        #Number of chunked documents to return
)

#### Testing retriever
# query = "What are current educational projects?"
# print(retriever.invoke(query))
# Output:
    # [Document(id='18f02617-dd7f-4110-9825-4357ed892655', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='Quality Education\tOur quality education programme focuses on giving the beneficiaries at our partner organisations access to formal education and encouraging their personal and professional development.\tOur goals are to:\tEnsure that orphaned and vulnerable children and young people in Peru have access to formal learning environments and additional support that fosters and develops their cognitive abilities and technical skills. We provide educational scholarship funding, improve the quality of tutoring by providing professional development support, and more!\th\tWork with our local partner organisations to identify and meet the basic physical, emotional, and social needs of their beneficiaries, equipping them with essential tools for life. We provide projects including (but are not limited to) facilitating financial education workshops and providing funding for dentist visits.\tClick on the buttons below to see how LAFF’s Quality Education programme helps our partner organisations.\tMosqoy\tSacred Valley Project\tCasa Mantay\tPersonal Development Workshops\tFor many years now, LAFF has been'),
    # Document(id='cc8c364c-ee4e-4dcf-a708-6ae41492c3f3', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='Home\nWe help children and young people in Peru build a better future\tWe are a UK registered charity, working with partner organisations in Peru to help disadvantaged children and young people build a better future.\tPROGRAMMES\tWe deliver our work through long-term partnerships  with local organisations in Peru\tThrough our partnership model, we support and invest in social enterprises to help build partner sustainability\tGet Involved\tDONATE\tSPONSOR THE EDUCATION OF A CHILD\tVOLUNTEER\tGET INVOLVED\tLatest news\n==============================\nProgrammes \nProgrammes\tOur programmes have been carefully designed and implemented in order to maximise the capacity of the staff in our partner organisations, increase sustainability and boost academic development. We regularly review our programmes to make sure they are working effectively and garnering desirable results. Our current programmes are outlined below:\tQuality Education\tCapacity Building\tMost of the questions were team oriented they really focused on how I worked in teams\tfrom the source\tand paper writer the results of those situations.'),
    # Document(id='641ddd1e-2ecb-4440-a406-894033163c60', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/mosqoy_contents.txt'}, page_content='community-led\xa0socioeconomic development projects. We have\xa0supported over 200 weavers in 11 communities.\t2.\tMosqoy Field School\tis our social enterprise that offers culturally responsible tours and field courses in Peru.\xa0In addition, we offer culturally and environmentally responsible tours to the general public, working with our partnering weaving communities and youth program graduates.\tWe work with youth from Canada and other countries in the Global North to educate about how to be more responsible travellers and consumers, both in their home countries and around the world. This program provides\xa0opportunities for youth to connect with and learn about\xa0issues facing communities in other parts of the world\xa0so that they can begin to change their habits of consumption and interaction.\tThrough this\xa0program, we have worked with over 6000 youth in the Global North.\t\u200b\t3.\tThe profits from both of these social enterprises funds the\tMosqoy Youth Program\t, which supports promising yet marginalized youth from remote communities in the region by providing post-secondary educational scholarships. This'),
    # Document(id='711cde9b-5dd7-4307-9e97-349819edbc06', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='offering its beneficiaries workshops on a variety of topics that contribute to a young person’s development.\tSome of the topics we’ve covered are:\tComprehensive Sex Education\tCV Writing\tVocational Guidance\tFinancial Literacy\tProblem Solving\tLeadership\tPartners and collaborators in our Quality Education programme:'),
    # Document(id='28377fcd-a68f-4d63-a732-864fd0f7cbb2', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/sacredvalleyproject_contents.txt'}, page_content='full potential. SVP aims to achieve this vision by supporting rural, indigenous Peruvian girls in their educational goals.\tView Our 2024 Annual Report Here\tWhy Girls?\tGirls’ education strengthens economies and creates jobs. Millions of educated girls, means more working women with the potential to add up to $12 trillion USD to global growth.  -Malala Fund\tEducated women invest 90% of their earnings back into their families.  -Clinton Global Initiative\t420 million people would be lifted out of poverty by achieving a secondary education. This would cut the number of people living in poverty by more than half.  -UNESCO\tCommunities are more stable — and can recover faster after conflict — when girls are educated. When a country gives all its children secondary education, they cut their risk of war in half. Education is vital for security around the world because extremism grows alongside inequality.   -Malala Fund\tEducated girls are healthier citizens who raise healthier families. The World Bank reports that universal secondary education for girls could virtually eliminate child marriage.')]
# Output returns 5 chunked docs
    # Since we put "search_kwargs={'k': 3}"







##### Creating first chain - detecting language
#### Setup prompt

#### Setup pydantic model

#### Setup llm model





##### Creating second chain - spanish processing
#### Create RunnableMAP

#### Create prompt

#### Create model

#### Create output parser




##### Creating third chain - english processing
#### Create RunnableMAP

#### Create prompt

#### Create model

#### Create output parser






##### Setup conditional router
#### Spanish path

#### English path

#### Neither






##### Main pipeline
#### Putting it all together












