from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

app = FastAPI()

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        # 1. Print incoming request for debugging
        print(f"Received Request: {query}")

        # 2. Initialize the Graph
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        # 3. Generate and save the Mermaid graph image
        try:
            png_graph = react_app.get_graph().draw_mermaid_png()
            with open("my_graph.png", "wb") as f:
                f.write(png_graph)
            print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        except Exception as graph_err:
            # If graph drawing fails (e.g., missing dependencies), 
            # we log it but don't crash the whole request.
            print(f"Graph drawing skipped: {graph_err}")

        # 4. Prepare messages for the AI
        # FIX: We use query.question to match the class definition above
        messages = {"messages": [HumanMessage(content=query.question)]}
        
        # 5. Invoke the LangGraph agent
        output = react_app.invoke(messages)

        # 6. Parse the final AI response
        if isinstance(output, dict) and "messages" in output:
            # Get the content of the very last message in the sequence
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)
        
        return {"answer": final_output}

    except Exception as e:
        import traceback
        print("--- ERROR TRACEBACK ---")
        traceback.print_exc()  # Crucial for debugging server-side issues
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )