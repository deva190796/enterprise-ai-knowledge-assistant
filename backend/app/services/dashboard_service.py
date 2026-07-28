from sqlalchemy.orm import Session

from app.models.user import User
from app.models.document import Document
from app.models.chat import ChatSession, ChatMessage


def get_dashboard_stats(db: Session):

    recent_documents = (
        db.query(Document)
        .order_by(Document.id.desc())
        .limit(5)
        .all()
    )

    recent_chats = (
        db.query(ChatSession)
        .order_by(ChatSession.id.desc())
        .limit(5)
        .all()
    )

    return {
        "total_users": db.query(User).count(),
        "total_documents": db.query(Document).count(),
        "total_chat_sessions": db.query(ChatSession).count(),
        "total_messages": db.query(ChatMessage).count(),

        "recent_documents": [
            {
                "id": doc.id,
                "name": doc.original_filename
            }
            for doc in recent_documents
        ],

        "recent_chats": [
            {
                "id": chat.id,
                "title": chat.title
            }
            for chat in recent_chats
        ]
    }