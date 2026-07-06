from topic.data.postgres_topic_repository import TopicRepositoryPostgres
from topic.data.default_topic_repository_impl import DefaultTopicRepositoryImpl
from topic.domain.usecase.create_topic_usecase import CreateTopicUseCase
from topic.domain.usecase.delete_topic_usecase import DeleteTopicUseCase
from topic.domain.usecase.get_all_topics_usecase import GetAllTopicsUseCase
from topic.domain.usecase.get_default_topics_usecase import GetDefaultTopicsUseCase


class TopicContainer:
    def __init__(self):
        self.topic_repository = TopicRepositoryPostgres()
        self.topic_repository.init_db()

        self.create_topic_use_case = CreateTopicUseCase(self.topic_repository)
        self.delete_topic_use_case = DeleteTopicUseCase(self.topic_repository)
        self.get_all_topics_use_case = GetAllTopicsUseCase(self.topic_repository)
        self.get_default_topics_use_case = GetDefaultTopicsUseCase(DefaultTopicRepositoryImpl())

container = TopicContainer()
