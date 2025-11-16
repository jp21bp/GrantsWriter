###### RAG agent
    # Will be used on organization content blob found on main webpage
    # Recall: blob is in one big text file
        # Thus, we'll need a diff strat than Jopara RAG
            # Specifically, we won't need "document_loaders"
        # We'll simply open the file
        # Rest is similar to JoparaRAG

##### General setup
#### Importing libraries

#### Setting up environment

#### Setting up LLM





##### File Embeddings
#### Create embedding model

#### Loading text file(s)

#### Split text into chunks

#### Creating vector store

#### Setting up retriever







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












