from config import Settings, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class OpenRouterProvider:
    """
    Provides LLM API from OpenRouter.
    Initializes model, prompt template and output parser.
    Returns LLM Gateway chain. 
    """
    def __init__(self, model_name: str):
        self.app_settings = get_settings()
        self.openrouter_api_key = self.app_settings.OPENROUTER_API_KEY
        self.llm_model_name = model_name
        self.parser = JsonOutputParser()

        self._init_llm()
        self._init_prompt_template()

    def _init_llm(self):
        self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key,
                model=self.llm_model_name,
                temperature=0.2,
            )
    def _init_prompt_template(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
              """Analyze the provided query and context.
Extract ONLY information that is explicitly stated in the context.
Output Requirements:
- Return ONLY a valid JSON object.
- Do NOT include explanations.
- Do NOT include markdown.
- Do NOT include extra text.
- Follow the exact schema provided.
- If a field is not found in the context:
    - set "value" to null
    - set "evidence" to []
Extraction Rules:
- Do NOT infer or guess.
- Do NOT use external knowledge.
- Extract text exactly as written when possible.
- Evidence must come from the provided context only.
- Evidence format:
    {{
    "chunk_id": "<chunk_id>",
    "snippet": "<exact snippet from context>"
    }}
Example:
Input: 
query: regulation name
context:
output schema:
{{"regulation_name": {{ "value": "your extracted answer", "evidence": [{{"chunk_id": "<chunk_number>" , "snippet": "<exact snippet from context>"}}] }}
if field not found in context:
"regulation_name":  {{ "value": null, "evidence": [] }}"""
             ),
            ("human", "query: {query}\ncontext: {context}")
        ])

    def get_llm_gateway_chain(self):
        return self.prompt | self.llm | self.parser
    
    
    
    
    
    
