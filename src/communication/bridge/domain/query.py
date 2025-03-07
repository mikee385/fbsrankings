from typing import Callable
from typing import Dict
from typing import Optional
from typing import Type

from communication.bus.domain.query import Q
from communication.bus.domain.query import Query
from communication.bus.domain.query import QueryBus
from communication.bus.domain.query import QueryHandler
from communication.bus.domain.query import R
from communication.channel import Channel
from communication.channel import Payload
from serialization import Serializer


PayloadHandler = Callable[[Payload], None]


class QueryBridge(QueryBus):
    def __init__(
        self,
        channel: Channel,
        serializer: Serializer,
        topics: Dict[Type[Query[R]], str],
        result_types: Dict[Type[Query[R]], Type[R]],
    ) -> None:
        self._channel = channel
        self._serializer = serializer

        self._request_topics: Dict[Type[Query[R]], str] = {}
        self._response_topics: Dict[Type[Query[R]], str] = {}
        for type_, topic in topics.items():
            self._request_topics[type_] = topic + "/request"
            self._response_topics[type_] = topic + "/response"

        self._result_types: Dict[Type[Query[R]], Type[R]] = {}
        self._result_types.update(result_types)

        self._handlers: Dict[Type[Query[R]], PayloadHandler] = {}
        self._results: Dict[str, Optional[R]] = {}

    def register_handler(self, type_: Type[Q], handler: QueryHandler[Q, R]) -> None:
        query_type = type_

        if query_type not in self._request_topics:
            raise ValueError(f"Unknown type: {query_type}")
        request_topic = self._request_topics[query_type]

        if query_type not in self._response_topics:
            raise ValueError(f"Unknown type: {query_type}")
        response_topic = self._response_topics[query_type]

        def payload_handler(payload: Payload) -> None:
            query = self._serializer.deserialize(payload, query_type)
            result = handler(query)
            response = self._serializer.serialize(result)
            self._channel.publish(response_topic + "/" + str(query.query_id), response)

        existing = self._handlers.get(query_type)
        if existing is not None:
            raise ValueError(f"A handler has already been registered for {query_type}")
        self._handlers[type_] = payload_handler

        self._channel.subscribe(request_topic, payload_handler)

    def unregister_handler(self, type_: Type[Q]) -> None:
        request_topic = self._request_topics.get(type_)
        if request_topic is None:
            raise ValueError(f"Unknown type: {type_}")

        payload_handler = self._handlers.pop(type_)
        if payload_handler is not None:
            self._channel.unsubscribe(request_topic, payload_handler)

    def query(self, query: Query[R]) -> R:
        query_type = type(query)

        if query_type not in self._result_types:
            raise ValueError(f"Unknown type: {query_type}")
        result_type = self._result_types[query_type]

        if query_type not in self._request_topics:
            raise ValueError(f"Unknown type: {query_type}")
        request_topic = self._request_topics[query_type]

        if query_type not in self._response_topics:
            raise ValueError(f"Unknown type: {query_type}")
        response_topic = self._response_topics[query_type] + "/" + str(query.query_id)

        self._results[response_topic] = None

        def payload_handler(payload: Payload) -> None:
            result = self._serializer.deserialize(payload, result_type)
            if response_topic in self._results:
                self._results[response_topic] = result

        self._channel.subscribe(response_topic, payload_handler)

        request = self._serializer.serialize(query)
        self._channel.publish(request_topic, request)

        result = self._results.pop(response_topic)
        self._channel.unsubscribe(response_topic, payload_handler)

        if result is None:
            raise RuntimeError(f"No result found for {query_type}")

        return result
