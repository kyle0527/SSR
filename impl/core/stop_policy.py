from dataclasses import dataclass, field
import time

@dataclass
class StopPolicy:
    max_consecutive_errors: int = 3
    max_runtime_seconds: int | None = 900
    per_target_timeout_seconds: int | None = 60
    fail_fast: bool = True
    max_drop_ratio: float = 0.5

    start_ts: float = field(default_factory=time.monotonic)
    consecutive_errors: int = 0
    kept: int = 0
    dropped: int = 0

    def on_error(self) -> None:
        self.consecutive_errors += 1

    def on_success(self) -> None:
        self.consecutive_errors = 0

    def on_batch_result(self, kept: int, dropped: int) -> None:
        self.kept += kept
        self.dropped += dropped

    def exceeded_time(self) -> bool:
        return self.max_runtime_seconds is not None and (time.monotonic() - self.start_ts) >= self.max_runtime_seconds

    def exceeded_consecutive_errors(self) -> bool:
        return self.consecutive_errors >= self.max_consecutive_errors

    def exceeded_drop_ratio(self) -> bool:
        total = self.kept + self.dropped
        if total == 0: return False
        return (self.dropped / total) >= self.max_drop_ratio

    def should_stop(self) -> tuple[bool, str | None]:
        if self.exceeded_time():
            return True, "max_runtime_seconds"
        if self.exceeded_consecutive_errors():
            return True, "max_consecutive_errors"
        if self.exceeded_drop_ratio():
            return True, "max_drop_ratio"
        return False, None