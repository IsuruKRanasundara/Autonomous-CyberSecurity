"""Kafka event publishing utilities."""

from typing import Any, Dict

from app.config.kafka import get_kafka_producer


class StreamProducer:
	"""Publish normalized events to Kafka topics."""

	def publish(self, topic: str, event: Dict[str, Any]) -> None:
		producer = get_kafka_producer()
		producer.send_event(topic, event)
