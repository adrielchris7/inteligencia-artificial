"""The toy world loaded from YAML: facts, weather, and example queries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Fact:
    key: str
    aliases: tuple[str, ...]
    text: str


@dataclass(frozen=True)
class Forecast:
    city: str
    temp: int
    summary: str


@dataclass(frozen=True)
class Prior:
    match: str
    answer: str


@dataclass(frozen=True)
class World:
    name: str
    facts: tuple[Fact, ...]
    weather: tuple[Forecast, ...]
    queries: tuple[str, ...]
    priors: tuple[Prior, ...]
    max_steps: int
    source: Path | None = None

    def forecast(self, city: str) -> Forecast | None:
        needle = _fold(city)
        for item in self.weather:
            if _fold(item.city) == needle:
                return item
        return None

    def lookup(self, query: str) -> Fact | None:
        needle = _fold(query)
        for fact in self.facts:
            names = (fact.key, *fact.aliases)
            if any(needle == _fold(name) or needle in _fold(name) or _fold(name) in needle for name in names):
                return fact
        return None


def load_world(path: str | Path) -> World:
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    return parse_world(raw, source=path)


def parse_world(raw: dict[str, Any], source: Path | None = None) -> World:
    facts = _facts(raw.get("facts"))
    weather = _weather(raw.get("weather"))
    if not facts and not weather:
        raise ValueError("facts or weather: provide at least one tool source")

    max_steps = int(raw.get("max_steps", 6))
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")

    return World(
        name=str(raw.get("name") or "world"),
        facts=facts,
        weather=weather,
        queries=tuple(str(q) for q in (raw.get("queries") or [])),
        priors=tuple(
            Prior(match=str(p["match"]), answer=str(p["answer"]))
            for p in (raw.get("priors") or [])
            if isinstance(p, dict) and p.get("match") and p.get("answer")
        ),
        max_steps=max_steps,
        source=source,
    )


def _facts(rows: Any) -> tuple[Fact, ...]:
    out: list[Fact] = []
    for i, row in enumerate(rows or []):
        if not isinstance(row, dict):
            raise ValueError(f"facts[{i}] must be a mapping with key and text")
        text = str(row.get("text") or "").strip()
        key = str(row.get("key") or "").strip()
        if not key or not text:
            raise ValueError(f"facts[{i}] needs key and text")
        aliases = tuple(str(a) for a in (row.get("aliases") or []))
        out.append(Fact(key=key, aliases=aliases, text=text))
    return tuple(out)


def _weather(raw: Any) -> tuple[Forecast, ...]:
    out: list[Forecast] = []
    if not raw:
        return ()
    if not isinstance(raw, dict):
        raise ValueError("weather must be a mapping of city → {temp, summary}")
    for city, payload in raw.items():
        if not isinstance(payload, dict):
            raise ValueError(f"weather[{city}] must be a mapping with temp and summary")
        out.append(
            Forecast(
                city=str(city),
                temp=int(payload["temp"]),
                summary=str(payload.get("summary") or "").strip(),
            )
        )
    return tuple(out)


def _fold(text: str) -> str:
    return " ".join(text.casefold().split())
