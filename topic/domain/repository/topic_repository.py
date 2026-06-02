from abc import ABC, abstractmethod

from topic.domain.entity.topic_entity import TopicEntity

class TopicRepository(ABC):

    @abstractmethod
    def get_all_topics(self, userId: str) -> list[TopicEntity]:
        pass

    @abstractmethod
    def create_topic(self, userId: str, name: str) -> TopicEntity:
        pass
