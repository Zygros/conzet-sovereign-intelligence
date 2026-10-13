"""Loopback HTTP acceptance test for the bounded A2A envelope contract.

This uses a real localhost HTTP request/response, but the receiver is a test
fixture, not a remote production agent or external model.
"""
from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen

from scripts.a2a_envelope import validate_envelope


def _make_envelope(*, message_id, task_id, sender, recipient, task_type, payload, digest, status):
    return {
        "protocol_version": "1.0",
        "message_id": message_id,
        "task_id": task_id,
        "sender": sender,
        "recipient": recipient,
        "task_type": task_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "permissions": {
            "scopes": ["source:read", "evidence:write"],
            "sensitive_action_confirmation": True,
        },
        "payload": payload,
        "evidence": [{
            "kind": "sha256",
            "uri": "urn:sha256:" + digest,
            "sha256": digest,
        }],
        "provenance": {
            "source_refs": ["urn:conzetian:a2a-http-fixture"],
            "producer": sender,
            "schema_version": "1.0",
            "repository_commit": None,
        },
        "status": status,
    }


def test_local_http_a2a_round_trip_preserves_task_and_digest():
    task = {"objective": "classify fixture", "execution_allowed": False}
    canonical = json.dumps(task, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    received = {}

    class Receiver(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            request_envelope = json.loads(self.rfile.read(length))
            received["validation_errors"] = validate_envelope(request_envelope)
            received["request"] = request_envelope
            response_envelope = _make_envelope(
                message_id="http-response-001",
                task_id=request_envelope["task_id"],
                sender="localhost-test-agent",
                recipient=request_envelope["sender"],
                task_type=request_envelope["task_type"] + ".result",
                payload={
                    "task_id": request_envelope["task_id"],
                    "decision": "needs_review",
                    "execution_performed": False,
                },
                digest=digest,
                status="completed",
            )
            body = json.dumps(response_envelope).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            return

    server = HTTPServer(("127.0.0.1", 0), Receiver)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request_envelope = _make_envelope(
            message_id="http-request-001",
            task_id="task-http-001",
            sender="phoenix-test-client",
            recipient="localhost-test-agent",
            task_type="review_discovery_candidate",
            payload=task,
            digest=digest,
            status="submitted",
        )
        assert validate_envelope(request_envelope) == []
        request = Request(
            f"http://127.0.0.1:{server.server_port}/a2a",
            data=json.dumps(request_envelope).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            assert response.status == 200
            result = json.loads(response.read())

        assert received["validation_errors"] == []
        assert result["task_id"] == request_envelope["task_id"]
        assert result["evidence"][0]["sha256"] == digest
        assert validate_envelope(result) == []
        assert result["payload"]["execution_performed"] is False
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
