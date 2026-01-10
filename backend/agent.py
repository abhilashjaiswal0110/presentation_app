"""
Claude Agent SDK integration for presentation manipulation.

Defines tools for creating and editing presentations,
and provides the main agent streaming function.
"""

import uuid
import logging
from typing import Any, AsyncGenerator, Optional
from contextvars import ContextVar

from models import Presentation, Slide, SlideLayout, PendingEdit
from session import PresentationSession, session_manager

logger = logging.getLogger(__name__)

# Context variable for current session (async-safe)
_current_session: ContextVar[Optional[PresentationSession]] = ContextVar(
    'current_session',
    default=None
)


def get_current_session() -> Optional[PresentationSession]:
    """Get the current session from context."""
    return _current_session.get()


def set_current_session(session: Optional[PresentationSession]):
    """Set the current session in context."""
    _current_session.set(session)


# Try to import Claude Agent SDK
try:
    from claude_agent_sdk import (
        ClaudeSDKClient,
        ClaudeAgentOptions,
        tool,
        create_sdk_mcp_server,
        AssistantMessage,
        UserMessage,
        SystemMessage,
        ResultMessage,
        TextBlock,
        ToolUseBlock,
        ToolResultBlock,
    )
    AGENT_SDK_AVAILABLE = True
    AGENT_SDK_ERROR = None
    print("[Agent] Claude Agent SDK loaded successfully")
except ImportError as e:
    AGENT_SDK_AVAILABLE = False
    AGENT_SDK_ERROR = f"{e}. Install with: pip install claude-agent-sdk"
    ClaudeSDKClient = None
    ClaudeAgentOptions = None
    tool = None
    create_sdk_mcp_server = None
    AssistantMessage = None
    UserMessage = None
    SystemMessage = None
    ResultMessage = None
    TextBlock = None
    ToolUseBlock = None
    ToolResultBlock = None
    print(f"[Agent] WARNING: Claude Agent SDK not available: {e}")

# Fallback tool decorator when SDK not available
if not AGENT_SDK_AVAILABLE:
    def tool(name: str, description: str, params: dict):
        def decorator(func):
            func._tool_name = name
            func._tool_description = description
            func._tool_params = params
            return func
        return decorator


# =============================================================================
# TOOL DEFINITIONS
# =============================================================================

@tool("create_presentation", "Create a new presentation", {"title": str})
async def tool_create_presentation(args: dict[str, Any]) -> dict[str, Any]:
    """Create a new presentation with the given title."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}

    title = args.get("title", "Untitled Presentation")
    session.presentation = Presentation(title=title)
    session.pending_edits = []
    session.applied_edits = []

    return {"success": True, "title": title, "slide_count": 0}


@tool("add_slide", "Add a new slide with HTML content", {
    "html": str,
    "position": int,  # Optional - defaults to end
    "layout": str  # Optional - defaults to "blank"
})
async def tool_add_slide(args: dict[str, Any]) -> dict[str, Any]:
    """Add a new slide to the presentation."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation created. Use create_presentation first."}

    html = args.get("html", "")
    position = args.get("position")
    layout_str = args.get("layout", "blank")

    try:
        layout = SlideLayout(layout_str)
    except ValueError:
        layout = SlideLayout.BLANK

    # Determine position
    if position is None or position >= len(session.presentation.slides):
        index = len(session.presentation.slides)
    else:
        index = max(0, position)

    # Create pending edit
    edit = PendingEdit(
        edit_id=str(uuid.uuid4()),
        slide_index=index,
        operation="ADD",
        params={"html": html, "layout": layout.value},
        preview=f"Add slide at position {index + 1}"
    )
    session.pending_edits.append(edit)

    return {"success": True, "slide_index": index, "edit_id": edit.edit_id}


@tool("update_slide", "Update an existing slide's HTML content", {
    "slide_index": int,
    "html": str
})
async def tool_update_slide(args: dict[str, Any]) -> dict[str, Any]:
    """Update the content of an existing slide."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation loaded"}

    slide_index = args.get("slide_index", 0)
    html = args.get("html", "")

    if slide_index < 0 or slide_index >= len(session.presentation.slides):
        return {"error": f"Invalid slide index: {slide_index}"}

    edit = PendingEdit(
        edit_id=str(uuid.uuid4()),
        slide_index=slide_index,
        operation="UPDATE",
        params={"html": html},
        preview=f"Update slide {slide_index + 1}"
    )
    session.pending_edits.append(edit)

    return {"success": True, "slide_index": slide_index, "edit_id": edit.edit_id}


@tool("delete_slide", "Delete a slide from the presentation", {"slide_index": int})
async def tool_delete_slide(args: dict[str, Any]) -> dict[str, Any]:
    """Delete a slide from the presentation."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation loaded"}

    slide_index = args.get("slide_index", 0)

    if slide_index < 0 or slide_index >= len(session.presentation.slides):
        return {"error": f"Invalid slide index: {slide_index}"}

    edit = PendingEdit(
        edit_id=str(uuid.uuid4()),
        slide_index=slide_index,
        operation="DELETE",
        params={},
        preview=f"Delete slide {slide_index + 1}"
    )
    session.pending_edits.append(edit)

    return {"success": True, "slide_index": slide_index, "edit_id": edit.edit_id}


@tool("reorder_slides", "Move a slide to a new position", {
    "from_index": int,
    "to_index": int
})
async def tool_reorder_slides(args: dict[str, Any]) -> dict[str, Any]:
    """Reorder slides in the presentation."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation loaded"}

    from_index = args.get("from_index", 0)
    to_index = args.get("to_index", 0)
    num_slides = len(session.presentation.slides)

    if from_index < 0 or from_index >= num_slides:
        return {"error": f"Invalid from_index: {from_index}"}
    if to_index < 0 or to_index >= num_slides:
        return {"error": f"Invalid to_index: {to_index}"}

    edit = PendingEdit(
        edit_id=str(uuid.uuid4()),
        slide_index=from_index,
        operation="REORDER",
        params={"to_index": to_index},
        preview=f"Move slide {from_index + 1} to position {to_index + 1}"
    )
    session.pending_edits.append(edit)

    return {"success": True, "from_index": from_index, "to_index": to_index}


@tool("list_slides", "List all slides in the presentation", {})
async def tool_list_slides(args: dict[str, Any]) -> dict[str, Any]:
    """List all slides with their index and content preview."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"slides": [], "count": 0}

    import re
    slides = []
    for slide in session.presentation.slides:
        # Create a preview by stripping HTML and truncating
        preview = slide.html[:200].replace('<', ' <').replace('>', '> ')
        preview = re.sub(r'<[^>]+>', '', preview).strip()
        preview = ' '.join(preview.split())[:100]

        slides.append({
            "index": slide.index,
            "layout": slide.layout.value,
            "preview": preview,
            "has_notes": bool(slide.notes)
        })

    return {"slides": slides, "count": len(slides)}


@tool("get_slide", "Get full details of a specific slide", {"slide_index": int})
async def tool_get_slide(args: dict[str, Any]) -> dict[str, Any]:
    """Get the full HTML content and details of a slide."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation loaded"}

    slide_index = args.get("slide_index", 0)

    if slide_index < 0 or slide_index >= len(session.presentation.slides):
        return {"error": f"Invalid slide index: {slide_index}"}

    slide = session.presentation.slides[slide_index]
    return {
        "index": slide.index,
        "html": slide.html,
        "layout": slide.layout.value,
        "notes": slide.notes
    }


@tool("set_theme", "Set the presentation theme (colors, fonts)", {"theme": dict})
async def tool_set_theme(args: dict[str, Any]) -> dict[str, Any]:
    """Set the presentation theme."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation created"}

    theme = args.get("theme", {})
    session.presentation.theme = theme

    return {"success": True, "theme": theme}


@tool("get_pending_edits", "Get all pending edits that haven't been committed", {})
async def tool_get_pending_edits(args: dict[str, Any]) -> dict[str, Any]:
    """Get all pending edits."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}

    edits = [
        {
            "edit_id": e.edit_id,
            "slide_index": e.slide_index,
            "operation": e.operation,
            "preview": e.preview
        }
        for e in session.pending_edits
    ]

    return {"edits": edits, "count": len(edits)}


@tool("commit_edits", "Apply all pending edits to the presentation", {})
async def tool_commit_edits(args: dict[str, Any]) -> dict[str, Any]:
    """Apply all pending edits."""
    session = get_current_session()
    if not session:
        return {"error": "No active session"}
    if not session.presentation:
        return {"error": "No presentation created"}

    applied_count = 0

    for edit in session.pending_edits:
        try:
            if edit.operation == "ADD":
                # Add new slide
                slide = Slide(
                    index=edit.slide_index,
                    html=edit.params.get("html", ""),
                    layout=SlideLayout(edit.params.get("layout", "blank"))
                )
                # Insert at position
                if edit.slide_index >= len(session.presentation.slides):
                    session.presentation.slides.append(slide)
                else:
                    session.presentation.slides.insert(edit.slide_index, slide)
                # Re-index all slides
                for i, s in enumerate(session.presentation.slides):
                    s.index = i

            elif edit.operation == "UPDATE":
                if 0 <= edit.slide_index < len(session.presentation.slides):
                    session.presentation.slides[edit.slide_index].html = edit.params.get("html", "")

            elif edit.operation == "DELETE":
                if 0 <= edit.slide_index < len(session.presentation.slides):
                    del session.presentation.slides[edit.slide_index]
                    # Re-index
                    for i, s in enumerate(session.presentation.slides):
                        s.index = i

            elif edit.operation == "REORDER":
                to_index = edit.params.get("to_index", 0)
                if 0 <= edit.slide_index < len(session.presentation.slides):
                    slide = session.presentation.slides.pop(edit.slide_index)
                    session.presentation.slides.insert(to_index, slide)
                    # Re-index
                    for i, s in enumerate(session.presentation.slides):
                        s.index = i

            session.applied_edits.append(edit.to_dict())
            applied_count += 1

        except Exception as e:
            logger.error(f"Error applying edit {edit.edit_id}: {e}")

    # Clear pending edits
    session.pending_edits = []

    # Save session
    session_manager.save_session(session)

    return {
        "success": True,
        "applied_count": applied_count,
        "total_slides": len(session.presentation.slides)
    }


# =============================================================================
# TOOL REGISTRATION
# =============================================================================

PRESENTATION_TOOLS = [
    tool_create_presentation,
    tool_add_slide,
    tool_update_slide,
    tool_delete_slide,
    tool_reorder_slides,
    tool_list_slides,
    tool_get_slide,
    tool_set_theme,
    tool_get_pending_edits,
    tool_commit_edits,
]

# Tool name to function mapping for fallback mode
TOOL_MAP = {func._tool_name: func for func in PRESENTATION_TOOLS if hasattr(func, '_tool_name')}


# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

SYSTEM_PROMPT_NEW = """You are a presentation creation assistant. Create professional slides using HTML.

WORKFLOW:
1. Use create_presentation to start a new presentation with a title
2. Use add_slide to add slides with HTML content
3. Use commit_edits to finalize and save all changes

HTML GUIDELINES:
- Use semantic HTML (h1, h2, p, ul, li)
- Use inline styles for positioning and colors
- Keep text concise - bullet points, not paragraphs
- Slide dimensions: 960x540px (16:9 aspect ratio)

EXAMPLE SLIDE HTML:
<div style="padding: 40px; font-family: Arial, sans-serif;">
  <h1 style="color: #1a73e8; margin-bottom: 20px;">Slide Title</h1>
  <ul style="font-size: 24px; line-height: 1.6;">
    <li>First key point</li>
    <li>Second key point</li>
    <li>Third key point</li>
  </ul>
</div>

DESIGN PRINCIPLES:
- One main idea per slide
- Consistent color scheme throughout
- Use contrast for readability
- Maximum 5-6 bullet points per slide
- Use visual hierarchy with font sizes

You can call add_slide multiple times in parallel for efficiency when creating multiple slides.
Always call commit_edits when done to save the presentation."""

SYSTEM_PROMPT_CONTINUATION = """You are editing an existing presentation.

CRITICAL: Only modify slides the user specifically requests.
DO NOT change slides that weren't mentioned unless explicitly asked.

WORKFLOW:
1. Use list_slides to see all current slides
2. Use get_slide to see details of specific slides
3. Use update_slide or add_slide to make changes
4. Use commit_edits to save changes

Use list_slides first to understand the current state before making any changes."""


# =============================================================================
# MESSAGE SERIALIZATION
# =============================================================================

def _get_friendly_tool_description(tool_name: str, tool_input: dict) -> str:
    """Convert a tool call into a user-friendly description."""
    if not isinstance(tool_input, dict):
        return None

    if "create_presentation" in tool_name:
        title = tool_input.get("title", "Untitled")
        return f"Creating presentation: {title}"
    elif "add_slide" in tool_name:
        return "Adding a new slide..."
    elif "update_slide" in tool_name:
        idx = tool_input.get("slide_index", 0)
        return f"Updating slide {idx + 1}..."
    elif "delete_slide" in tool_name:
        idx = tool_input.get("slide_index", 0)
        return f"Deleting slide {idx + 1}..."
    elif "list_slides" in tool_name:
        return "Listing all slides..."
    elif "get_slide" in tool_name:
        idx = tool_input.get("slide_index", 0)
        return f"Getting slide {idx + 1} details..."
    elif "commit_edits" in tool_name:
        return "Saving changes..."
    elif "set_theme" in tool_name:
        return "Setting presentation theme..."

    return None


def _serialize_message(message) -> dict:
    """Convert an agent message to a JSON-serializable dict."""
    msg_dict = {"type": "unknown"}

    if AssistantMessage and isinstance(message, AssistantMessage):
        msg_dict["type"] = "assistant"
        texts = []
        tool_calls = []

        for block in message.content:
            if TextBlock and isinstance(block, TextBlock):
                texts.append(block.text)
            elif ToolUseBlock and isinstance(block, ToolUseBlock):
                tool_name = getattr(block, "name", "unknown")
                tool_input = getattr(block, "input", {})
                friendly_desc = _get_friendly_tool_description(tool_name, tool_input)

                tool_calls.append({
                    "name": tool_name,
                    "input": tool_input if isinstance(tool_input, dict) else str(tool_input)[:200],
                    "friendly": friendly_desc
                })

        if texts:
            msg_dict["text"] = " ".join(texts)
        if tool_calls:
            msg_dict["tool_calls"] = tool_calls
            msg_dict["type"] = "tool_use"
            friendly_msgs = [tc["friendly"] for tc in tool_calls if tc.get("friendly")]
            if friendly_msgs:
                msg_dict["friendly"] = friendly_msgs

    elif UserMessage and isinstance(message, UserMessage):
        msg_dict["type"] = "user"
        if hasattr(message, "content"):
            msg_dict["content"] = str(message.content)[:500]

    elif SystemMessage and isinstance(message, SystemMessage):
        msg_dict["type"] = "system"
        if hasattr(message, "content"):
            msg_dict["content"] = str(message.content)[:500]

    elif ResultMessage and isinstance(message, ResultMessage):
        msg_dict["type"] = "result"
        # Extract session_id from ResultMessage
        if hasattr(message, "session_id"):
            msg_dict["session_id"] = message.session_id

    return msg_dict


# =============================================================================
# AGENT OPTIONS
# =============================================================================

def _create_agent_options(
    session: PresentationSession,
    is_continuation: bool = False,
    resume_session_id: Optional[str] = None,
) -> "ClaudeAgentOptions":
    """Create agent options with presentation tools."""
    session.is_continuation = is_continuation

    # Create in-process MCP server with our tools
    pres_server = create_sdk_mcp_server(
        name="presentation",
        version="1.0.0",
        tools=PRESENTATION_TOOLS
    )

    # Use different system prompt for continuations
    system_prompt = SYSTEM_PROMPT_CONTINUATION if is_continuation else SYSTEM_PROMPT_NEW

    # Add context files to prompt if available
    if session.context_files:
        context_text = "\n\n".join([
            f"=== {f['filename']} ===\n{f['text']}"
            for f in session.context_files if f.get('text')
        ])
        if context_text:
            system_prompt += f"\n\nCONTEXT FILES:\n{context_text}"

    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        mcp_servers={"presentation": pres_server},
        allowed_tools=[
            "mcp__presentation__create_presentation",
            "mcp__presentation__add_slide",
            "mcp__presentation__update_slide",
            "mcp__presentation__delete_slide",
            "mcp__presentation__reorder_slides",
            "mcp__presentation__list_slides",
            "mcp__presentation__get_slide",
            "mcp__presentation__set_theme",
            "mcp__presentation__get_pending_edits",
            "mcp__presentation__commit_edits",
        ],
        resume=resume_session_id,
    )


# =============================================================================
# AGENT STREAMING
# =============================================================================

async def run_agent_stream(
    instructions: str,
    is_continuation: bool = False,
    resume_session_id: Optional[str] = None,
    user_session_id: Optional[str] = None,
    context_files: Optional[list[dict]] = None,
) -> AsyncGenerator[dict, None]:
    """
    Run the agent and stream results.

    Args:
        instructions: User instructions
        is_continuation: Whether this is continuing a previous session
        resume_session_id: Claude session ID to resume (for multi-turn)
        user_session_id: Backend session ID
        context_files: Parsed context files

    Yields:
        SSE event dictionaries
    """
    print(f"[Agent Stream] Starting with is_continuation={is_continuation}, "
          f"resume_session_id={resume_session_id}, user_session_id={user_session_id}")

    if not AGENT_SDK_AVAILABLE:
        print(f"[Agent Stream] SDK not available: {AGENT_SDK_ERROR}")
        yield {"type": "error", "error": f"Claude Agent SDK not available: {AGENT_SDK_ERROR}"}
        return

    # Get or create session
    session = session_manager.get_or_create_session(user_session_id)

    if context_files:
        session.context_files = context_files

    set_current_session(session)

    yield {"type": "init", "message": "Starting agent...", "session_id": session.session_id}
    yield {"type": "status", "message": "Connecting to Claude Agent SDK..."}

    options = _create_agent_options(session, is_continuation, resume_session_id)
    message_count = 0
    result_text = ""
    agent_session_id = None  # Will be extracted from ResultMessage

    try:
        async with ClaudeSDKClient(options=options) as client:
            print(f"[Agent Stream] Connected, sending query...")
            yield {"type": "status", "message": "Agent connected, processing..."}

            await client.query(instructions)

            async for message in client.receive_response():
                message_count += 1
                msg_type = type(message).__name__

                # Log message
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            result_text = block.text
                            preview = result_text[:200].replace('\n', ' ')
                            print(f"[Agent Stream] #{message_count} {msg_type}: {preview}...")
                        else:
                            block_type = type(block).__name__
                            print(f"[Agent Stream] #{message_count} {msg_type}/{block_type}")
                elif ResultMessage and isinstance(message, ResultMessage):
                    # Extract session_id from ResultMessage for multi-turn support
                    agent_session_id = getattr(message, 'session_id', None)
                    print(f"[Agent Stream] #{message_count} {msg_type}: session_id={agent_session_id}")
                else:
                    print(f"[Agent Stream] #{message_count} {msg_type}")

                yield _serialize_message(message)

    except Exception as e:
        print(f"[Agent Stream] Error: {e}")
        import traceback
        traceback.print_exc()
        yield {"type": "error", "error": f"Agent error: {str(e)}"}
        return

    finally:
        set_current_session(None)

    # Save session state
    session.claude_session_id = agent_session_id
    session_manager.save_session(session)

    # Yield final summary
    yield {
        "type": "complete",
        "success": True,
        "result": result_text,
        "message_count": message_count,
        "session_id": agent_session_id,
        "user_session_id": session.session_id,
        "slide_count": len(session.presentation.slides) if session.presentation else 0
    }
