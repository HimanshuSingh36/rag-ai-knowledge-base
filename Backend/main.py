# from config import gemini_client, groq_client, openrouter_client
# from prompts import SYSTEM_PROMPT
# from schema import Output_format
# from tools import AVAILABLE_TOOL_NAMES, available_tools
# from openai import (
#     RateLimitError,
#     APIConnectionError,
#     AuthenticationError,
#     BadRequestError,
# )
# import time
# from logger import logger
# from model_select import ModelRouter
# import json

# FALLBACK_MODELS = [
#     # OpenRouter
#     {"model": "openrouter/free", "get_client": openrouter_client},
#     {"model": "deepseek/deepseek-v4-flash", "get_client": openrouter_client},
#     {"model": "qwen/qwen3-next-80b-a3b-instruct", "get_client": openrouter_client},
#     {
#         "model": "qwen/qwen3-coder-480b-a35b-instruct",
#         "get_client": openrouter_client,
#     },
#     {"model": "qwen/qwen3-30b-a3b-thinking-2507", "get_client": openrouter_client},
#     {"model": "google/gemma-4-31b-it", "get_client": openrouter_client},
#     {"model": "google/gemma-4-26b-a4b-it", "get_client": openrouter_client},
#     # Gemini
#     {"model": "gemini-2.5-flash", "get_client": gemini_client},
#     {"model": "gemini-2.5-flash-lite", "get_client": gemini_client},
#     # Groq
#     {"model": "llama-3.1-8b-instant", "get_client": groq_client},
#     {"model": "llama-3.3-70b-versatile", "get_client": groq_client},
#     {"model": "openai/gpt-oss-120b", "get_client": groq_client},
#     # {"model": "openai/gpt-oss-20b", "get_client": groq_client},
# ]
# router = ModelRouter(FALLBACK_MODELS)


# def call_model(messages):
#     delay = 2
#     max_retry = 5

#     for attempt in range(max_retry):
#         try:
#             response = ModelRouter(messages)
#             return response
#             # return client.chat.completions.parse(
#             #     model="gemini-3.6-flash",
#             #     response_format=Output_format,
#             #     messages=messages,
#             # )
#         except RateLimitError:
#             print(
#                 f"⏳ Rate limited. Retrying in {delay}s (attempt {attempt + 1}/{max_retry})"
#             )
#             time.sleep(delay)
#             delay *= 2
#         except APIConnectionError:
#             print("🌐 Network issue. Retrying...")
#             time.sleep(delay)
#         except AuthenticationError:
#             raise SystemExit("❌ Invalid API key. Check your .env file.")
#         except BadRequestError as e:
#             print(f"⚠️ Malformed request: {e}")
#             raise
#     raise RuntimeError("Exceeded max retries calling the model.")


# def model():
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#     ]

#     while True:
#         user_query = input("👉")
#         messages.append(
#             {"role": "user", "content": user_query},
#         )

#         while True:
#             response = router.call(messages)
#             # print("/n response is : ", response)
#             # print("\n\n🛠️ debugging", response.model)
#             # response=client.chat.completions.parse(
#             #     model=model,
#             #     response_format=Output_format,
#             #     messages=messages,
#             # )

#             raw_content = response.choices[0].message.content
#             print("raw : ", raw_content)
#             parsed_data = json.loads(raw_content)
#             messages.append({"role": "assistant", "content": raw_content})

#             # parsed_data = response.choices[0].message.parsed
#             # print("parsed data :", parsed_data)
#             content = parsed_data.get("content")
#             step = parsed_data.get("step")

#             if parsed_data.get("step") == "Start":
#                 logger.info(f"🏁Starting the process : {content}")
#                 messages.append(
#                     {"role": "user", "content": "Continue to the next step."}
#                 )
#                 continue

#             elif parsed_data.get("step") == "Plan":
#                 logger.debug(f"🤔 Planning the process : {content}")
#                 messages.append({"role": "user", "content": "Planning next step."})
#                 continue

#             elif parsed_data.get("step") == "Tool":
#                 tool_to_Call = parsed_data.get("tool")
#                 parsed_data_input = parsed_data.get("input")
#                 logger.info(f"🛠️: {tool_to_Call} ({parsed_data_input})")
#                 tool_response = available_tools[tool_to_Call](parsed_data_input)
#                 logger.debug(
#                     f"🛠️: {tool_to_Call} ({parsed_data_input}) = {tool_response}"
#                 )
#                 messages.append(
#                     {
#                         "role": "user",
#                         "content": f"""
#                         Tool execution result:
                    
#                     Tool: {tool_to_Call}
#                     Input: {parsed_data_input}
#                     Result: {tool_response}
                    
#                     Process this result and continue to the next step.
#                     """,
#                     }
#                 )
#                 continue
#             elif parsed_data.get("step") == "Output":
#                 logger.info("Processing done.")
#                 print(
#                     f"🤖 Processing done ✅ \n here is the output of your query : {content}"
#                 )
#                 break
#             else:
#                 logger.error(f"Unknown step found 🤪\n Aborting process ❌", step)
#                 break


# if __name__ == "__main__":
#     model()
from config import gemini_client, groq_client, openrouter_client
from tools import available_tools
from model_select import ModelRouter
from agent import Agent
from logger import logger


# =========================================
# MODEL CONFIGURATION
# =========================================

FALLBACK_MODELS = [
    # OpenRouter
    {
        "model": "openrouter/free",
        "get_client": openrouter_client,
    },
    {
        "model": "deepseek/deepseek-v4-flash",
        "get_client": openrouter_client,
    },
    {
        "model": "qwen/qwen3-next-80b-a3b-instruct",
        "get_client": openrouter_client,
    },
    {
        "model": "qwen/qwen3-coder-480b-a35b-instruct",
        "get_client": openrouter_client,
    },
    {
        "model": "qwen/qwen3-30b-a3b-thinking-2507",
        "get_client": openrouter_client,
    },
    {
        "model": "google/gemma-4-31b-it",
        "get_client": openrouter_client,
    },
    {
        "model": "google/gemma-4-26b-a4b-it",
        "get_client": openrouter_client,
    },

    # Gemini
    {
        "model": "gemini-2.5-flash",
        "get_client": gemini_client,
    },
    {
        "model": "gemini-2.5-flash-lite",
        "get_client": gemini_client,
    },

    # Groq
    {
        "model": "llama-3.1-8b-instant",
        "get_client": groq_client,
    },
    {
        "model": "llama-3.3-70b-versatile",
        "get_client": groq_client,
    },
    {
        "model": "openai/gpt-oss-120b",
        "get_client": groq_client,
    },
]


# =========================================
# INITIALIZE MODEL ROUTER
# =========================================

router = ModelRouter(FALLBACK_MODELS)


# =========================================
# INITIALIZE AGENT
# =========================================

agent = Agent(
    router=router,
    available_tools=available_tools,
)


# =========================================
# CLI
# =========================================

def main():

    logger.info("🚀 AI Agent started.")

    while True:

        try:
            user_query = input("👉 ")

        except (KeyboardInterrupt, EOFError):

            logger.info("🛑 Agent stopped by user.")
            break

        user_query = user_query.strip()

        if not user_query:
            logger.warning("⚠️ Empty query received.")
            continue

        if user_query.lower() in {"exit", "quit"}:

            logger.info("🛑 Agent stopped by user.")
            break

        logger.info(f"👤 User query: {user_query}")

        # =====================================
        # RUN AGENT
        # =====================================

        try:

            for event in agent.run(user_query):

                # ---------------------------------
                # CLI display
                # ---------------------------------

                event_type = event.get("type")

                if event_type == "step":

                    step = event.get("step")
                    content = event.get("content")

                    print(f"\n🔹 {step}")
                    print(content)

                elif event_type == "tool_start":

                    tool = event.get("tool")
                    tool_input = event.get("input")

                    print(
                        f"\n🛠️ Tool: {tool}"
                    )
                    print(
                        f"Input: {tool_input}"
                    )

                elif event_type == "tool_result":

                    tool = event.get("tool")

                    print(
                        f"✅ {tool} completed"
                    )

                elif event_type == "output":

                    content = event.get("content")

                    print(
                        "\n🤖 Final Answer:\n"
                    )
                    print(content)

                elif event_type == "error":

                    error = event.get("error")

                    print(
                        f"\n❌ Agent Error: {error}"
                    )

                elif event_type == "model_response":

                    # Keep raw model responses hidden from
                    # normal CLI output.
                    logger.debug(
                        f"Model response: "
                        f"{event.get('raw')}"
                    )

        except Exception as e:

            logger.error(
                f"❌ Agent execution failed: {e}",
                exc_info=True,
            )

            print(
                f"\n❌ Something went wrong: {e}"
            )

def run_query(user_query : str):
    user_query = user_query.strip()
    output=""
    if not user_query:
        return "No query from user received"
    try:
        for event in agent.run(user_query):
            event_type=event.get("type")

            if event_type=="step":
                step = event.get("step")
                content = event.get("content")
                print(f"\n🔹 {step}")
                print(content)
            elif event_type == "tool_start":
                tool = event.get("tool")
                print(f"✅ {tool} completed")
            elif event_type=="output":
                content = event.get("content")
                return content
    except Exception as e:
        return f"Model cannot respond due to reason : {e}"

    return f"Something went wrong"

if __name__ == "__main__":
    main()
