from schema import Output_format
from openai import RateLimitError, NotFoundError, AuthenticationError, BadRequestError
from pydantic import ValidationError
from logger import logger


class ModelRouter:
    def __init__(self, fallback_models):
        self.fallback_models = fallback_models
        self.current_index = 0

    def call(self, messages):
        current_index = 0
        while current_index < len(self.fallback_models):
            entry = self.fallback_models[self.current_index]
            model_name = entry["model"]
            client = entry["get_client"]()

            try:
                # response = client.chat.completions.parse(
                #     model=model_name,
                #     response_format=Output_format,
                #     messages=messages,
                # )
                response = client.chat.completions.create(
                    model=model_name,
                    response_format={"type": "json_object"},
                    messages=messages,
                )

                # if response.choices[0].message.parsed is None:
                #     refusal = getattr(response.choices[0].message, "refusal", None)
                #     logger.warning(
                #         f"{model_name} returned no parseable output "
                #         f"(refusal: {refusal!r}), switching to next fallback model."
                #     )
                #     self.current_index += 1
                #     continue

                return response
            except (RateLimitError, NotFoundError, ValidationError) as e:
                print(
                    f"{model_name} unavailable ({type(e).__name__}), "
                    f"switching to next fallback model."
                )
                logger.warning(
                    f"{model_name} unavailable ({type(e).__name__}), "
                    f"switching to next fallback model."
                )
                current_index += 1
            except AuthenticationError:
                logger.error(f"Invalid API key for {model_name}. Check your .env file.")
                raise SystemExit(
                    f"Invalid API key for {model_name}. Check your .env file."
                )
            except BadRequestError as e:
                print( f"{model_name} doesn't support structured outputs, switching to next fallback model."
                                    )
                if "response_format" in str(e) or "json_schema" in str(e):
                    logger.warning(
                        f"{model_name} doesn't support structured outputs, switching to next fallback model."
                    )
                    current_index += 1
                else:
                    logger.error(f"Malformed request to {model_name}: {e}")
                    raise
        logger.error("All fallback models exhausted — no provider available.")
        raise RuntimeError("All fallback models exhausted — no provider available.")
