"""Kafka event consumption utilities."""

from typing import Any, Dict, List

from app.config.kafka import get_kafka_consumer


class StreamConsumer:
	"""Consume normalized events from Kafka topics."""

	def poll(self) -> Dict[str, Any]:
		consumer = get_kafka_consumer()
		return consumer.consume_messages()
