from sample_data import get_relevant_data
import json

class DataCollectorAgent:
    """Gathers relevant business data based on query"""
    
    def __init__(self):
        self.name = "Data Collector"
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data collection specialist. 
            You have been provided with actual business data below.
            
            Analyze the data and present the most relevant metrics for the user's query.
            Format your response clearly with the key data points.
            
            Available Data:
            {data}
            
            Extract and present the most relevant information for the query.
            """),
            ("user", "{query}")
        ])
    
    def execute(self, query: str) -> dict:
        """Execute data collection agent"""
        # Get relevant sample data based on query
        data_package = get_relevant_data(query)
        
        # Format data as JSON string
        data_json = json.dumps(data_package["data"], indent=2)
        
        chain = self.prompt | self.llm
        response = chain.invoke({
            "query": query,
            "data": data_json
        })
        
        result = {
            "agent": self.name,
            "output": response.content,
            "status": "completed",
            "data_source": data_package["data_source"]
        }
        
        return result