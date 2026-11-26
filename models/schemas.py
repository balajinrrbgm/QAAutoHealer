from pydantic import BaseModel, Field

class TestFailureReport(BaseModel):
    test_id: str
    test_name: str
    error_message: str
    stack_trace: str
    application_code_snippet: str = Field(default="")

class AnalysisResult(BaseModel):
    test_id: str
    root_cause_summary: str
    is_test_flaky: bool
    recommended_fix_type: str = Field(..., description="e.g., 'update_test_selector', 'fix_app_logic'")

class PatchRequest(BaseModel):
    test_id: str
    root_cause_summary: str
    application_code_snippet: str
    target_language: str = Field(default="python")

class PatchResult(BaseModel):
    test_id: str
    generated_patch: str
    explanation: str
