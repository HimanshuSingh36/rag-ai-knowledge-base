from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional,Literal

load_dotenv()
client = OpenAI(api_key=os.getenv("google_api_key"), base_url=os.getenv("google_base_url"))


def get_weather(city: str):

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"

    return "Something went wrong"


availble_tools = {"get_weather": get_weather}


SYSTEM_PROMPT = """
    You are an expert AI assistant that solves user queries using chain-of-thought reasoning.
    You work strictly in three phases: start, plan, output.
    You need to first plan what needs to be done. The plan can be multiple steps
    once you think enough plan has been done, finally you can give output.
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Only give best solution
    - Strictly follow the given JSON output format
    - Only run one step at a time
    - The sequence of step is start(onnce the user gives the input), plan(that can be multiple time) and then finally output
    - Always think step-by-step. Break the problem into the smallest possible atomic steps
        (e.g., one arithmetic operation, one logical deduction, or one sub-task per step).
    - Do NOT skip steps or combine multiple operations into a single "Plan" step.
    - Follow standard rules/conventions relevant to the problem (e.g., BODMAS/PEMDAS for math).
    - Before giving the final "Output", include a step where you verify your reasoning/result.
    - Only run ONE step at a time. Wait for the next turn to continue.
    - Strictly return a single valid JSON object per response. No extra text, no markdown.
    - The "step" field must be exactly one of: "Start", "Plan", "Output".

    CRITICAL JSON SAFETY RULES for the "content" field:
    - The "content" value must be a single valid JSON string.
    - NEVER use triple quotes (\"\"\") — they are not valid JSON.
    - If content includes code or multi-line text, escape newlines as \\n and
      escape any double quotes inside as \\".
    - Do not include literal unescaped newlines, tabs, or unescaped quotes.


    Output JSON Format:
    { "step": "Start" | "Plan" | "Output" | "Tool", "content" : "string", "tool" : "string", "input" : "string" }

    Available Tools:
    - get_weather(city : str): Takes city name as a string and returns the weather information about the city


    Example 1:
    START: {"step": "Start", "content": "Hey, can you solve 2 + 3 * 5 / 10"}
    PLAN: {"step": "Plan", "content": "The user wants to evaluate a math expression. I should follow BODMAS/PEMDAS order of operations."}
    PLAN: {"step": "Plan", "content": "First, resolve multiplication: 3 * 5 = 15."}
    PLAN: {"step": "Plan", "content": "Next, resolve division: 15 / 10 = 1.5."}
    PLAN: {"step": "Plan", "content": "Next, resolve addition: 2 + 1.5 = 3.5."}
    PLAN: {"step": "Plan", "content": "Double-checking: 2 + (3 * 5 / 10) = 2 + 1.5 = 3.5. This is correct."}
    OUTPUT: {"step": "Output", "content": "The answer is 3.5"}

    Example 2:
    START:{"step": "Start", "content": "Hey, can tell me the weather of delhi today"}
    PLAN: {"step": "Plan", "content": "The user wants to know the weather of Delhi."}
    PLAN: {"step": "Plan", "content": "Let's see if we have any suitable tool for this user's query "}
    PLAN: {"step": "Plan", "content": "Great, we have get_weather tool which takes city: str as parameter"}
    PLAN: {"step": "Plan", "content": "As user want to know the weather of delhi we'll use get_weather tool and pass Delhi as parameter (get_weather(delhi))"}
    PLAN: {"step": "Tool", "tool" : "get_weather", "input": "delhi"}
    PLAN: {"step": "Observe", "tool" : "get_weather" , "imput": "Delhi", "content": "The current weather of delhi is 28°C and today is expected to be a rainy day in Delhi"}
    PLAN: {"step": "Plan", "content": "Great, i got the information of weather of delhi"}
    OUTPUT: {"step": "Output", "content": "The current weather of delhi is 28°C and today is expected to be a rainy day in Delhi"}
"""
class Output_format(BaseModel):
    step: Literal["Start", "Plan", "Tool", "Observe", "Output"]
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    while True:
        user_query = input("😀 What's your query for today : ")
        messages.append(
            {"role": "user", "content": user_query},
        )

        while True:
            response = client.chat.completions.parse(
                model="gemini-3.6-flash",
                response_format=Output_format,
                messages=messages
            )

            raw_content = response.choices[0].message.content

            messages.append({"role": "assistant", "content": raw_content})

            parsed_data = response.choices[0].message.parsed
            # print("RAW RESPONSE:", raw_content)
            # print("PARSED DATA:", parsed_data)
            content = parsed_data.content
            step = parsed_data.step

            if parsed_data.step == "Start":
                print(f"🏁Starting the process : {content}")
                messages.append({"role": "user", "content": "Continue to the next step."})
                continue

            elif parsed_data.step == "Plan":
                print(f"🤔 Planning the process : {content}")
                messages.append({"role": "user", "content": "Planning next step."})
                continue

            elif parsed_data.step == "Tool":
                tool_to_Call = parsed_data.tool
                parsed_data_input = parsed_data.input
                print(f"🛠️: {tool_to_Call} ({parsed_data_input})")
                tool_response = availble_tools[tool_to_Call](parsed_data_input)
                print(f"🛠️: {tool_to_Call} ({parsed_data_input}) = {tool_response}")
                messages.append(
                    {
                        "role": "user",
                        "content": f"""
                        Tool execution result:
                    
                    Tool: {tool_to_Call}
                    Input: {parsed_data_input}
                    Result: {tool_response}
                    
                    Process this result and continue to the next step.
                    """,
                    }
                )
                continue

            elif parsed_data.step == "Observe":
                parsed_data_input = parsed_data.input
                print(f"Getting the current values for weather of {parsed_data_input}")
                messages.append({"role": "user", "content": f"Got the current values for weather of {parsed_data_input}, Continuing to the next step."})
                continue

            elif parsed_data.step == "Output":
                print(
                    f"🤖 Processing done ✅ \n here is the output of your query : {content}"
                )
                break
            else:
                print(f"Unknown step found 🤪\n Aborting process ❌", step)
                break


main()


# /////////////////// upgraded from claude /////////////////////////////////

# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# import json
# import requests

# load_dotenv()

# client = OpenAI(api_key=os.getenv("groq_api_key"), base_url=os.getenv("groq_base_url"))


# def get_weather(city: str):

#     url = f"https://wttr.in/{city.lower()}?format=%C+%t"

#     response = requests.get(url, timeout=10)

#     if response.status_code == 200:
#         return f"The weather of {city} is {response.text.strip()}"

#     return f"Could not get weather for {city}"


# available_tools = {"get_weather": get_weather}


# SYSTEM_PROMPT = """
# You are an AI assistant that can use tools.

# Your job is to decide whether you need a tool and then provide the final answer.

# Available tool:

# get_weather(city: str)
# - Returns the current weather for a city.

# You MUST return exactly one valid JSON object.

# The JSON must have exactly this structure:

# {
#     "step": "Plan" | "Tool" | "Output",
#     "content": "string",
#     "tool": "string",
#     "input": "string"
# }

# Rules:

# 1. If a tool is required, return:
# {
#     "step": "Tool",
#     "content": "brief description",
#     "tool": "get_weather",
#     "input": "city name"
# }

# 2. After receiving a tool result, use the tool result as the source of truth.

# 3. NEVER invent, modify, estimate, or contradict a tool result.

# 4. If multiple cities are requested, call get_weather for each required city.

# 5. If the same city appears more than once, you may reuse the previous result.

# 6. When enough information has been collected, return:
# {
#     "step": "Output",
#     "content": "final answer",
#     "tool": "",
#     "input": ""
# }

# 7. Do not generate a Start step.

# 8. Do not generate an Observe step.

# 9. Do not include markdown.

# 10. Do not include any text outside the JSON object.

# 11. Always include all four fields:
# step, content, tool, input.
# """


# def ask_llm(messages):

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=messages,
#         response_format={"type": "json_object"},
#         temperature=0,
#     )

#     raw_content = response.choices[0].message.content

#     print("\nRAW RESPONSE:")
#     print(raw_content)

#     try:
#         data = json.loads(raw_content)
#     except json.JSONDecodeError as e:

#         print("❌ Invalid JSON from model")
#         print(e)

#         return None

#     return data


# def main():


#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#     ]
#     while True:
#         user_query = input("😀 What's your query for today : ")
#         messages.append({
#                     "role": "user",
#                     "content": user_query
#                 })

#     # Store tool results so we don't unnecessarily call the same city twice
#         tool_results = {}

#         # Safety limit
#         max_iterations = 10

#         while True:


#             print(f"\n========== ITERATION==========")

#             parsed_data = ask_llm(messages)

#             if parsed_data is None:
#                 print("❌ Stopping because model returned invalid JSON.")
#                 break

#             # Validate required fields
#             step = parsed_data.get("step")
#             content = parsed_data.get("content", "")
#             tool_name = parsed_data.get("tool", "")
#             tool_input = parsed_data.get("input", "")

#             if not step:
#                 print("❌ Model did not return a step.")
#                 print(parsed_data)
#                 break

#             print("STEP:", step)

#             # ------------------------------------------------
#             # PLAN
#             # ------------------------------------------------

#             if step.lower() == "plan":

#                 print(f"🤔 Planning: {content}")

#                 messages.append({"role": "assistant", "content": json.dumps(parsed_data)})

#                 continue

#             # ------------------------------------------------
#             # TOOL
#             # ------------------------------------------------

#             elif step.lower() == "tool":

#                 if not tool_name:
#                     print("❌ Tool name is missing.")
#                     break

#                 if not tool_input:
#                     print("❌ Tool input is missing.")
#                     break

#                 if tool_name not in available_tools:
#                     print(f"❌ Unknown tool: {tool_name}")
#                     break

#                 print(f"🛠️ Calling {tool_name}({tool_input})")

#                 # Normalize city name
#                 city = tool_input.strip().lower()

#                 # Reuse previous result if same city was already requested
#                 if city in tool_results:

#                     print(f"♻️ Reusing previous result for {city}")

#                     tool_response = tool_results[city]

#                 else:

#                     tool_response = available_tools[tool_name](tool_input)

#                     tool_results[city] = tool_response

#                 print(f"🛠️ Result: {tool_response}")

#                 # Tell the model what the tool ACTUALLY returned
#                 messages.append({"role": "assistant", "content": json.dumps(parsed_data)})

#                 messages.append(
#                     {
#                         "role": "user",
#                         "content": json.dumps(
#                             {
#                                 "type": "tool_result",
#                                 "tool": tool_name,
#                                 "input": tool_input,
#                                 "result": tool_response,
#                             }
#                         ),
#                     }
#                 )

#                 continue

#             # ------------------------------------------------
#             # OUTPUT
#             # ------------------------------------------------

#             elif step.lower() == "output":

#                 print("\n🤖 Processing done ✅")
#                 print(f"\n{content}")

#                 break

#             # ------------------------------------------------
#             # UNKNOWN
#             # ------------------------------------------------

#             else:

#                 print(f"❌ Unknown step: {step}")
#                 print(parsed_data)

#                 break

#         else:

#             print("❌ Agent stopped: maximum iterations reached.")


# main()
