from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.services.rag_service import ask_question
from app.services.chat_service import (
    create_chat_session,
    add_message,
    get_user_sessions,
    get_chat_messages,
    delete_chat_session
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    document: str | None = None
    history: list[Message] = []
    session_id: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    session_id: int


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Create new session if this is the first message
    session_id = request.session_id

    if session_id is None:

        title = (
            request.question[:50]
            if len(request.question) > 50
            else request.question
        )

        session = create_chat_session(
            db=db,
            user_id=current_user.id,
            title=request.question
        )

        session_id = session.id

    # Save user message
    add_message(
        db=db,
        session_id=session_id,
        role="user",
        content=request.question
    )

    # Generate AI response
    result = ask_question(
        question=request.question,
        document=request.document,
        history=request.history
    )

    # Save assistant response
    add_message(
        db=db,
        session_id=session_id,
        role="assistant",
        content=result["answer"]
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        session_id=session_id
    )
@router.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    sessions = get_user_sessions(
        db=db,
        user_id=current_user.id
    )

    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}")
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    messages = get_chat_messages(
        db=db,
        session_id=session_id
    )

    return [
        {
            "role": m.role,
            "content": m.content
        }
        for m in messages
    ]


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    delete_chat_session(
        db=db,
        session_id=session_id
    )

    return {
        "message": "Chat deleted successfully"
    }