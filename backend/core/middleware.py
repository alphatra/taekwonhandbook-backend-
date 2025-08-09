import logging
import time
import uuid
from typing import Callable

from django.http import HttpRequest, HttpResponse
from rich.console import Console
from rich.table import Table
from rich.text import Text


class RequestLogMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.logger = logging.getLogger("request")
        self.console = Console(force_terminal=True)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.monotonic()
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        response = None
        try:
            response = self.get_response(request)
            return response
        finally:
            duration_ms = int((time.monotonic() - start) * 1000)
            if response is None:
                status_code = 500
            else:
                status_code = response.status_code
                response.headers["X-Request-ID"] = request_id
            # Structured JSON log (dla prod agregacji)
            self.logger.info(
                "request",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.get_full_path(),
                    "status": status_code,
                    "duration_ms": duration_ms,
                    "user_id": getattr(getattr(request, "user", None), "id", None),
                    "remote_addr": request.META.get("REMOTE_ADDR"),
                },
            )
            # Rich pretty print (dev): kolor, tabela skrótowa
            try:
                status_text = Text(str(status_code), style="green" if 200 <= status_code < 400 else ("yellow" if 400 <= status_code < 500 else "red"))
                t = Table.grid(expand=False)
                t.add_column(justify="right", style="cyan", no_wrap=True)
                t.add_column()
                t.add_row("REQ", f"[{request_id}] {request.method} {request.get_full_path()}")
                t.add_row("STA", status_text)
                t.add_row("DUR", f"{duration_ms} ms")
                user_id = getattr(getattr(request, "user", None), "id", None)
                t.add_row("USR", str(user_id))
                self.console.print(t)
            except Exception:
                pass

