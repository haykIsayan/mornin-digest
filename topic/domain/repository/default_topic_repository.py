from abc import ABC, abstractmethod

from topic.domain.entity.topic_entity import TopicEntity


class DefaultTopicRepository(ABC):

    @abstractmethod
    def get_default_topics(self) -> list[TopicEntity]:
        pass
