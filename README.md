# ProductRepairAppProject

An application that takes in a picture of a device as well as a prompt explaining the problem the user is facing with the project. The application identifies the product and returns actionable steps to fix the product.

Tech Stack:
- LangChain: Used for building agents: MultiQueryAgent, web search using DuckDuckGo, connecting with ChromaDB 
- LangGraph: Used to connect the agents together and build a cohesive workflow
- OpenAI API & LLama3.1 8B: OPENAI API used to identify product in image; LLAMA3.1 used to retrieve from local vector db and for generation.
- ChromaDB: Database to store embeddings of several pdfs of repair manuals

