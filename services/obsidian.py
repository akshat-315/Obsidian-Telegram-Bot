from typing import Optional
from pydantic import BaseModel

class ObsidianFleetingTemplate(BaseModel):
    title: str
    content: Optional[str] = None

def parse_message(message) -> ObsidianFleetingTemplate:
    # First line is for title, rest is for content(optional)
    lines = message.split("\n")
    title = lines[0]
    content = "\n".join(lines[1:]).lstrip("\n") or None
    return ObsidianFleetingTemplate(title=title, content=content)