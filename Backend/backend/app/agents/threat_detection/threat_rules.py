"""Detection rules and IOC matching logic."""

from typing import Any, Dict, Iterable, List


RULES: List[Dict[str, Any]] = [
	{"name": "suspicious_port", "ports": {22, 3389, 4444}},
	{"name": "malicious_hash", "hashes": {"example-malware-hash"}},
]


def match_rules(event: Dict[str, Any], iocs: Iterable[str] | None = None) -> List[str]:
	"""Return matching rule names for an event."""
	matches: List[str] = []
	ports = set(event.get("ports", []))
	file_hash = event.get("file_hash")

	for rule in RULES:
		if rule["name"] == "suspicious_port" and ports.intersection(rule["ports"]):
			matches.append(rule["name"])
		if rule["name"] == "malicious_hash" and file_hash in rule["hashes"]:
			matches.append(rule["name"])

	if iocs:
		indicators = set(iocs)
		if event.get("indicator") in indicators:
			matches.append("ioc_match")

	return matches
