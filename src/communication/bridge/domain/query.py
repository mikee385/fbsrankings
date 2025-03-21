from typing import Any
from typing import Callable
from typing import cast
from typing import Optional

from communication.bus import QueryBus
from communication.channel import Channel
from communication.channel import Payload
from communication.messages import Q
from communication.messages import Query
from communication.messages import QueryHandler
from communication.messages import R
from serialization import Serializer


PayloadHandler = Callable[[Payload], None]


class QueryBridge(QueryBus):
    def __init__(
        self,
        channel: Channel,
        serializer: Serializer,
        topics: dict[type[Query[Any]], str],
    ) -> None:
        self._channel = channel
        self._serializer = serializer

        self._topics: dict[type[Query[Any]], str] = {}
        self._topics.update(topics)

        self._handlers: dict[type[Query[Any]], PayloadHandler] = {}
        self._results: dict[str, Optional[Any]] = {}

    def _get_request_topic(self, type_: type[Q]) -> str:
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")
        return topic + "/request"

    def _get_response_topic(self, query: Q) -> str:
        type_ = type(query)
        topic = self._topics.get(type_)
        if topic is None:
            raise ValueError(f"Unknown type: {type_}")
        return topic + "/response/" + str(query.query_id)

    def register_handler(self, type_: type[Q], handler: QueryHandler[Q, R]) -> None:
        query_type = type_

        def payload_handler(payload: Payload) -> None:
            query = self._serializer.deserialize(payload, query_type)
            result = handler(query)
            response = self._serializer.serialize(result)
            response_topic = self._get_response_topic(query)
            self._channel.publish(response_topic, response)

        existing = self._handlers.get(query_type)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {query_type}")
        self._handlers[query_type] = payload_handler

        request_topic = self._get_request_topic(query_type)
        self._channel.subscribe(request_topic, payload_handler)

    def unregister_handler(self, type_: type[Q]) -> None:
        payload_handler = self._handlers.pop(type_)
        if payload_handler is not None:
            request_topic = self._get_request_topic(type_)
            self._channel.unsubscribe(request_topic, payload_handler)

    def query(self, query: Query[R], return_type: type[R]) -> R:
        query_type = type(query)

        response_topic = self._get_response_topic(query)
        self._results[response_topic] = None

        def payload_handler(payload: Payload) -> None:
            result = self._serializer.deserialize(payload, return_type)
            if response_topic in self._results:
                self._results[response_topic] = result

        self._channel.subscribe(response_topic, payload_handler)

        request = self._serializer.serialize(query)
        request_topic = self._get_request_topic(query_type)
        self._channel.publish(request_topic, request)

        result = self._results.pop(response_topic)
        self._channel.unsubscribe(response_topic, payload_handler)

        if result is None:
            raise RuntimeError(f"No result found for {query_type}")

        return cast(R, result)
