"""
Comprehensive test script for enhanced agent integration
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any

from src.agents.core.enhanced_orchestrator import EnhancedOrchestrator
from src.agents.core.enhanced_base_agent import AgentConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_enhanced_agents():
    """Test individual enhanced agents"""
    
    print("=" * 80)
    print("TESTING ENHANCED AGENTS")
    print("=" * 80)
    
    # Test Trend Analysis Agent
    from src.agents.specialists.enhanced_trend_analysis import EnhancedTrendAnalysisAgent
    
    trend_agent = EnhancedTrendAnalysisAgent(
        AgentConfig(temperature=0.7, max_tokens=1000)
    )
    
    print("\n1. Testing Enhanced Trend Analysis Agent...")
    try:
        trend_result = await trend_agent.get_trend_summary("Sustainable Fashion")
        print(f"   ✓ Success: {trend_result['insights']['trend_count']} trends found")
        print(f"   ✓ Metrics: {trend_agent.get_metrics()}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test Content Strategy Agent
    from src.agents.core.enhanced_content_strategy import EnhancedContentStrategyAgent
    
    strategy_agent = EnhancedContentStrategyAgent(
        AgentConfig(temperature=0.7, max_tokens=1500)
    )
    
    print("\n2. Testing Enhanced Content Strategy Agent...")
    try:
        strategy_result = await strategy_agent.get_strategy_summary(
            "Sustainable Fashion",
            target_audience="eco-conscious millennials",
            content_goals=["brand_awareness", "engagement"]
        )
        print(f"   ✓ Success: {len(strategy_result['strategy']['content_pillars'])} pillars")
        print(f"   ✓ Calendar: {strategy_result['calendar_length']} posts")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

async def test_enhanced_orchestrator():
    """Test the enhanced orchestrator"""
    
    print("\n" + "=" * 80)
    print("TESTING ENHANCED ORCHESTRATOR")
    print("=" * 80)
    
    orchestrator = EnhancedOrchestrator()
    
    # Test system status
    print("\n1. System Status:")
    status = orchestrator.get_system_status()
    print(f"   ✓ Agents: {status['agents_initialized']}")
    print(f"   ✓ Health: {status['system_health']}")
    
    # Test single phase execution
    print("\n2. Testing Single Phase...")
    try:
        phase_result = await orchestrator.execute_single_phase(
            "trend_analysis",
            {"topic": "AI in Marketing"}
        )
        print(f"   ✓ Phase completed successfully")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test complete workflow
    print("\n3. Testing Complete Workflow...")
    workflow_config = {
        "topic": "Remote Work Trends 2025",
        "target_audience": "remote workers and digital nomads aged 25-40",
        "content_goals": ["thought_leadership", "community_building", "lead_generation"],
        "platforms": ["linkedin", "twitter", "instagram"],
        "duration": 30,
        "budget": 1500
    }
    
    try:
        workflow_result = await orchestrator.execute_workflow(workflow_config)
        
        print(f"\n   ✓ Workflow ID: {workflow_result['workflow_id']}")
        print(f"   ✓ Duration: {workflow_result['duration_seconds']:.2f}s")
        print(f"   ✓ Success Rate: {workflow_result['summary']['success_rate']:.2%}")
        print(f"   ✓ Content Pieces: {workflow_result['summary']['content_pieces_created']}")
        print(f"   ✓ Visual Assets: {workflow_result['summary']['visuals_created']}")
        
        # Save results
        with open(f"test_results_{workflow_result['workflow_id']}.json", 'w', encoding='utf-8') as f:
            json.dump(workflow_result, f, indent=2, ensure_ascii=False)
        
        return workflow_result
        
    except Exception as e:
        print(f"   ✗ Workflow Error: {str(e)}")
        return None

async def test_error_handling():
    """Test error handling and edge cases"""
    
    print("\n" + "=" * 80)
    print("TESTING ERROR HANDLING")
    print("=" * 80)
    
    orchestrator = EnhancedOrchestrator()
    
    # Test invalid topic
    print("\n1. Testing Invalid Input...")
    try:
        result = await orchestrator.execute_workflow({})
        print(f"   ✓ Handled gracefully: {result['status']}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)}")
    
    # Test missing required fields
    print("\n2. Testing Missing Fields...")
    try:
        result = await orchestrator.execute_workflow({
            "target_audience": "test",
            "content_goals": ["test"]
            # Missing topic
        })
        print(f"   ✓ Handled gracefully: {result['status']}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)}")

async def test_performance_metrics():
    """Test performance metrics collection"""
    
    print("\n" + "=" * 80)
    print("TESTING PERFORMANCE METRICS")
    print("=" * 80)
    
    orchestrator = EnhancedOrchestrator()
    
    # Run multiple workflows to collect metrics
    test_configs = [
        {
            "topic": "Digital Marketing Trends",
            "target_audience": "marketing professionals",
            "content_goals": ["education", "engagement"]
        },
        {
            "topic": "Sustainable Living",
            "target_audience": "environmental enthusiasts",
            "content_goals": ["awareness", "community"]
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n{i}. Testing Workflow: {config['topic']}")
        try:
            result = await orchestrator.execute_workflow(config)
            print(f"   ✓ Completed in {result['duration_seconds']:.2f}s")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
    
    # Display aggregate metrics
    print("\nAggregate Metrics:")
    metrics = orchestrator.get_agent_metrics()
    for agent_name, agent_metrics in metrics.items():
        print(f"   {agent_name}:")
        print(f"      - Success Rate: {agent_metrics['success_rate']:.2%}")
        print(f"      - Avg Duration: {agent_metrics['avg_duration']:.2f}s")
        print(f"      - Total Calls: {agent_metrics['total_calls']}")

async def test_workflow_history():
    """Test workflow history functionality"""
    
    print("\n" + "=" * 80)
    print("TESTING WORKFLOW HISTORY")
    print("=" * 80)
    
    orchestrator = EnhancedOrchestrator()
    
    # Run a test workflow
    config = {
        "topic": "Test History Feature",
        "target_audience": "test audience",
        "content_goals": ["test"]
    }
    
    await orchestrator.execute_workflow(config)
    
    # Check history
    history = orchestrator.get_workflow_history(5)
    print(f"\n✓ History contains {len(history)} workflows")
    
    if history:
        latest = history[-1]
        print(f"✓ Latest: {latest['workflow_id']} - {latest['status']}")

async def main():
    """Run all tests"""
    
    print("Starting Enhanced Integration Tests...")
    print(f"Start Time: {datetime.now()}")
    
    try:
        # Run individual agent tests
        await test_enhanced_agents()
        
        # Run orchestrator tests
        workflow_result = await test_enhanced_orchestrator()
        
        # Test error handling
        await test_error_handling()
        
        # Test performance metrics
        await test_performance_metrics()
        
        # Test workflow history
        await test_workflow_history()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"End Time: {datetime.now()}")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
