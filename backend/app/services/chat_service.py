from sqlalchemy.orm import Session

from app.models.chat import ChatSession, ChatMessage


def create_chat_session(db: Session, user_id: int, title: str):
    session = ChatSession(
        user_id=user_id,
        title=title[:50]  # Limit title to 50 characters
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def add_message(
    db: Session,
    session_id: int,
    role: str,
    content: str
):
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_session(db: Session, session_id: int):
    return (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )


def get_user_sessions(db: Session, user_id: int):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )
def get_chat_messages(db: Session, session_id: int):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )


def delete_chat_session(db: Session, session_id: int):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if session:
        db.delete(session)
        db.commit()