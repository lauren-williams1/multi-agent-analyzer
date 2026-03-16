# streamlit app

# main.py
import streamlit as st
from orchestrator import MultiAgentOrchestrator
import os

# Page config
st.set_page_config(
    page_title="Multi-Agent Business Analyzer",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 Multi-Agent Business Analyzer")
st.markdown("**AI-powered data analysis using specialized agents**")
st.markdown("---")

# Sidebar info
with st.sidebar:
    st.header("About")
    st.write("""
    This system uses 3 specialized AI agents:
    
    **📥 Data Collector**
    Identifies needed data points
    
    **📊 Analysis Agent**
    Analyzes trends and patterns
    
    **💡 Insights Agent**
    Generates recommendations
    """)
    
    st.markdown("---")
    st.write("Built with LangChain & OpenAI GPT-3.5")

# Main content
st.subheader("Enter Your Business Analysis Request")

# Example queries
with st.expander("💡 Example Queries"):
    st.write("""
    - Analyze Q4 sales trends for e-commerce business
    - Evaluate customer churn patterns for SaaS company
    - Analyze marketing campaign ROI for retail brand
    - Identify growth opportunities for B2B product
    """)

# Input
query = st.text_area(
    "What would you like to analyze?",
    placeholder="Example: Analyze Q4 sales trends for e-commerce business",
    height=100,
    key="query_input"
)

# Analyze button
if st.button("🚀 Analyze with Multi-Agent System", type="primary"):
    if query:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            st.error("❌ OPENAI_API_KEY not found. Please add it in Streamlit secrets.")
            st.stop()
        
        # Run analysis
        with st.spinner("🤖 Agents are working on your analysis..."):
            try:
                orchestrator = MultiAgentOrchestrator()
                report = orchestrator.run(query)
                
                # Show success
                st.success(f"✅ Analysis complete! Execution time: {report['execution_time_seconds']}s")
                
                # Show metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("⏱️ Execution Time", f"{report['execution_time_seconds']}s")
                with col2:
                    st.metric("🤖 Agents Used", report['agents_executed'])
                
                st.markdown("---")
                
                # Show results in tabs
                tab1, tab2, tab3 = st.tabs(["📥 Data Collection", "📊 Analysis", "💡 Insights"])
                
                with tab1:
                    st.markdown("### Data Collection Phase")
                    st.write(report['results']['data_collection'])
                
                with tab2:
                    st.markdown("### Analysis Phase")
                    st.write(report['results']['analysis'])
                
                with tab3:
                    st.markdown("### Insights & Recommendations")
                    st.write(report['results']['insights'])
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.write("Please check your OpenAI API key and try again.")
    else:
        st.warning("⚠️ Please enter a query above")


        # Show success with safety indicators
        if report.get("human_review", {}).get("required"):
                    st.warning(f"⚠️ Human review recommended: {report['human_review']['reason']}")
        else:
            st.success(f"✅ Analysis complete! Execution time: {report['execution_time_seconds']}s")
                    
                # Show metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏱️ Time", f"{report['execution_time_seconds']}s")
        with col2:
            st.metric("🤖 Agents", report['agents_executed'])
        with col3:
            conf = report['safety']['confidence_scores']['average']
            st.metric("🎯 Confidence", f"{conf:.0%}")
        with col4:
            errors = report['reliability']['error_count']
            st.metric("❌ Errors", errors)
                
                # Safety warnings
        if report['safety']['warnings']:
            with st.expander("⚠️ Safety Warnings", expanded=True):
                for warning in report['safety']['warnings']:
                        st.warning(warning)
                
            st.markdown("---")
                
                # Show results in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📥 Data Collection", 
            "📊 Analysis", 
            "💡 Insights",
            "🔍 Execution Details"
        ])
                
        with tab1:
            st.markdown("### Data Collection Phase")
            conf = report['safety']['confidence_scores']['data_collection']
            st.caption(f"Confidence: {conf:.0%}")
            st.write(report['results']['data_collection'])
                
        with tab2:
            st.markdown("### Analysis Phase")
            conf = report['safety']['confidence_scores']['analysis']
            st.caption(f"Confidence: {conf:.0%}")
            st.write(report['results']['analysis'])
                
        with tab3:
            st.markdown("### Insights & Recommendations")
            conf = report['safety']['confidence_scores']['insights']
            st.caption(f"Confidence: {conf:.0%}")
            st.write(report['results']['insights'])
                
        with tab4:
            st.markdown("### Execution Details")
                    
            st.write("**Safety Checks:**")
            st.json(report['safety'])
                    
            st.write("**Reliability Metrics:**")
            st.json(report['reliability'])
                    
            st.write("**Human Review Status:**")
            st.json(report['human_review'])

# Footer
st.markdown("---")
st.caption("Multi-Agent Business Analyzer | Built with Streamlit & LangChain")



