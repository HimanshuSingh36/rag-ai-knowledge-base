from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from tools import AVAILABLE_TOOL_NAMES


class Output_format(BaseModel):
    step: Literal["Start", "Plan", "Tool", "Output"]
    content: Optional[str] = None
    tool: Optional[str] = None
    input: Optional[str] = None

    @field_validator("tool")
    @classmethod
    def validate_available_tools(cls,value):
        if value=="":
            return None
        if value is not None and value not in AVAILABLE_TOOL_NAMES:
            raise ValueError(f"Unknown tool '{value}'. Valid tools: {sorted(AVAILABLE_TOOL_NAMES)}")
        return value
