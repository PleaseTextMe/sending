from prometheus_client import Counter, Gauge

ACTIVE_WS_CONNECTIONS = Gauge(
    "active_websocket_connections",
    "Number of active WebSocket connections"
)

TYPING_EVENTS_TOTAL = Counter(
    "typing_events_total",
    "Total number of typing events sent"
)
