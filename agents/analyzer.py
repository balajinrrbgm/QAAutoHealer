import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from models.schemas import TestFailureReport, AnalysisResult

def analyze_test_failure(report: TestFailureReport) -> AnalysisResult:
    \"\"\"
    Uses LangChain to analyze a test failure from UiPath Test Cloud.
    \"\"\"
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return AnalysisResult(
            test_id=report.test_id,
            root_cause_summary="Error running analysis.",
            is_test_flaky=False,
            recommended_fix_type="unknown"
        )

    prompt = PromptTemplate(
        input_variables=["test_name", "error_message", "stack_trace"],
        template=\"\"\"
        You are an expert QA Automation Engineer.
        Analyze the following automated test failure:

        Test Name: {test_name}
        Error Message: {error_message}
        Stack Trace:
        {stack_trace}

        Instructions:
        1. Summarize the root cause of the failure.
        2. Determine if the test is likely flaky (e.g., timeout, network blip) or a hard failure.
        3. Recommend a fix type: 'update_test_selector', 'fix_app_logic', or 'increase_timeout'.

        Format your response EXACTLY as follows:
        Summary: [Your root cause summary]
        Flaky: [True or False]
        FixType: [Recommended fix type]
        \"\"\"
    )

    try:
        chain = prompt | llm
        response = chain.invoke({
            "test_name": report.test_name,
            "error_message": report.error_message,
            "stack_trace": report.stack_trace
        })
        
        text = response.content
        summary = ""
        is_flaky = False
        fix_type = "update_test_selector"
        
        for line in text.split('\\n'):
            if line.startswith("Summary:"):
                summary = line.replace("Summary:", "").strip()
            elif line.startswith("Flaky:"):
                val = line.replace("Flaky:", "").strip().lower()
                is_flaky = val == "true"
            elif line.startswith("FixType:"):
                fix_type = line.replace("FixType:", "").strip()
                
        return AnalysisResult(
            test_id=report.test_id,
            root_cause_summary=summary,
            is_test_flaky=is_flaky,
            recommended_fix_type=fix_type
        )
    except Exception as e:
        return AnalysisResult(
            test_id=report.test_id,
            root_cause_summary=f"Analysis failed: {e}",
            is_test_flaky=False,
            recommended_fix_type="unknown"
        )
