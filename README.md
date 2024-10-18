# Product Repair App Project

An application that takes in a picture of a device as well as a prompt explaining the problem the user is facing with the project. The application identifies the product and returns actionable steps to fix the product.

Tech Stack:
- LangChain: Used for building agents: MultiQueryAgent, web search using DuckDuckGo, connecting with ChromaDB 
- LangGraph: Used to connect the agents together and build a cohesive workflow
- OpenAI API & LLama3.1 8B: OPENAI API used to identify product in image; LLAMA3.1 used to retrieve from local vector db and for generation.
- ChromaDB: Database to store embeddings of several pdfs of repair manuals

# Preview:
![Product Repair App Website](https://github.com/user-attachments/assets/37d289d3-1da5-4b6b-96cc-9ad51edf446e)

# Process Flows:
Fig 1: Architecture
![PRArchiColour drawio](https://github.com/user-attachments/assets/c1ff143c-739c-4bdb-8756-9d03f1b656bc)

<br><br>

Fig 2: Flow
![PRFlowColour drawio](https://github.com/user-attachments/assets/4c0900e1-4435-44ef-a309-875cac65846f)
