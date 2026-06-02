import uuid

from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.topic_repository import TopicRepository


class TopicRepositoryRuntime(TopicRepository):

    def __init__(self):
        self.topics = {}

    def create_topic(self, userId: str, name: str) -> TopicEntity:
        id = str(uuid.uuid4())
        topic = TopicEntity(id=id, name=name)
        if userId not in self.topics:
            self.topics[userId] = []
        self.topics[userId].append(topic)
        return topic

    def get_all_topics(self, userId: str) -> list[TopicEntity]:
        return self.topics.get(userId, [])
