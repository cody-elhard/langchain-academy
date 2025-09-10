from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

SHIFT = 2

def caeser_cipher_encode(msg: str) -> str:
  """Encrypts a message using caeser cipher

  Args:
      msg: message
  """
  result = ""
  for char in msg:
      if char.isalpha():
          base = ord('A') if char.isupper() else ord('a')
          result += chr((ord(char) - base + SHIFT) % 26 + base)
      else:
          result += char
  return result

def caeser_cipher_decode(msg: str) -> str:
    """Decrypts a message using caeser cipher

    Args:
        msg: message
    """
    result = ""
    for char in msg:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - SHIFT) % 26 + base)
        else:
            result += char
    return result

tools = [caeser_cipher_encode, caeser_cipher_decode]

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You handle my caeser cipher questions.")

def assistant(state: MessagesState):
  return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
  "assistant",
  tools_condition,
)
builder.add_edge("tools", "assistant")
graph = builder.compile()
  