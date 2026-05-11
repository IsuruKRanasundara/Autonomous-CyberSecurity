"""Kafka producer and consumer configuration."""

import json
import logging
from typing import Any, Callable, Dict, List, Optional

from kafka import KafkaProducer, KafkaConsumer

from app.config.settings import settings


logger = logging.getLogger(__name__)


class KafkaEventTopics:
    """Kafka event topic constants."""

    ALERTS = settings.kafka.KAFKA_ALERTS_TOPIC
    INCIDENTS = settings.kafka.KAFKA_INCIDENTS_TOPIC
    LOGS = settings.kafka.KAFKA_LOGS_TOPIC
    TELEMETRY = settings.kafka.KAFKA_TELEMETRY_TOPIC

    @classmethod
    def all_topics(cls) -> List[str]:
        """Get all configured topics."""
        return [cls.ALERTS, cls.INCIDENTS, cls.LOGS, cls.TELEMETRY]


class KafkaProducerClient:
    """Kafka producer for sending events."""

    def __init__(self, bootstrap_servers: Optional[List[str]] = None):
        """Initialize Kafka producer.

        Args:
            bootstrap_servers: List of Kafka bootstrap servers.
                If None, uses settings.
        """
        self.bootstrap_servers = bootstrap_servers or settings.kafka.KAFKA_BOOTSTRAP_SERVERS
        self.producer: Optional[KafkaProducer] = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the Kafka producer."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
                retries=3,
                max_in_flight_requests_per_connection=1,
            )
            logger.info(
                "Kafka producer initialized with servers: %s",
                self.bootstrap_servers,
            )
        except Exception as e:
            logger.exception("Failed to initialize Kafka producer: %s", e)
            raise

    def send_event(
        self,
        topic: str,
        value: Dict[str, Any],
        key: Optional[str] = None,
        callback: Optional[Callable] = None,
    ) -> None:
        """Send an event to a Kafka topic.

        Args:
            topic: Topic name.
            value: Event data (dict).
            key: Optional message key for partitioning.
            callback: Optional callback for send completion.
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return

        try:
            future = self.producer.send(topic, value=value, key=key)
            if callback:
                future.add_callback(callback)
            else:
                future.add_errback(self._on_send_error)
            logger.debug("Event sent to topic %s: %s", topic, value)
        except Exception as e:
            logger.exception("Failed to send event to topic %s: %s", topic, e)

    def send_alert(self, alert_data: Dict[str, Any], key: Optional[str] = None) -> None:
        """Send an alert event.

        Args:
            alert_data: Alert information.
            key: Optional partition key.
        """
        self.send_event(KafkaEventTopics.ALERTS, alert_data, key=key)

    def send_incident(
        self, incident_data: Dict[str, Any], key: Optional[str] = None
    ) -> None:
        """Send an incident event.

        Args:
            incident_data: Incident information.
            key: Optional partition key.
        """
        self.send_event(KafkaEventTopics.INCIDENTS, incident_data, key=key)

    def send_logs(self, log_data: Dict[str, Any], key: Optional[str] = None) -> None:
        """Send a logs event.

        Args:
            log_data: Log information.
            key: Optional partition key.
        """
        self.send_event(KafkaEventTopics.LOGS, log_data, key=key)

    def send_telemetry(
        self, telemetry_data: Dict[str, Any], key: Optional[str] = None
    ) -> None:
        """Send a telemetry event.

        Args:
            telemetry_data: Telemetry information.
            key: Optional partition key.
        """
        self.send_event(KafkaEventTopics.TELEMETRY, telemetry_data, key=key)

    @staticmethod
    def _on_send_error(exc: Exception) -> None:
        """Error callback for send operations."""
        logger.error("Kafka send error: %s", exc)

    def flush(self, timeout_ms: int = 10000) -> None:
        """Flush pending messages.

        Args:
            timeout_ms: Timeout in milliseconds.
        """
        if self.producer:
            self.producer.flush(timeout_ms=timeout_ms)

    def close(self) -> None:
        """Close the producer."""
        if self.producer:
            try:
                self.producer.close()
                logger.info("Kafka producer closed")
            except Exception as e:
                logger.exception("Error closing Kafka producer: %s", e)


class KafkaConsumerClient:
    """Kafka consumer for processing events."""

    def __init__(
        self,
        topics: Optional[List[str]] = None,
        bootstrap_servers: Optional[List[str]] = None,
        group_id: Optional[str] = None,
    ):
        """Initialize Kafka consumer.

        Args:
            topics: List of topics to subscribe to.
            bootstrap_servers: List of Kafka bootstrap servers.
            group_id: Consumer group ID.
        """
        self.topics = topics or KafkaEventTopics.all_topics()
        self.bootstrap_servers = bootstrap_servers or settings.kafka.KAFKA_BOOTSTRAP_SERVERS
        self.group_id = group_id or settings.kafka.KAFKA_CONSUMER_GROUP
        self.consumer: Optional[KafkaConsumer] = None
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the Kafka consumer."""
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset=settings.kafka.KAFKA_AUTO_OFFSET_RESET,
                enable_auto_commit=True,
                session_timeout_ms=settings.kafka.KAFKA_SESSION_TIMEOUT_MS,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            logger.info(
                "Kafka consumer initialized for topics: %s (group: %s)",
                self.topics,
                self.group_id,
            )
        except Exception as e:
            logger.exception("Failed to initialize Kafka consumer: %s", e)
            raise

    def consume_messages(
        self, timeout_ms: int = 1000, max_records: int = 100
    ) -> Dict[str, Any]:
        """Consume messages from subscribed topics.

        Args:
            timeout_ms: Timeout in milliseconds.
            max_records: Maximum records to fetch.

        Returns:
            Dictionary of topic -> messages.
        """
        if not self.consumer:
            logger.error("Kafka consumer not initialized")
            return {}

        try:
            messages = self.consumer.poll(timeout_ms=timeout_ms, max_records=max_records)
            return messages
        except Exception as e:
            logger.exception("Error consuming messages: %s", e)
            return {}

    def seek_to_beginning(self) -> None:
        """Seek to beginning of all partitions."""
        if self.consumer:
            try:
                self.consumer.seek_to_beginning()
                logger.info("Seeked to beginning of all partitions")
            except Exception as e:
                logger.exception("Error seeking to beginning: %s", e)

    def seek_to_end(self) -> None:
        """Seek to end of all partitions."""
        if self.consumer:
            try:
                self.consumer.seek_to_end()
                logger.info("Seeked to end of all partitions")
            except Exception as e:
                logger.exception("Error seeking to end: %s", e)

    def commit(self) -> None:
        """Commit current offsets."""
        if self.consumer:
            try:
                self.consumer.commit()
                logger.debug("Consumer offsets committed")
            except Exception as e:
                logger.exception("Error committing offsets: %s", e)

    def close(self) -> None:
        """Close the consumer."""
        if self.consumer:
            try:
                self.consumer.close()
                logger.info("Kafka consumer closed")
            except Exception as e:
                logger.exception("Error closing Kafka consumer: %s", e)


# Global singleton instances
_producer_instance: Optional[KafkaProducerClient] = None
_consumer_instance: Optional[KafkaConsumerClient] = None


def get_kafka_producer() -> KafkaProducerClient:
    """Get or create the Kafka producer singleton.

    Returns:
        KafkaProducerClient instance.
    """
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = KafkaProducerClient()
    return _producer_instance


def get_kafka_consumer(
    topics: Optional[List[str]] = None,
) -> KafkaConsumerClient:
    """Get or create the Kafka consumer singleton.

    Args:
        topics: Optional list of topics to consume.

    Returns:
        KafkaConsumerClient instance.
    """
    global _consumer_instance
    if _consumer_instance is None:
        _consumer_instance = KafkaConsumerClient(topics=topics)
    return _consumer_instance


def close_kafka() -> None:
    """Close all Kafka connections."""
    global _producer_instance, _consumer_instance

    if _producer_instance:
        _producer_instance.close()
        _producer_instance = None

    if _consumer_instance:
        _consumer_instance.close()
        _consumer_instance = None

    logger.info("Kafka connections closed")
