from abc import ABC, abstractmethod
from typing import Any

from src.models.schemas import Campaign


class StateManager(ABC):
    """Abstract base for persisting swarm state."""

    @abstractmethod
    async def save_campaign(self, campaign: Campaign):
        pass

    @abstractmethod
    async def save_task_result(self, campaign_id: str, result: dict[str, Any]):
        pass

    @abstractmethod
    async def get_campaign_status(self, campaign_id: str) -> Campaign | None:
        pass


class InMemoryStateManager(StateManager):
    """
    Simple in-memory implementation for MVP/Testing.

    PRODUCTION MIGRATION PATH:
    - PostgreSQL: Use 'asyncpg' to implement campaigns/tasks persistence using the schema defined in technical.md.
    - Redis: Use 'redis-py' for episodic task queues and caching persona traits.
    - Consistency: Implement OCC via 'state_version' in PostgreSQL updates.
    """

    def __init__(self):
        self.campaigns: dict[str, Campaign] = {}
        self.results: dict[str, list[dict[str, Any]]] = {}

    async def save_campaign(self, campaign: Campaign):
        self.campaigns[str(campaign.id)] = campaign
        if str(campaign.id) not in self.results:
            self.results[str(campaign.id)] = []

    async def save_task_result(self, campaign_id: str, result: dict[str, Any]):
        if campaign_id in self.results:
            self.results[campaign_id].append(result)

    async def get_campaign_status(self, campaign_id: str) -> Campaign | None:
        return self.campaigns.get(campaign_id)
