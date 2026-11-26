from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import TestFailureReport, AnalysisResult, PatchRequest, PatchResult
from agents.analyzer import analyze_test_failure
from agents.patcher import generate_code_patch
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="QAAutoHealer API",
    description="API for UiPath Test Cloud to automatically analyze and patch failing tests.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/analyze_failure", response_model=AnalysisResult)
async def analyze_failure_endpoint(report: TestFailureReport):
    \"\"\"
    Endpoint called by UiPath Test Cloud webhook when a test suite fails.
    \"\"\"
    try:
        result = analyze_test_failure(report)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate_patch", response_model=PatchResult)
async def generate_patch_endpoint(req: PatchRequest):
    \"\"\"
    Endpoint to generate a code patch based on the failure analysis.
    \"\"\"
    try:
        result = generate_code_patch(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "QAAutoHealer API is running."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
