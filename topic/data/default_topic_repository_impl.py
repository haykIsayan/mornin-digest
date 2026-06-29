from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.default_topic_repository import DefaultTopicRepository

_DEFAULT_TOPICS = [
    "Technology",
    "Science",
    "Health & Wellness",
    "Business",
    "Sports",
    "Politics",
    "Arts & Culture",
    "Movies",
    "Shows",
    "Music",
    "Food & Drink",
    "Gaming",
    "Environment",
    "Finance",
    "Travel",
]


class DefaultTopicRepositoryImpl(DefaultTopicRepository):

    def get_default_topics(self) -> list[TopicEntity]:
        return [
            TopicEntity(id=str(i), name=name)
            for i, name in enumerate(_DEFAULT_TOPICS, start=1)
        ]
