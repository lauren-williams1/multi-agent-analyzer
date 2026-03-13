# orchestrator.py
from agents import DataCollectorAgent, AnalysisAgent, InsightsAgent
from datetime import datetime

class MultiAgentOrchestrator:
    """Coordinates multiple agents in sequential workflow"""
    
    def __init__(self):
        self.data_collector = DataCollectorAgent()
        self.analyzer = AnalysisAgent()
        self.insights_generator = InsightsAgent()
        self.execution_log = []
    
    def run(self, query: str) -> dict:
        """
        Execute multi-agent workflow:
        1. Data Collector identifies needed data
        2. Analysis Agent analyzes the data
        3. Insights Agent generates recommendations
        4. Consolidate results
        """
        
        start_time = datetime.now()
        
        # Step 1: Data Collection
        data_result = self.data_collector.execute(query)
        self.execution_log.append(data_result)
        
        # Step 2: Analysis
        analysis_result = self.analyzer.execute(
            query=query,
            data_collected=data_result["output"]
        )
        self.execution_log.append(analysis_result)
        
        # Step 3: Insights Generation
        insights_result = self.insights_generator.execute(
            query=query,
            analysis=analysis_result["output"]
        )
        self.execution_log.append(insights_result)
        
        # Consolidate
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        report = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": round(execution_time, 2),
            "agents_executed": len(self.execution_log),
            "results": {
                "data_collection": data_result["output"],
                "analysis": analysis_result["output"],
                "insights": insights_result["output"]
            },
            "execution_log": self.execution_log
        }
        
        return report