import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from models.schemas import PatchRequest, PatchResult

def generate_code_patch(req: PatchRequest) -> PatchResult:
    \"\"\"
    Uses Gemini as a Coding Agent to generate a code patch that fixes the failing test.
    \"\"\"
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return PatchResult(
            test_id=req.test_id,
            generated_patch="# Error initializing LLM",
            explanation=str(e)
        )

    prompt = PromptTemplate(
        input_variables=["summary", "code_snippet", "language"],
        template=\"\"\"
        You are an expert Software Engineer and Coding Agent.
        A test has failed with the following root cause: {summary}

        Target Language: {language}
        Application Code Snippet to Fix:
        {code_snippet}

        Instructions:
        1. Write a code patch to fix the issue described in the root cause summary.
        2. Output ONLY the fixed code. Do NOT use markdown code blocks like ```python.
        3. Provide a brief explanation of how the patch fixes the issue.

        Format your response EXACTLY as follows:
        Explanation: [Brief explanation of the fix]
        Code:
        [Your fixed code here]
        \"\"\"
    )

    try:
        chain = prompt | llm
        response = chain.invoke({
            "summary": req.root_cause_summary,
            "code_snippet": req.application_code_snippet,
            "language": req.target_language
        })
        
        text = response.content
        explanation = ""
        code = ""
        
        lines = text.split('\\n')
        in_code_block = False
        
        for line in lines:
            if line.startswith("Explanation:"):
                explanation = line.replace("Explanation:", "").strip()
            elif line.startswith("Code:"):
                in_code_block = True
            elif in_code_block:
                code += line + "\\n"
                
        return PatchResult(
            test_id=req.test_id,
            generated_patch=code.strip(),
            explanation=explanation
        )
    except Exception as e:
        return PatchResult(
            test_id=req.test_id,
            generated_patch="# Patch generation failed",
            explanation=str(e)
        )
