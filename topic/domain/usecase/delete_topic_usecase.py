from topic.domain.repository.topic_repository import TopicRepository


class DeleteTopicUseCase:
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def execute(self, user_id: str, topic_id: str) -> None:
        self.topic_repository.delete_topic(user_id, topic_id)
