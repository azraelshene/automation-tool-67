import math
import random
import time
from typing import Any, Callable, Dict, Optional, Type


class DynamicCryptoHandler:
    def __init__(self, max_attempts: int = 4):
        self.max_attempts = max_attempts
        self.fallbacks: Dict[Type[Exception], Callable[[Exception, int], Optional[Any]]] = {}

    def bind_edge_case(self, *exceptions: Type[Exception]):
        def wrapper(fn: Callable[[Exception, int], Any]):
            for exc in exceptions:
                self.fallbacks[exc] = fn
            return fn
        return wrapper

    def safe_run(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        history = []
        for attempt in range(1, self.max_attempts + 1):
            try:
                payload = operation(*args, **kwargs)
                return {"success": True, "data": payload, "attempts": attempt, "trace": history}
            except Exception as err:
                history.append(f"{type(err).__name__}: {str(err)}")
                handler = self.fallbacks.get(type(err)) or self._match_subclass(err)
                
                if not handler or attempt == self.max_attempts:
                    return {
                        "success": False,
                        "error": str(err),
                        "type": type(err).__name__,
                        "attempts": attempt,
                        "trace": history,
                    }

                handler(err, attempt)
                jitter = random.uniform(0.05, 0.25)
                time.sleep(math.pow(1.5, attempt) * 0.1 + jitter)

    def _match_subclass(self, err: Exception) -> Optional[Callable]:
        for exc_cls, fn in self.fallbacks.items():
            if isinstance(err, exc_cls):
                return fn
        return None


rpc_handler = DynamicCryptoHandler(max_attempts=3)


@rpc_handler.bind_edge_case(ConnectionResetError, TimeoutError)
def _handle_network_flicker(err: Exception, attempt: int) -> None:
    err.args = (*err.args, f"retry_sequence_{attempt}")


@rpc_handler.bind_edge_case(ValueError, ArithmeticError)
def _handle_slippage_or_math(err: Exception, attempt: int) -> None:
    err.args = (*err.args, f"sanitized_inputs_v{attempt}")
