from config import gemini_client, groq_client, openrouter_client
from tools import available_tools
from model_select import ModelRouter
from agent import Agent
from retriever import search_documents
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
            # =====================================
            # RETRIEVE RELEVANT DOCUMENTS
            # =====================================

            # documents = search_documents(user_query, document_id=document_id)

            context = search_documents(user_query)

            # =====================================
            # AUGMENT USER QUERY
            # =====================================

            augmented_query = f"""
            Use the following context to help answer the user's question.

            IMPORTANT:
            - Answer using the provided context when the information is available.
            - Do not invent facts that are not supported by the context.
            - If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.

            CONTEXT:
            {context}

            USER QUESTION:
            {user_query}
            """

            for event in agent.run(augmented_query):

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

                    print(f"\n🛠️ Tool: {tool}")
                    print(f"Input: {tool_input}")

                elif event_type == "tool_result":

                    tool = event.get("tool")

                    print(f"✅ {tool} completed")

                elif event_type == "output":

                    content = event.get("content")

                    print("\n🤖 Final Answer:\n")
                    print(content)

                elif event_type == "error":

                    error = event.get("error")

                    print(f"\n❌ Agent Error: {error}")

                elif event_type == "model_response":

                    # Keep raw model responses hidden from
                    # normal CLI output.
                    logger.debug(f"Model response: " f"{event.get('raw')}")

        except Exception as e:

            logger.error(
                f"❌ Agent execution failed: {e}",
                exc_info=True,
            )

            print(f"\n❌ Something went wrong: {e}")


def run_query(user_query: str, document_id: str = None):
    user_query = user_query.strip()
    output = ""
    if not user_query:
        return "No query from user received"
    try:
        context = search_documents(user_query, document_id=document_id)
        augmented_query = f"""
        Use the following context to help answer the user's question.
        
        IMPORTANT:
        - Answer using the provided context when the information is available.
        - Do not invent facts that are not supported by the context.
        - If the answer cannot be found in the context, clearly say that the information is not available in the provided documents.
        
        CONTEXT:
        {context}
        
        USER QUESTION:
        {user_query}
        """
        for event in agent.run(augmented_query):
            event_type = event.get("type")

            if event_type == "step":
                step = event.get("step")
                content = event.get("content")
                print(f"\n🔹 {step}")
                print(content)
            elif event_type == "tool_start":
                tool = event.get("tool")
                print(f"✅ {tool} completed")
            elif event_type == "output":
                content = event.get("content")
                return content
    except Exception as e:
        return f"Model cannot respond due to reason : {e}"

    return f"Something went wrong"


if __name__ == "__main__":
    main()
