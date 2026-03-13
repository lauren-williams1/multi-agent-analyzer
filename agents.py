# agents.py
from langchain_openai import ChatOpenAI
#from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import os

# Initialize LLM
def get_llm():
    """Initialize OpenAI LLM"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=api_key
    )

class DataCollectorAgent:
    """Gathers relevant business data based on query"""
    
    def __init__(self):
        self.name = "Data Collector"
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data collection specialist. 
            Given a business analysis request, identify what data would be needed.
            Return a structured list of data points to collect.
            
            Format your response as:
            DATA NEEDED:
            - [data point 1]
            - [data point 2]
            - [data point 3]
            
            Be specific and business-focused.
            """),
            ("user", "{query}")
        ])
    
    def execute(self, query: str) -> dict:
        """Execute data collection agent"""
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})
        
        return {
            "agent": self.name,
            "output": response.content,
            "status": "completed"
        }


class AnalysisAgent:
    """Analyzes data and identifies trends/patterns"""
    
    def __init__(self):
        self.name = "Analysis Agent"
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a business data analyst.
            Given collected data points, perform analysis and identify:
            1. Key trends
            2. Patterns
            3. Anomalies
            4. Correlations
            
            Be specific and quantitative where possible.
            """),
            ("user", """Business Query: {query}
            
            Data Collected: {data_collected}
            
            Perform detailed analysis:""")
        ])
    
    def execute(self, query: str, data_collected: str) -> dict:
        """Execute analysis agent"""
        chain = self.prompt | self.llm
        response = chain.invoke({
            "query": query,
            "data_collected": data_collected
        })
        
        return {
            "agent": self.name,
            "output": response.content,
            "status": "completed"
        }


class InsightsAgent:
    """Generates actionable recommendations"""
    
    def __init__(self):
        self.name = "Insights Agent"
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a business strategy consultant.
            Given data analysis, provide:
            1. Top 3 actionable insights
            2. Specific recommendations
            3. Potential risks to consider
            4. Next steps
            
            Be concrete and business-focused.
            """),
            ("user", """Business Query: {query}
            
            Analysis Results: {analysis}
            
            Generate strategic insights:""")
        ])
    
    def execute(self, query: str, analysis: str) -> dict:
        """Execute insights agent"""
        chain = self.prompt | self.llm
        response = chain.invoke({
            "query": query,
            "analysis": analysis
        })
        
        return {
            "agent": self.name,
            "output": response.content,
            "status": "completed"
        }