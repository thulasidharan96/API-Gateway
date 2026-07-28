from __future__ import annotations

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

_TELEMETRY_CONFIGURED = False


def configure_telemetry(*, service_name: str, service_version: str) -> None:
    global _TELEMETRY_CONFIGURED
    if _TELEMETRY_CONFIGURED:
        return

    provider = TracerProvider(
        resource=Resource.create(
            {"service.name": service_name, "service.version": service_version}
        ),
    )
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    _TELEMETRY_CONFIGURED = True


def instrument_fastapi(app: object) -> None:
    FastAPIInstrumentor.instrument_app(app)  # type: ignore[arg-type]
