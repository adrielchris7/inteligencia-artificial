"""The canonical ReAct prompt: tools + Thought / Action / Observation format."""

from __future__ import annotations

from react.tools import Tool

# Same skeleton as the lecture (Yao et al. 2023 / LangChain ZERO_SHOT_REACT_DESCRIPTION).
TEMPLATE = """You are a ReAct agent. Answer the question by interleaving thinking and tools.

You can use these tools:
{tool_list}

Use this format (keep these English labels; write Thought and Final Answer in Spanish):

Question: the input question you must answer
Thought: razona siempre en español sobre qué hacer
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (Thought / Action / Action Input / Observation can repeat N times)
Thought: Ya sé la respuesta final
Final Answer: the final answer to the original input question, in Spanish

Do not write Observation — the environment provides it after you stop.
Write only one Thought and either one Action or one Final Answer, then stop.
Every Thought must be in Spanish. Never write a Thought in English.
Use tools for facts. Do not invent weather, closet contents, or arithmetic.
If the question is about packing or clothes, call Weather and then Lookup with closet before the Final Answer.

Begin!

Question: {question}
"""

COT_TEMPLATE = """You are answering a question. Think step by step, then give a final answer.
You have no tools. Do not invent tool calls.

Use this format (keep these English labels; write Thought and Final Answer in Spanish):

Question: the input question you must answer
Thought: razona siempre en español sobre qué hacer
Final Answer: the final answer to the original input question, in Spanish

Every Thought must be in Spanish. Never write a Thought in English.

Begin!

Question: {question}
"""


def tool_list(tools: tuple[Tool, ...]) -> str:
    return "\n".join(f"- {tool.name}: {tool.description}" for tool in tools)


def tool_names(tools: tuple[Tool, ...]) -> str:
    return ", ".join(tool.name for tool in tools)


def build_prompt(question: str, tools: tuple[Tool, ...]) -> str:
    if not tools:
        return COT_TEMPLATE.format(question=question)
    return TEMPLATE.format(
        tool_list=tool_list(tools),
        tool_names=tool_names(tools),
        question=question,
    )
