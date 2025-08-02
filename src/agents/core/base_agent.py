from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """An abstract base class for all agents in the system."""

    def __init__(self, name: str):
        """
        Initializes the agent with a name.

        Args:
            name: The name of the agent.
        """
        self.name = name

    @abstractmethod
    def invoke(self, state: dict) -> dict:
        """
        The main method to run the agent's logic.
        Subclasses must implement this method.

        Args:
            state: The current state of the workflow.

        Returns:
            A dictionary representing the updated state.
        """
        pass

    def __call__(self, state: dict) -> dict:
        """Allows the agent to be called as a function."""
        print(f"--- EXECUTING AGENT: {self.name} ---")
        return self.invoke(state)
