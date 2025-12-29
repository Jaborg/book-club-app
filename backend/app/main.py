from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routes.books import router as books_router
from app.routes.members import router as members_router
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(members_router)
