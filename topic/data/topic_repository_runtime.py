import uuid

from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.topic_repository import TopicRepository


class TopicRepositoryRuntime(TopicRepository):

    def __init__(self):
        self.topics = {}

    def create_topic(self, user_id: str, name: str) -> TopicEntity:
        id = str(uuid.uuid4())
        topic = TopicEntity(id=id, name=name)
        if user_id not in self.topics:
            self.topics[user_id] = []
        self.topics[user_id].append(topic)
        return topic

    def get_all_topics(self, user_id: str) -> list[TopicEntity]:
        return self.topics.get(user_id, [])
