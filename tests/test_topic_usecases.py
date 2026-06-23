from unittest.mock import MagicMock

from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.usecase.create_topic_usecase import CreateTopicUseCase
from topic.domain.usecase.get_all_topics_usecase import GetAllTopicsUseCase


def make_topic(id="t1", name="python"):
    return TopicEntity(id=id, name=name)


class TestCreateTopicUseCase:
    def test_creates_and_returns_topic(self):
        repo = MagicMock()
        topic = make_topic()
        repo.create_topic.return_value = topic
        use_case = CreateTopicUseCase(repo)

        result = use_case.execute("u1", "python")

        repo.create_topic.assert_called_once_with("u1", "python")
        assert result is topic


class TestGetAllTopicsUseCase:
    def test_returns_all_topics_for_user(self):
        repo = MagicMock()
        topics = [make_topic("t1", "python"), make_topic("t2", "rust")]
        repo.get_all_topics.return_value = topics
        use_case = GetAllTopicsUseCase(repo)

        result = use_case.execute("u1")

        repo.get_all_topics.assert_called_once_with("u1")
        assert result == topics

    def test_returns_empty_list_when_user_has_no_topics(self):
        repo = MagicMock()
        repo.get_all_topics.return_value = []
        use_case = GetAllTopicsUseCase(repo)

        result = use_case.execute("u1")

        assert result == []
