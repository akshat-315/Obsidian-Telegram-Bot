import re
import logging
from datetime import date
from typing import Optional
from pydantic import BaseModel
from services.github import get_installation_token, create_file
from config import settings

logger = logging.getLogger("obsidian_workflow_bot")

FLEETING_DIR = settings.FLEETING_DIR


class ObsidianFleetingTemplate(BaseModel):
    title: str
    content: Optional[str] = None


def parse_message(message) -> ObsidianFleetingTemplate:
    # First line is for title, rest is for content(optional)
    lines = message.split("\n")
    title = lines[0]
    content = "\n".join(lines[1:]).lstrip("\n") or None
    return ObsidianFleetingTemplate(title=title, content=content)


def build_note_content(note: ObsidianFleetingTemplate) -> str:
    today = date.today().isoformat()
    frontmatter = f"---\ntags:\n  - fleeting\ndate: {today}\n---"
    if note.content:
        return f"{frontmatter}\n\n{note.content}"
    return frontmatter


def create_fleeting_note(note: ObsidianFleetingTemplate) -> None:
    token = get_installation_token()
    content = build_note_content(note)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", note.title).strip()
    path = f"{FLEETING_DIR}/{safe_title}.md"
    create_file(token, path, content, message=f"Add fleeting note: {safe_title}")
    logger.info(f"Fleeting note created: {path}")