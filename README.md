# Agentic QA Auto-Healer

**Track:** Track 3: UiPath Test Cloud
**Hackathon:** UiPath AgentHack

## 🚀 What the Project Does

The Agentic QA Auto-Healer re-imagines software testing by creating self-healing test suites. Instead of engineers spending hours debugging why an automated test failed in UiPath Test Cloud, this solution automatically intercepts the failure, analyzes the stack trace, and writes a code patch to fix it.

### The Workflow:
1. **Detection:** A test fails in UiPath Test Cloud. A webhook triggers our FastAPI backend.
2. **Analysis:** A LangChain/Gemini analyzer agent reviews the error message and stack trace to determine the root cause (e.g., "The CSS selector for the login button changed").
3. **Patch Generation (Coding Agent Bonus!):** Our Gemini Coding Agent generates the exact code patch required to fix the test script or the underlying application code.
4. **Human-in-the-Loop:** A QA Engineer reviews the generated patch in UiPath Action Center.
5. **Resolution:** Upon approval, the patch is merged, and UiPath Test Cloud automatically re-runs the suite to verify the fix.

## 💻 Setup Instructions & Prerequisites

### Prerequisites
- Python 3.10+
- Google Gemini API Key (`GOOGLE_API_KEY`)

### Local Backend Setup (Agents)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8002
   ```
   The API will be available at `http://localhost:8002` and Swagger docs at `http://localhost:8002/docs`.

### UiPath Integration
- Connect **UiPath Test Cloud** webhooks to point to `POST http://localhost:8002/api/v1/analyze_failure`.
- Once the analysis is complete, configure an API Workflow to hit the `/generate_patch` endpoint, passing the analysis results and the broken code snippet.
