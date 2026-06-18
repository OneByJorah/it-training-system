from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ORM Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String)
    telegram_id = Column(String)
    current_level = Column(String)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    raw_transcript = Column(Text)
    summary = Column(Text)
    duration = Column(Integer)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, default="CURRENT_TIMESTAMP")


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)


class VideoSkill(Base):
    __tablename__ = "video_skills"
    video_id = Column(Integer, ForeignKey("videos.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)


class UserSkill(Base):
    __tablename__ = "user_skills"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    proficiency_score = Column(Float)


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    title = Column(String)
    questions_json = Column(Text)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    text = Column(Text)
    options_json = Column(Text)
    correct_index = Column(Integer)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Float)
    completed_at = Column(String, default="CURRENT_TIMESTAMP")


class LearningPath(Base):
    __tablename__ = "learning_paths"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    status = Column(String)


class LearningPathItem(Base):
    __tablename__ = "learning_path_items"
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"))
    item_order = Column(Integer)
    item_type = Column(String)
    item_id = Column(Integer)
    completed = Column(Integer, default=0)


class UserEvent(Base):
    __tablename__ = "user_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String)
    metadata_json = Column(Text)
    created_at = Column(String, default="CURRENT_TIMESTAMP")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="IT Training API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/users")
def create_user(name: str, telegram_id: str | None = None, role: str | None = None, db: Session = Depends(get_db)):
    user = User(name=name, telegram_id=telegram_id, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/videos/upload")
async def upload_video(title: str, uploaded_by: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = f"/data/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    video = Video(title=title, file_path=path, uploaded_by=uploaded_by)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


@app.get("/videos")
def list_videos(db: Session = Depends(get_db)):
    return db.query(Video).all()


@app.get("/quizzes")
def list_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).all()


@app.post("/learning-paths")
def create_path(user_id: int, title: str, description: str | None = None, db: Session = Depends(get_db)):
    path = LearningPath(user_id=user_id, title=title, description=description, status="active")
    db.add(path)
    db.commit()
    db.refresh(path)
    return path
