"""
Enhanced Base Agent for the AI Marketing System
Provides unified architecture for all agents with advanced features
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import asyncio
from datetime import datetime
import json
from dataclasses import dataclass, asdict

@dataclass
class AgentMetrics:
    """Performance metrics for agent operations"""
    execution_time: float
    success_rate: float
    last_execution: datetime
    total_calls: int
    error_count: int

@dataclass
class AgentConfig:
    """Configuration for agent behavior"""
    model_name: str = "deepseek-r1-distill-llama-70b"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0

class EnhancedBaseAgent(ABC):
    """
    Enhanced base agent with unified architecture, logging, metrics, and error handling
    """
    
    def __init__(self, name: str, config: Optional[AgentConfig] = None):
        self.name = name
        self.config = config or AgentConfig()
        self.metrics = AgentMetrics(
            execution_time=0.0,
            success_rate=1.0,
            last_execution=datetime.now(),
            total_calls=0,
            error_count=0
        )
        self.logger = self._setup_logger()
        self.memory = {}
        
    def _setup_logger(self) -> logging.Logger:
        """Setup dedicated logger for this agent"""
        logger = logging.getLogger(f"agent.{self.name}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    async def execute_with_metrics(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with performance tracking"""
        start_time = datetime.now()
        self.metrics.total_calls += 1
        
        try:
            self.logger.info(f"Starting execution with state: {list(state.keys())}")
            result = await self._execute_safe(state)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics.execution_time = execution_time
            self.metrics.last_execution = datetime.now()
            
            self.logger.info(f"Completed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            self.metrics.error_count += 1
            self.metrics.success_rate = (
                (self.metrics.total_calls - self.metrics.error_count) 
                / self.metrics.total_calls
            )
            
            self.logger.error(f"Execution failed: {str(e)}")
            return self._handle_error(state, e)
    
    async def _execute_safe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Safe execution with retry logic"""
        last_error = None
        
        for attempt in range(self.config.retry_count + 1):
            try:
                return await self._execute_with_timeout(state)
            except Exception as e:
                last_error = e
                if attempt < self.config.retry_count:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                    self.logger.warning(f"Retry attempt {attempt + 1} after error: {str(e)}")
        
        raise last_error
    
    async def _execute_with_timeout(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with timeout protection"""
        try:
            return await asyncio.wait_for(
                self._execute_core(state),
                timeout=self.config.timeout
            )
        except asyncio.TimeoutError:
            raise TimeoutError(f"Agent execution timed out after {self.config.timeout}s")
    
    @abstractmethod
    async def _execute_core(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Core agent logic - must be implemented by subclasses"""
        pass
    
    def _handle_error(self, state: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        """Handle errors gracefully"""
        error_info = {
            "error": str(error),
            "agent": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            **state,
            "error": error_info,
            f"{self.name.lower().replace(' ', '_')}_error": str(error)
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return {
            **asdict(self.metrics),
            "agent_name": self.name,
            "config": asdict(self.config)
        }
    
    def update_config(self, **kwargs) -> None:
        """Update agent configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
    
    def store_memory(self, key: str, value: Any) -> None:
        """Store information in agent memory"""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def retrieve_memory(self, key: str) -> Optional[Any]:
        """Retrieve information from agent memory"""
        if key in self.memory:
            return self.memory[key]["value"]
        return None
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for async execution"""
        return asyncio.run(self.execute_with_metrics(state))
