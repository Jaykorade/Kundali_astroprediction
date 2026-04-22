from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph
from pydantic import BaseModel
from chatbot.prompt import build_prompt
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

memory = ConversationBufferMemory(return_messages=True)

class ChatState(BaseModel):
    input: str
    history: list

def astrology_node(state: ChatState):
    prompt = f"""
    You are an expert Vedic astrologer.
    Answer based on kundali data and history.

    History: {state.history}
    Question: {state.input}
    """

    response = llm.invoke(prompt)

    return {
        "history": state.history + [state.input, response.content]
    }

def astrology_node(state):
    prompt = build_prompt(
        state["kundali"],
        state["dasha"],
        state["history"],
        state["input"]
    )

    response = llm.invoke(prompt)

    return {
        "history": state["history"] + [(state["input"], response.content)],
        "response": response.content
    }
graph = StateGraph(ChatState)
graph.add_node("astrology", astrology_node)
graph.set_entry_point("astrology")

chatbot = graph.compile()