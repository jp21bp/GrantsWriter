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




###### Old dirty
##### General setup
#### Importing libraries
# ### General libraries
# from dotenv import load_dotenv
# import os
# from pydantic import BaseModel, Field
# from langchain_core.prompts.chat import ChatPromptTemplate
# from langchain_core.runnables.base import RunnableLambda
# from langchain_core.output_parsers.string import StrOutputParser
# ### Model libraries
# from langchain_community.embeddings import JinaEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# ### Embedding libraries
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from utilities_clean import *


# #### Setting up environment
# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
# jina_api_key = os.getenv("JINA_API_KEY")

# #### Setting up models
# ### LLM model
#     # Web: https://aistudio.google.com/welcome
# llm = ChatGoogleGenerativeAI(
#     api_key=google_api_key,
#     model="gemini-2.0-flash",
#     # max_tokens=128
# )
# ### Embedding model
#     # Web: https://jina.ai/
# embedding_model = JinaEmbeddings(
#     api_token=jina_api_key,
#     model="jina-embeddings-v2-base-es"
# )









# ##### File Embeddings
#     # Note: we'll store all the embeddings in the same file
#         # I.e., all diff. docs will be embedded into the same vstore
#     # Thus, when loading the docs, we'll use "list.extend" over "list.append"
#         # [1,2,3].append([4,5]) = [1,2,3,[4,5]]
#         # [1,2,3].extend([4,5]) = [1,2,3,4,5]
# #### Loading text file(s)
# docs_path = "/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents"

# def load_files(docs_path: str) -> list:
#     loaded_docs = []
#         # Since docs aren't that big, each doc will have its own space
#             # I.e., 4 text files => "len(docs)" = 4
#     for file in os.listdir(docs_path):
#         if not file.endswith(".txt"): continue
#             # Skips all non-text files
#         file_path = os.path.join(docs_path, file)
#         loader = TextLoader(file_path)
#         loaded_docs.extend(loader.load())
#     return loaded_docs
    
# #### Split text into chunks
# def split_docs(loaded_docs: list) -> list:
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size = 1105, chunk_overlap = 0,
#     )
#         #IMPORTANT NOTE:
#             #1105 is needed to make "Chroma.from_docs()" line 99 work
#                 #Specifically, Jina embed model can only handle 512 chunked docs
#             #I.e., if we use a smaller size, then len(split_docs) > 512
#     chunked_docs = text_splitter.split_documents(loaded_docs)
#     return chunked_docs


# ## Checking the size of the chunked docs for Jina embed
# # sample = split_docs(load_files(docs_path))
# # print(len(sample))

# #### Creating vector store
# directory = "IndexStore"
# directory = os.path.join(docs_path, directory)
# if not os.path.isdir(directory):
#     # Create dir if not existant
#     os.mkdir(directory)
# if not os.listdir(directory): # Checks is dir is empty or not
#     # This path is that dir is empty
#     loaded_docs = load_files(docs_path)
#         #Load the docs
#     chunked_docs = split_docs(loaded_docs)
#         #Split the docs
#     vstore = Chroma.from_documents(
#         chunked_docs, embedding_model,
#         persist_directory=directory
#     )
#         # Store indexes in disk
# else: 
#     # This path means dir is not empty
#     vstore = Chroma(
#         persist_directory=directory, 
#         embedding_function=embedding_model
#     )
#         # Load indexes from non-empty dir

# #### Setting up retriever
# retriever = vstore.as_retriever(
#     search_type="similarity",
#         #Literal["similarity", "mmr", "similarity_score_threshold"]
#     search_kwargs={"k": 2}
#         #Number of chunked documents to return
# )

# #### Testing retriever
# # query = "What are current educational projects?"
# # print(retriever.invoke(query))
# # Output:
#     # [Document(id='18f02617-dd7f-4110-9825-4357ed892655', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='Quality Education\tOur quality education programme focuses on giving the beneficiaries at our partner organisations access to formal education and encouraging their personal and professional development.\tOur goals are to:\tEnsure that orphaned and vulnerable children and young people in Peru have access to formal learning environments and additional support that fosters and develops their cognitive abilities and technical skills. We provide educational scholarship funding, improve the quality of tutoring by providing professional development support, and more!\th\tWork with our local partner organisations to identify and meet the basic physical, emotional, and social needs of their beneficiaries, equipping them with essential tools for life. We provide projects including (but are not limited to) facilitating financial education workshops and providing funding for dentist visits.\tClick on the buttons below to see how LAFF’s Quality Education programme helps our partner organisations.\tMosqoy\tSacred Valley Project\tCasa Mantay\tPersonal Development Workshops\tFor many years now, LAFF has been'),
#     # Document(id='cc8c364c-ee4e-4dcf-a708-6ae41492c3f3', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='Home\nWe help children and young people in Peru build a better future\tWe are a UK registered charity, working with partner organisations in Peru to help disadvantaged children and young people build a better future.\tPROGRAMMES\tWe deliver our work through long-term partnerships  with local organisations in Peru\tThrough our partnership model, we support and invest in social enterprises to help build partner sustainability\tGet Involved\tDONATE\tSPONSOR THE EDUCATION OF A CHILD\tVOLUNTEER\tGET INVOLVED\tLatest news\n==============================\nProgrammes \nProgrammes\tOur programmes have been carefully designed and implemented in order to maximise the capacity of the staff in our partner organisations, increase sustainability and boost academic development. We regularly review our programmes to make sure they are working effectively and garnering desirable results. Our current programmes are outlined below:\tQuality Education\tCapacity Building\tMost of the questions were team oriented they really focused on how I worked in teams\tfrom the source\tand paper writer the results of those situations.'),
#     # Document(id='641ddd1e-2ecb-4440-a406-894033163c60', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/mosqoy_contents.txt'}, page_content='community-led\xa0socioeconomic development projects. We have\xa0supported over 200 weavers in 11 communities.\t2.\tMosqoy Field School\tis our social enterprise that offers culturally responsible tours and field courses in Peru.\xa0In addition, we offer culturally and environmentally responsible tours to the general public, working with our partnering weaving communities and youth program graduates.\tWe work with youth from Canada and other countries in the Global North to educate about how to be more responsible travellers and consumers, both in their home countries and around the world. This program provides\xa0opportunities for youth to connect with and learn about\xa0issues facing communities in other parts of the world\xa0so that they can begin to change their habits of consumption and interaction.\tThrough this\xa0program, we have worked with over 6000 youth in the Global North.\t\u200b\t3.\tThe profits from both of these social enterprises funds the\tMosqoy Youth Program\t, which supports promising yet marginalized youth from remote communities in the region by providing post-secondary educational scholarships. This'),
#     # Document(id='711cde9b-5dd7-4307-9e97-349819edbc06', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/laffcharity_contents.txt'}, page_content='offering its beneficiaries workshops on a variety of topics that contribute to a young person’s development.\tSome of the topics we’ve covered are:\tComprehensive Sex Education\tCV Writing\tVocational Guidance\tFinancial Literacy\tProblem Solving\tLeadership\tPartners and collaborators in our Quality Education programme:'),
#     # Document(id='28377fcd-a68f-4d63-a732-864fd0f7cbb2', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/sacredvalleyproject_contents.txt'}, page_content='full potential. SVP aims to achieve this vision by supporting rural, indigenous Peruvian girls in their educational goals.\tView Our 2024 Annual Report Here\tWhy Girls?\tGirls’ education strengthens economies and creates jobs. Millions of educated girls, means more working women with the potential to add up to $12 trillion USD to global growth.  -Malala Fund\tEducated women invest 90% of their earnings back into their families.  -Clinton Global Initiative\t420 million people would be lifted out of poverty by achieving a secondary education. This would cut the number of people living in poverty by more than half.  -UNESCO\tCommunities are more stable — and can recover faster after conflict — when girls are educated. When a country gives all its children secondary education, they cut their risk of war in half. Education is vital for security around the world because extremism grows alongside inequality.   -Malala Fund\tEducated girls are healthier citizens who raise healthier families. The World Bank reports that universal secondary education for girls could virtually eliminate child marriage.')]
# # Output returns 5 chunked docs
#     # Since we put "search_kwargs={'k': 3}"









# ##### Creating first chain - translating language
# #### Setup prompt
# SYST_PROMPT = """
#     You are an experienced Senior translator between English and Spanish.
#     Your role is to translate the input, English query into a Spanish verison.
#     Your associated pydantic model will have the following attributes:
#     * original: stores the original English query
#     * translation: stored the translated Spanish query

#     Below are a few examples of the task:
#     <Examples>
#     Original: "What are the organizaton's documents associated with education projects?"
#     Translation: "Cuales son los documentos de la organization que estan associados con proyectos educacionales?"
#     </Examples>
# """
# prompt = ChatPromptTemplate.from_messages([
#     ("system", SYST_PROMPT),
#     ("user", "This is the user's query: {query}")
# ])

# #### Setup pydantic model
# class Translator(BaseModel):
#     """Will detect the original user query and translate it to spanish"""
#     original: str = Field(...,
#         description="User's query in English"
#     )
#     translation: str = Field(...,
#         description="LLM's spanish translation of the user's query"
#     )

# #### Setup llm model
# translator_model = llm.with_structured_output(Translator)

# #### Setup translator chain
# translation_chain = prompt | translator_model










# ##### Creating second chain - spanish processing
# #### Create RunnableLambda
#     #In order to have chain get the run similar search on translated query
# inputs = RunnableLambda(
#     lambda x: retriever.invoke(x['entrada'])
# )
#     # Returns a LIST of docs (see line 132)

# #### Extracting the contents from the retrieved docs
# extract = RunnableLambda(
#     lambda x: [{"ingreso": doc.page_content} for doc in x]
#     # lambda x: [doc.page_content for doc in x]
#     # lambda x: [{"ingreso": doc.page_content} for doc in x]
# )

# #### Create prompt
# SYST_PROMPT = """
#     Eres un experto en traduciendo entre Espanol a Ingles.
#     Tu rol es traduccir informacion del Espanol al Ingles.
#     Traducce la informacion sin agregar contexto no encontrado 
#     en la informacion que se te de.
# """

# prompt = ChatPromptTemplate.from_messages([
#     ("system", SYST_PROMPT),
#     ("user", "{ingreso}")
#     # ("user", "la informacion es: ")
# ])

# #### Create model
# modelo_espanol = llm

# #### Create output parser
# output = StrOutputParser()

# #### Creating chain
# mini_cadena = prompt | modelo_espanol | output
# cadena_espanol = inputs | extract | mini_cadena.map()
#     # Returns a LIST of translated docs


# # print("Segunda cadena")
# # lista = inputs.invoke({"entrada": "proyectos educacionales?"})
# # print(lista)
# #     #output: Nuestros Proyectos      admin   2025-05-12T23:21:22+00:00       En Qallariy, cada proyecto es una pieza fundamental en nuestro compromiso de transformar vidas. A lo largo de los años, hemos desarrollado iniciativas que abarcan desde el apoyo social hasta la educación y la cultura, siempre con el objetivo de brindar esperanza y oportunidades a quienes más lo necesitan.        Casa de Acogida Mantay  La Casa de Acogida Mantay es un hogar lleno de amor y orientación, donde jóvenes madres entre 12 y 18 años encuentran un refugio seguro. Aquí, las madres adolescentes y sus hijos reciben atención y cuidado en diversas áreas de servicio, como la guardería, el refuerzo educativo, la cocina y la lavandería. Cada rincón de la casa cuenta una historia de esperanza y resiliencia, y cada día se tejen nuevas esperanzas y futuros.  saber más       Artes y Oficios Mantay  La escuela de formación Mantay Artes y Oficios surge para brindar a las madres una capacitación técnica que les permita sustentarse al alcanzar la mayoría de edad. Su doble función combina formación matutina y producción vespertina, apoyando la sostenibilidad de
# # print("CONTINUANDO")
# # extract_map = extract.map()
# # print(extract_map.invoke(lista))
# #     #output: [Document(id='7ee29146-6ab7-4518-b7eb-2fb6617dae3c', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/mantay_contents.txt'}, page_content='Nuestros Proyectos\tadmin\t2025-05-12T23:21:22+00:00\tEn Qallariy, cada proyecto es una pieza fundamental en nuestro compromiso de transformar vidas. A lo largo de los años, hemos desarrollado iniciativas que abarcan desde el apoyo social hasta la educación y la cultura, siempre con el objetivo de brindar esperanza y oportunidades a quienes más lo necesitan.\tCasa de Acogida Mantay\tLa Casa de Acogida Mantay es un hogar lleno de amor y orientación, donde jóvenes madres entre 12 y 18 años encuentran un refugio seguro. Aquí, las madres adolescentes y sus hijos reciben atención y cuidado en diversas áreas de servicio, como la guardería, el refuerzo educativo, la cocina y la lavandería. Cada rincón de la casa cuenta una historia de esperanza y resiliencia, y cada día se tejen nuevas esperanzas y futuros.\tsaber más\tArtes y Oficios Mantay\tLa escuela de formación Mantay Artes y Oficios surge para brindar a las madres una capacitación técnica que les permita sustentarse al alcanzar la mayoría de edad. Su doble función combina formación matutina y producción vespertina, apoyando la sostenibilidad de'), Document(id='65add5d7-a386-44b3-8fd7-1ad23d0d84d3', metadata={'source': '/home/jp/Documents/ComplexifyAgents/LangGraph/Course2_7/GrantsWriter/links_and_documents/mantay_contents.txt'}, page_content='albergadas reciben apoyo educativo continuo, abarcando desde la escolarización regular hasta la educación alternativa, para que nadie se quede atrás en el camino del aprendizaje.\tCocina\tIngredientes que nutren el cuerpo y el alma\tEn Mantay, la cocina es un rincón de aprendizaje en habilidades domésticas, donde la chef se transforma en una mentora práctica para las jóvenes mamás. Con su guía, cada clase se torna en una experiencia íntima, en la que la preparación de distintos alimentos se convierte en una lección de vida. No se trata solo de cocinar, sino de nutrir el alma con amor. Aquí se elaboran cinco comidas diarias —desayuno, almuerzo, cena y dos meriendas— que acarician tanto el cuerpo como el espíritu. Durante la semana, la chef lidera la actividad junto a alguna mamá residente, mientras que los fines de semana la tarea recae en las propias jóvenes, quienes se enriquecen al asumir esta responsabilidad.\tLavandería\tUn espacio de cuidado compartido\tLa lavandería es un espacio esencial en Mantay, especialmente por la gran cantidad de bebés y niños pequeños que lo habitan. Sabina,')]
# # print('SIGUIENTE')
# # otra_cadena = extract | prompt
# # # print('CONTINUANDO')
# # otra_cadena_resultados = otra_cadena.map().invoke(lista)
# # print(otra_cadena_resultados)
# # print('ultimo')
# # resultado = mini_cadena.map().invoke(lista)
# # print(resultado)


# # print('investiagndo')
# # results = cadena_espanol.invoke({'entrada': "proyectos educacionales?"})
# # print(results)


# # print("QUE ES")
# # print(prompt.invoke({'ingreso': 'UNODOSTRES'}))






# ##### Main pipeline
# #### Putting it all together
# def together(user_input: str) -> str:
#     ### Running the first chain
#     translation_results = translation_chain.invoke({
#         "query": user_input
#     })
#     original = translation_results.original
#     translation = translation_results.translation

#     ### Running the second chain
#     context_spanish = cadena_espanol.invoke({
#         "entrada": translation
#     })
#         #Returns list of strings
#             # These strings are translated versions of the original doc

#     ### Running similarity search on original query
#     context_english = retriever.invoke(original)
#     context_english = [x.page_content for x in context_english]

#     ### Combining all info together
#     final_context = "\n\n\n".join(context_english + context_spanish)
#     return final_context


# print(together("What are current educational projects?"))






























































































###### New dirty

##### General setup
#### Importing libraries
### General libraries
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableLambda
from langchain_core.output_parsers.string import StrOutputParser
### Model libraries
from langchain_community.embeddings import JinaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
### Embedding libraries
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
### Utilities library
from utilities_clean import *
import pprint

#### Setting up environment
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
jina_api_key = os.getenv("JINA_API_KEY")

# ### Setting up models
# ## LLM model
#     # Web: https://aistudio.google.com/welcome
# llm = ChatGoogleGenerativeAI(
#     api_key=google_api_key,
#     model="gemini-2.5-flash-lite",
#     # max_tokens=128
# )
# ## Embedding model
#     # Web: https://jina.ai/
# embedding_model = JinaEmbeddings(
#     api_token=jina_api_key,
#     model="jina-embeddings-v2-base-es"
# )

# llm = None
# embedding_model = None

### Setting up Utilities class for working with data
DB_NAME = 'output.db'
TABLE_NAME = 'rag'
DATA_ID = 1
storage = Storage(DB_NAME, TABLE_NAME)

utilities = Utilities()
metrics = Metrics()










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
    search_kwargs={"k": 1}
        #Number of chunked documents to return
)
























##### Creating first chain - translating language
#### Setup prompt
SYST_PROMPT = """\
You are an experienced Senior translator between English and Spanish. \
Your role is to translate the input, English query into a Spanish verison. \
Your associated pydantic model will have the following attributes:
* original: stores the original English query
* translation: stored the translated Spanish query

Below are a few examples of the task:
<Examples>
Original: "What are the organizaton's documents associated with education projects?"
Translation: "Cuales son los documentos de la organization que estan associados con proyectos educacionales?"
</Examples>\
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", SYST_PROMPT),
    ("user", "This is the user's query: {query}")
])

#### Setup pydantic model
class Translator(BaseModel):
    """Will detect the original user query and translate it to spanish"""
    original: str = Field(...,
        description="User's query in English"
    )
    translation: str = Field(...,
        description="LLM's spanish translation of the user's query"
    )

#### Setup llm model
translator_model = llm.with_structured_output(Translator, include_raw=True)

#### Setup translator chain
translation_chain = prompt | translator_model

#### Checking out chain output
### First invocation
# result_chain_one = translation_chain.invoke(
#     "What are current educational project?"
# )
# print('CHAIN ONE')
# print(type(result_chain_one))
# print(result_chain_one)

# DATA_ID = storage.save_data(result_chain_one, 2)

## Data retrieved
# first_chain_data = storage.retrieve_data(1)
    # Has invocation output with "include_raw = False", line 560
# print(type(first_chain_data))
# print(first_chain_data)
# print('\n' * 3)

# first_chain_data = storage.retrieve_data(2)
    # Has invocation results with "include_raw = True", line 560
# print(type(first_chain_data))
# pprint.pprint(
#     first_chain_data,
#     indent = 3,
#     depth = 3
# )
# print('\n' * 3 + "=" * 30)
# utilities.disect(first_chain_data['raw'])


# pyd = first_chain_data['parsed']
# print(pyd.original)
# print(pyd.translation)

# print(dir(first_chain_data['raw']))
# print(dict(first_chain_data['raw']))

# dicti = dict((first_chain_data)['raw'])

# for k,v in dicti.items():
#     print(k)
#     print(v)
#     print('\n' * 2)



#### Checking out the fill analysiss of the LC MEssage
# print(f'Breakdown analysis')
# utilities.disect(dicti)
# utilities.multi_analysis(dicti)

### CHekcing out metrics
# print('Metrics analysis')
# extract = metrics.extract_tokens_used(dicti, 'aimsg1')
# print(extract)
# hist = metrics.aggregate(extract)
# print(hist.history)






# print('TURNING TO JSON')
# json_str = json.dumps(dicti, indent=3)
# print(json_str)


# # printing = pprint.pp(
# #     dicti,
# #     indent = 3,
# #     depth = 1
# # )
# #     #Actually ends up printing the output itself
# # print(type(printing))
# # print(dir(printing))

# print('=' * 30)

# print('FIRST')
#     #DOES NOT WORK
# pprint.pp(
#     dicti,
#     indent = 3,
#     depth = 1
# )
#     #This needs to be done to perform the pprint output
# print('=' * 30)

# print('SECON')
# pprint.pp(
#     dicti,
#     indent = 3,
#     depth = 2
# )

# print('=' * 30)

# print('THIRD')
# pprint.pp(
#     dicti,
#     indent = 3,
#     depth = 3
# )

# print('=' * 30)

# print('FOURTH')
# pprint.pp(
#     dicti,
#     indent = 3,
#     depth = 4
# )

# print('=' * 30)

# print('Fifth')
# pprint.pp(
#     dicti,
#     indent = 3,
#     depth = 5
# )







# for k,v in first_chain_data['raw'].items():
#     print(k)
#     print(v)
#     print('\n' * 2)

# first_chain_data['raw'].pretty_print()
    #TODO:
        #Design utility fcn that will completely disect "AnyMesssage"
                # in a visually and practicall appealing way





















##### Creating second chain - spanish processing
#### Create RunnableLambda
    #In order to have chain get the run similar search on translated query
inputs = RunnableLambda(
    lambda x: retriever.invoke(x['entrada'])
)
    # Returns a LIST of docs (see line 132)

#### Extracting the contents from the retrieved docs
extract = RunnableLambda(
    lambda x: [{"ingreso": doc.page_content} for doc in x]
    # lambda x: [doc.page_content for doc in x]
    # lambda x: [{"ingreso": doc.page_content} for doc in x]
)

#### Create prompt
SYST_PROMPT = """\
Eres un experto en traduciendo entre Espanol a Ingles. \
Tu rol es traduccir informacion del Espanol al Ingles. \
Traducce la informacion sin agregar contexto no encontrado \
en la informacion que se te de.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYST_PROMPT),
    ("user", "{ingreso}")
    # ("user", "la informacion es: ")
])

#### Create model
modelo_espanol = llm

#### Create output parser
# output = StrOutputParser()
    #No lo voy a usar para sacar el "AIMessage" completo

#### Creating chain
mini_cadena = prompt | modelo_espanol 
cadena_espanol = inputs | extract | mini_cadena.map()
    # IMPORTANT: Returns a LIST of translated docs

#### Using the chain
# results = cadena_espanol.invoke({
#     'entrada' : 'proyectos educacionales'
# })

# storage.save_data(results, 3)

# print('DONE')

#### Exploring chain results

# results = storage.retrieve_data(3)
# print(results)
# utilities.disect(results[0])
    # Recall: results is a LIST, as mentioned in linbe 785

#### Metrics analysis
# print('Metrics analysis')
# extract = metrics.extract_tokens_used(results[0], 'aimsg2')
# print(extract)
# hist = metrics.aggregate(extract)
# print(hist.history)














##### Main pipeline
#### Putting it all together
### Create DB Storage class
    #Reason for intializing outside RAG class:
        # It connects to a DB
            # Thus, it might fails/ be timely
            # But if we leave it outside, it wouldn't corrupt RAG class
### Recreate DB table for final invocation check
DB_NAME = 'output.db'
TABLE_NAME = 'rag_table'
DATA_ID = 1
storage = Storage(DB_NAME, TABLE_NAME)

### Create the RAG class
class RAG():
    def __init__(self, data_id:int):
        self.data_id = data_id
        self.metrics = Metrics()

    def invoke(self, user_input: str) -> str:
        ### Running the first chain
        name = 'first_chain'
        translation_results = translation_chain.invoke({
            "query": user_input
        })  # Returns an AI Message
        
        # Saving the first chain
        self.data_id = storage.save_data(translation_results, self.data_id, name)
        
        

        # ### ALTERNATIVE
        # translation_results = storage.retrieve_data(1)
        # print(translation_results)
        # print('=' * 50)



        # Analyze metrics
        extract = metrics.extract_tokens_used(translation_results['raw'], name)
        self.metrics = metrics.aggregate(extract)

        # Get the pydantic results
        py_model = translation_results['parsed']
        original = py_model.original
        translation = py_model.translation



        ### Running the second chain
        context_spanish = cadena_espanol.invoke({
            "entrada": translation
        })
            #Returns list of strings
                # These strings are translated versions of the original doc

        #Save and metric the results of the second chain
        spanish_context_string = []
        for i, item in enumerate(context_spanish):
            name = f'second_chain_{i}'
            self.data_id = storage.save_data(item, self.data_id, name)
            extract = metrics.extract_tokens_used(item, name)
            self.metrics = metrics.aggregate(extract)
            spanish_context_string.append(item.content)



        # #### Alternative #####
        # context_spanish = storage.retrieve_data(2)
        # print(context_spanish)
        # print('=' * 50)
        # extract = metrics.extract_tokens_used(context_spanish, name)
        # self.metrics = metrics.aggregate(extract)
        # spanish_context_string = [context_spanish.content]



        ### Running similarity search on original query
        context_english = retriever.invoke(original)
        context_english = [x.page_content for x in context_english]

        ### Combining all info together
        final_context = "\n\n\n".join(context_english + spanish_context_string)
        self.data_id = storage.save_data(final_context, self.data_id, 'final_rag_context')
        return final_context, self.data_id

# rag = RAG(DATA_ID)
# final_context, last_id = rag.invoke("What are current educational projects?")
# print(final_context)
# print('='*50)
# print(last_id)
# print('='*50)
# print(rag.metrics.history)




















































