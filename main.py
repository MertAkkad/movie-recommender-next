
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import router as search_router  # Adjust if necessary

app = FastAPI()

# Allow frontend requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ask-a-movie-p8cxfvayz-mertakkads-projects.vercel.app"],  # Adjust based on deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)


@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running"}
