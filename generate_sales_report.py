#!/usr/bin/env python3
"""
Script to generate a new sales report for the last 3 days and provide it to the agent for analysis.
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta

# Add the sp-api-agent-system to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sp-api-agent-system'))

from sp_api_agent_system import QueryProcessor

async def generate_and_analyze_sales_report():
    """Generate a new sales report for the last 3 days and analyze it"""
    
    print("🔄 Generating new sales report for the last 3 days...")
    
    # Initialize the query processor
    processor = QueryProcessor()
    
    # Query for sales data for the last 3 days
    query = "Get sales data for the last 3 days and provide detailed insights"
    
    print(f"📊 Processing query: {query}")
    
    try:
        # Process the query using the agent system
        result = processor.process_simple(query)
        
        print("✅ Sales report generated and analyzed successfully!")
        print("\n" + "="*80)
        print("📈 SALES REPORT ANALYSIS")
        print("="*80)
        print(result)
        print("="*80)
        
        return result
        
    except Exception as e:
        print(f"❌ Error generating sales report: {e}")
        return None

if __name__ == "__main__":
    # Run the async function
    result = asyncio.run(generate_and_analyze_sales_report())
    
    if result:
        print("\n🎯 Sales report analysis completed successfully!")
    else:
        print("\n❌ Failed to generate sales report analysis")
        sys.exit(1)

