import json

from prompts import SYSTEM_PROMPT
from logger import logger


class Agent:

    def __init__(self, router, available_tools):
        self.router = router
        self.available_tools = available_tools

        # Safety limits
        self.max_steps = 20
        self.max_invalid_responses = 3

    def run(self, user_query: str):

        logger.info(
            f"🚀 New agent request: {user_query}"
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_query,
            },
        ]

        step_count = 0
        invalid_response_count = 0

        while True:

            # =================================================
            # STEP LIMIT
            # =================================================

            step_count += 1

            logger.debug(
                f"🔄 Agent iteration: {step_count}"
            )

            if step_count > self.max_steps:

                logger.error(
                    f"❌ Agent exceeded maximum steps: "
                    f"{self.max_steps}"
                )

                yield {
                    "type": "error",
                    "stage": "agent",
                    "error": (
                        "Agent exceeded the maximum "
                        "number of steps."
                    ),
                }

                return

            # =================================================
            # MODEL CALL
            # =================================================

            logger.debug("🤖 Calling model...")

            try:
                response = self.router.call(messages)

            except Exception as e:

                logger.error(
                    f"❌ Model call failed: {e}",
                    exc_info=True,
                )

                yield {
                    "type": "error",
                    "stage": "model",
                    "error": str(e),
                }

                return

            # =================================================
            # EXTRACT RESPONSE
            # =================================================

            try:

                raw_content = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except (AttributeError, IndexError) as e:

                logger.error(
                    f"❌ Invalid model response: {e}",
                    exc_info=True,
                )

                yield {
                    "type": "error",
                    "stage": "response",
                    "error": str(e),
                }

                return

            model_name = getattr(
                response,
                "model",
                "unknown",
            )

            logger.debug(
                f"🤖 Model: {model_name}"
            )

            # =================================================
            # EMPTY RESPONSE
            # =================================================

            if raw_content is None or not raw_content.strip():

                invalid_response_count += 1

                logger.error(
                    f"❌ Model returned empty content. "
                    f"Model: {model_name}"
                )

                logger.error(
                    f"Full response: {response}"
                )

                if (
                    invalid_response_count
                    >= self.max_invalid_responses
                ):

                    yield {
                        "type": "error",
                        "stage": "response",
                        "error": (
                            "Model repeatedly returned "
                            "empty responses."
                        ),
                    }

                    return

                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Your previous response was empty. "
                            "Return exactly one valid JSON object "
                            "using the required format."
                        ),
                    }
                )

                continue

            # =================================================
            # RAW RESPONSE LOG
            # =================================================

            logger.debug(
                f"🤖 Model response "
                f"[{model_name}]: {raw_content}"
            )

            yield {
                "type": "model_response",
                "model": model_name,
                "raw": raw_content,
            }

            # =================================================
            # PARSE JSON
            # =================================================

            try:

                parsed_data = json.loads(
                    raw_content
                )

            except json.JSONDecodeError as e:

                invalid_response_count += 1

                logger.error(
                    f"❌ Failed to parse model JSON: {e}"
                )

                logger.error(
                    f"Raw response: {raw_content}"
                )

                if (
                    invalid_response_count
                    >= self.max_invalid_responses
                ):

                    yield {
                        "type": "error",
                        "stage": "json",
                        "error": str(e),
                        "raw": raw_content,
                    }

                    return

                messages.append(
                    {
                        "role": "user",
                        "content": """
Your previous response was not valid JSON.

Return ONLY one valid JSON object.

Required format:

{
    "step": "Start | Plan | Tool | Output",
    "content": "string",
    "tool": "string",
    "input": "string"
}

Do not use markdown.
Do not add any text outside the JSON object.
""",
                    }
                )

                continue

            # =================================================
            # JSON OBJECT VALIDATION
            # =================================================

            if not isinstance(parsed_data, dict):

                invalid_response_count += 1

                logger.error(
                    "❌ Model returned non-object JSON."
                )

                logger.error(
                    f"Parsed response: {parsed_data}"
                )

                messages.append(
                    {
                        "role": "user",
                        "content": """
Your previous response was valid JSON,
but it was not a JSON object.

Return exactly one JSON object with:

{
    "step": "Start | Plan | Tool | Output",
    "content": "string",
    "tool": "string",
    "input": "string"
}
""",
                    }
                )

                if (
                    invalid_response_count
                    >= self.max_invalid_responses
                ):

                    yield {
                        "type": "error",
                        "stage": "validation",
                        "error": (
                            "Model repeatedly returned "
                            "an invalid JSON structure."
                        ),
                    }

                    return

                continue

            # =================================================
            # EXTRACT DATA
            # =================================================

            step = parsed_data.get("step")
            content = parsed_data.get(
                "content",
                "",
            )
            tool_name = parsed_data.get(
                "tool",
                "",
            )
            tool_input = parsed_data.get(
                "input",
                "",
            )

            logger.debug(
                f"📦 Parsed agent response: "
                f"step={step}, "
                f"tool={tool_name}, "
                f"input={tool_input}"
            )

            # =================================================
            # VALIDATE STEP
            # =================================================

            valid_steps = {
                "Start",
                "Plan",
                "Tool",
                "Output",
            }

            if step not in valid_steps:

                invalid_response_count += 1

                logger.error(
                    f"❌ Invalid agent step: {step}"
                )

                logger.error(
                    f"📦 Full parsed response: "
                    f"{parsed_data}"
                )

                if (
                    invalid_response_count
                    >= self.max_invalid_responses
                ):

                    yield {
                        "type": "error",
                        "stage": "validation",
                        "error": (
                            "Model repeatedly returned "
                            "an invalid agent step."
                        ),
                        "response": parsed_data,
                    }

                    return

                messages.append(
                    {
                        "role": "user",
                        "content": """
Your previous response is invalid.

The "step" field MUST be exactly one of:

"Start"
"Plan"
"Tool"
"Output"

Return ONLY one valid JSON object:

{
    "step": "Start | Plan | Tool | Output",
    "content": "string",
    "tool": "string",
    "input": "string"
}
""",
                    }
                )

                continue

            # Valid response
            invalid_response_count = 0

            # =================================================
            # SAVE ASSISTANT RESPONSE
            # =================================================

            messages.append(
                {
                    "role": "assistant",
                    "content": raw_content,
                }
            )

            # =================================================
            # START
            # =================================================

            if step == "Start":

                logger.info(
                    f"🏁 Starting process: {content}"
                )

                yield {
                    "type": "step",
                    "step": "Start",
                    "content": content,
                }

                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Continue to the next step. "
                            "Return only one JSON step."
                        ),
                    }
                )

                continue

            # =================================================
            # PLAN
            # =================================================

            elif step == "Plan":

                logger.debug(
                    f"🤔 Planning: {content}"
                )

                yield {
                    "type": "step",
                    "step": "Plan",
                    "content": content,
                }

                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Continue to the next step. "
                            "Return only one JSON step."
                        ),
                    }
                )

                continue

            # =================================================
            # TOOL
            # =================================================

            elif step == "Tool":

                # ---------------------------------------------
                # Check tool name
                # ---------------------------------------------

                if not tool_name:

                    logger.error(
                        "❌ Tool step has no tool name."
                    )

                    yield {
                        "type": "error",
                        "stage": "tool",
                        "error": (
                            "Tool step does not contain "
                            "a tool name."
                        ),
                    }

                    return

                # ---------------------------------------------
                # Check tool exists
                # ---------------------------------------------

                if tool_name not in self.available_tools:

                    logger.error(
                        f"❌ Unknown tool requested: "
                        f"{tool_name}"
                    )

                    yield {
                        "type": "error",
                        "stage": "tool",
                        "error": (
                            f"Unknown tool: {tool_name}"
                        ),
                        "available_tools": list(
                            self.available_tools.keys()
                        ),
                    }

                    return

                # ---------------------------------------------
                # Log
                # ---------------------------------------------

                logger.info(
                    f"🛠️ Executing tool: "
                    f"{tool_name}({tool_input})"
                )

                # ---------------------------------------------
                # UI event
                # ---------------------------------------------

                yield {
                    "type": "tool_start",
                    "tool": tool_name,
                    "input": tool_input,
                    "content": content,
                }

                # ---------------------------------------------
                # Execute
                # ---------------------------------------------

                try:

                    tool_function = (
                        self.available_tools[
                            tool_name
                        ]
                    )

                    tool_response = tool_function(
                        tool_input
                    )

                except Exception as e:

                    logger.error(
                        f"❌ Tool '{tool_name}' failed: {e}",
                        exc_info=True,
                    )

                    yield {
                        "type": "tool_error",
                        "tool": tool_name,
                        "input": tool_input,
                        "error": str(e),
                    }

                    return

                # ---------------------------------------------
                # Log result
                # ---------------------------------------------

                logger.info(
                    f"✅ Tool completed: {tool_name}"
                )

                logger.debug(
                    f"🛠️ Tool result: "
                    f"{tool_name}({tool_input}) = "
                    f"{tool_response}"
                )

                # ---------------------------------------------
                # UI event
                # ---------------------------------------------

                yield {
                    "type": "tool_result",
                    "tool": tool_name,
                    "input": tool_input,
                    "result": tool_response,
                }

                # ---------------------------------------------
                # Send result to model
                # ---------------------------------------------

                messages.append(
                    {
                        "role": "user",
                        "content": f"""
Tool execution result:

Tool: {tool_name}

Input:
{tool_input}

Result:
{tool_response}

Use this result to continue solving
the original user request.

Return only the next single JSON step.
""",
                    }
                )

                continue

            # =================================================
            # OUTPUT
            # =================================================

            elif step == "Output":

                logger.info(
                    "✅ Agent processing completed."
                )

                logger.debug(
                    f"🤖 Final output: {content}"
                )

                yield {
                    "type": "output",
                    "content": content,
                }

                return