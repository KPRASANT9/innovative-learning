"""Python: the craft of programming, compressed into a blueprint.

Sibling of SQL.md. SQL names how a question moves through data.
This module names how a program stays honest while it answers.
Read a piece of work from the inside out:

    Intelligence = level_5(level_4(level_3(level_2(level_1(facts)))))

Five questions. Five levels. Each level is a pure step with a closed
type, so the next idea can sit on top of this file without reopening
a promise that was already kept.

                 [ LEVEL 5: THE ROW THAT CAN SEE ]
                                |
                     (window by identity, in time)
                                |
                                v
               [ LEVEL 4: A NORMAL WITH MEMORY ]
                                |
                      (sum and count, not the row)
                                |
                                v
               [ LEVEL 3: ONE CONTEXT, TWO KEYS ]
                                |
                         (join, gaps named)
                                |
                                v
               [ LEVEL 2: THE REFUSAL ]
                                |
                        (filter at the gate)
                                |
                                v
                  [ LEVEL 1: THE HONEST FACT ]
                                |
                     (type, identity, immutability)
                                |
                                v
                       [ THE THING ITSELF ]
                 (money, time, a name, a bool)

When to stand on which level
----------------------------
Need                         Level   What you hold afterward
define / validate / store    1       an immutable fact
filter / refuse / search     2       a smaller honest set
relate / join / synthesize   3       one context, gaps named
summarize / baseline         4       a normal that forgot the row
compare / window / context   5       the row, with its neighbors

Worked example: the same financial risk sketch as SQL.md, corrected
where a sketch would otherwise flatter the outlier or drop a gap.

Prepare on top of this by replacing a level or by reading Intelligence.
Do not weaken level 1 to make a later level easier.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from typing import Iterable


MONEY = Decimal("0.01")
RATIO = Decimal("0.0001")
DEFAULT_WINDOW = 3  # current row and two predecessors, as in ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
DEFAULT_ANOMALY_MULTIPLE = Decimal("3")


class CraftError(Exception):
    """A blueprint was asked to guess, or a fact broke its promise."""


@dataclass(frozen=True, slots=True)
class Level:
    """One question the craft keeps, and the wisdom that answers it."""

    number: int
    question: str
    wisdom: str
    operation: str
    when: str


LEVELS: tuple[Level, ...] = (
    Level(
        1,
        "What must remain true of a single fact, no matter who handles it later?",
        "Give the fact a type, an identity, and no way to change its mind. "
        "Money is a decimal. Time knows its zone. A bool is a bool.",
        "construct and validate",
        "a fact is born, or a raw value crosses the edge of the program",
    ),
    Level(
        2,
        "What should be refused before it is allowed to meet anything else?",
        "Refuse at the gate. A declined charge is a different story, not a small "
        "transaction. The join is not a place to clean up.",
        "filter",
        "some facts are out of the question you are actually asking",
    ),
    Level(
        3,
        "How do two kinds of fact become one context without either losing its key?",
        "Join on identity. When the other side is missing, name the gap. "
        "A silent gap becomes a wrong number downstream.",
        "join",
        "the answer needs attributes that live in more than one relation",
    ),
    Level(
        4,
        "What is allowed to be forgotten when many facts become a normal?",
        "Compress into sufficient statistics. Keep sum and count. "
        "The individual row does not live in this layer, and an average that "
        "already includes the point you will judge is not yet a fair normal.",
        "group into sum and count",
        "you need a normal and you truly mean to forget the row",
    ),
    Level(
        5,
        "How does one fact see its neighbors and still remain itself?",
        "Partition by identity, order by time, frame a finite window. "
        "Judge the row against peers. When the peer set is empty, leave it unnamed.",
        "window and compare",
        "the answer must name the row and also know its surroundings",
    ),
)

QUESTIONS: tuple[str, ...] = tuple(level.question for level in LEVELS)

RULES: tuple[str, ...] = (
    "Model the fact before you summarize it.",
    "Refuse at the gate, before any join.",
    "Keep the row when the answer must name the row.",
    "Judge a row against peers, using statistics that can exclude the row itself.",
    "Leave an empty peer set unnamed.",
)

_NEEDS: dict[str, int] = {
    "store": 1,
    "define": 1,
    "validate": 1,
    "filter": 2,
    "refuse": 2,
    "search": 2,
    "relate": 3,
    "join": 3,
    "synthesize": 3,
    "summarize": 4,
    "compress": 4,
    "baseline": 4,
    "compare": 5,
    "window": 5,
    "context": 5,
}


def answer(number: int) -> Level:
    """Return the level that answers one of the five questions."""

    if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= len(LEVELS):
        raise CraftError("the craft has five questions, numbered 1 through 5")
    return LEVELS[number - 1]


def choose_level(need: str) -> Level:
    """Name the need. Receive the level that is built to carry it."""

    if not isinstance(need, str):
        raise CraftError("name the need with a string")
    key = need.strip().lower()
    try:
        number = _NEEDS[key]
    except KeyError as exc:
        known = ", ".join(sorted(_NEEDS))
        raise CraftError(f"unknown need {need!r}; the blueprint knows: {known}") from exc
    return answer(number)


def _expect(value: object, kind: type, message: str) -> None:
    if type(value) is not kind:
        raise CraftError(message)


def _positive_int(value: object, name: str) -> int:
    # bool is a subclass of int. A flag is not an identity.
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CraftError(f"{name} must be a positive int")
    return value


def _key(value: object, name: str) -> str:
    if not isinstance(value, str) or value == "" or value != value.strip():
        raise CraftError(f"{name} must be a non-empty string with no surrounding space")
    return value


def _money(value: object) -> Decimal:
    """Banker's rounding to cents. Floats are refused because they cannot name most cents."""

    if isinstance(value, bool) or isinstance(value, float):
        raise CraftError("money takes Decimal, int, or a decimal string; a float cannot name most cents")
    if isinstance(value, Decimal):
        amount = value
    elif isinstance(value, int):
        amount = Decimal(value)
    elif isinstance(value, str):
        if value != value.strip():
            raise CraftError("money must be an exact decimal string")
        try:
            amount = Decimal(value)
        except InvalidOperation as exc:
            raise CraftError(f"money cannot read {value!r}") from exc
    else:
        raise CraftError("money takes Decimal, int, or a decimal string")
    if not amount.is_finite():
        raise CraftError("money must be a finite amount")
    if amount < 0:
        raise CraftError("money must be zero or more")
    return amount.quantize(MONEY, rounding=ROUND_HALF_EVEN)


def _instant(value: object) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise CraftError("timestamp must be a timezone-aware datetime")
    return value


def _bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise CraftError(f"{name} must be a bool")
    return value


def _window(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise CraftError("window must be a positive int")
    return value


def _multiple(value: object) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise CraftError("anomaly multiple must be a positive Decimal")
    return value


# --- Level 1: the honest fact -------------------------------------------------


@dataclass(frozen=True, slots=True)
class Transaction:
    """One movement of money. Cohort is not here: it belongs to the user, not the event.

    A profile that changes over time would be a third relation. This blueprint
    does not pretend a single profile is a history.
    """

    transaction_id: int
    user_id: int
    amount: Decimal
    ts: datetime
    is_declined: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "transaction_id", _positive_int(self.transaction_id, "transaction_id"))
        object.__setattr__(self, "user_id", _positive_int(self.user_id, "user_id"))
        object.__setattr__(self, "amount", _money(self.amount))
        object.__setattr__(self, "ts", _instant(self.ts))
        object.__setattr__(self, "is_declined", _bool(self.is_declined, "is_declined"))


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Who the user is for this question. One user, one profile, one cohort."""

    user_id: int
    cohort_id: str
    risk_tier: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "user_id", _positive_int(self.user_id, "user_id"))
        object.__setattr__(self, "cohort_id", _key(self.cohort_id, "cohort_id"))
        object.__setattr__(self, "risk_tier", _key(self.risk_tier, "risk_tier"))


@dataclass(frozen=True, slots=True)
class Ledger:
    """Level 1 result. Facts with unique identities, input order preserved."""

    entries: tuple[Transaction, ...]


def level_1(transactions: Iterable[Transaction]) -> Ledger:
    """Bind facts. Identity collision is a broken ledger, not a row to merge quietly."""

    entries = tuple(transactions)
    seen: set[int] = set()
    for entry in entries:
        _expect(entry, Transaction, "a ledger accepts only Transaction facts")
        if entry.transaction_id in seen:
            raise CraftError(
                f"transaction identity collided on transaction_id={entry.transaction_id}"
            )
        seen.add(entry.transaction_id)
    return Ledger(entries)


# --- Level 2: the refusal -----------------------------------------------------


@dataclass(frozen=True, slots=True)
class SettledLedger:
    """Level 2 result. Declined charges cannot be constructed into this type."""

    entries: tuple[Transaction, ...]

    def __post_init__(self) -> None:
        declined = tuple(entry.transaction_id for entry in self.entries if entry.is_declined)
        if declined:
            raise CraftError(f"settled ledger still holds declined transactions: {declined}")


def level_2(ledger: Ledger) -> SettledLedger:
    """Keep the charges that actually settled. Refusal happens before any join."""

    _expect(ledger, Ledger, "filter accepts only a ledger from level 1")
    kept = tuple(entry for entry in ledger.entries if not entry.is_declined)
    return SettledLedger(kept)


# --- Level 3: one context, two keys ------------------------------------------


@dataclass(frozen=True, slots=True)
class Hydrated:
    """A settled event that found its profile. Both keys are still on the value."""

    transaction: Transaction
    profile: UserProfile


@dataclass(frozen=True, slots=True)
class Gap:
    """A settled event with no profile. Present, named, and out of every average."""

    transaction: Transaction
    reason: str


@dataclass(frozen=True, slots=True)
class Synthesis:
    """Level 3 result. Matched rows and named gaps. Nothing in the settled set is dropped."""

    matched: tuple[Hydrated, ...]
    gaps: tuple[Gap, ...]


def level_3(settled: SettledLedger, profiles: Iterable[UserProfile]) -> Synthesis:
    """Join on user_id. Extra profiles are unused context. A missing profile is a gap.

    The fact table drives the question. A wider dimension table is not an error.
    Two profiles for one user is a broken key, and the join refuses to pick one.
    """

    _expect(settled, SettledLedger, "join accepts only a settled ledger; filter first")
    by_user: dict[int, UserProfile] = {}
    for profile in profiles:
        _expect(profile, UserProfile, "join accepts only UserProfile facts")
        if profile.user_id in by_user:
            raise CraftError(f"profile identity collided on user_id={profile.user_id}")
        by_user[profile.user_id] = profile

    matched: list[Hydrated] = []
    gaps: list[Gap] = []
    for entry in settled.entries:
        profile = by_user.get(entry.user_id)
        if profile is None:
            gaps.append(
                Gap(entry, f"no profile for user_id={entry.user_id}")
            )
        else:
            matched.append(Hydrated(entry, profile))
    return Synthesis(tuple(matched), tuple(gaps))


# --- Level 4: a normal with memory -------------------------------------------


@dataclass(frozen=True, slots=True)
class CohortBaseline:
    """Sufficient statistics for one cohort. The rows that produced them are gone."""

    cohort_id: str
    count: int
    total: Decimal

    def peer_average(self, amount: Decimal) -> Decimal | None:
        """Average of everyone else in the cohort.

        Returns None when the row has no peer. A single member cannot be a normal.
        """

        amount = _money(amount)
        if amount > self.total:
            raise CraftError("cannot exclude an amount larger than the cohort total")
        others = self.count - 1
        if others <= 0:
            return None
        return ((self.total - amount) / Decimal(others)).quantize(MONEY, rounding=ROUND_HALF_EVEN)


@dataclass(frozen=True, slots=True)
class BaselineBook:
    """Level 4 result. Cohorts in key order. Gaps never enter the book."""

    cohorts: tuple[CohortBaseline, ...]

    def for_cohort(self, cohort_id: str) -> CohortBaseline:
        for cohort in self.cohorts:
            if cohort.cohort_id == cohort_id:
                return cohort
        raise CraftError(f"no baseline for cohort_id={cohort_id}")


def level_4(synthesis: Synthesis) -> BaselineBook:
    """Collapse matched rows into sum and count. Gaps stay out, so a missing profile cannot move a normal."""

    _expect(synthesis, Synthesis, "baseline accepts only a synthesis from level 3")
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    counts: dict[str, int] = defaultdict(int)
    for row in synthesis.matched:
        cohort_id = row.profile.cohort_id
        totals[cohort_id] += row.transaction.amount
        counts[cohort_id] += 1
    cohorts = tuple(
        CohortBaseline(cohort_id, counts[cohort_id], totals[cohort_id])
        for cohort_id in sorted(counts)
    )
    return BaselineBook(cohorts)


# --- Level 5: the row that can see -------------------------------------------


@dataclass(frozen=True, slots=True)
class RiskScore:
    """The original event, plus a finite look at its past, judged against peers.

    risk_tier is carried and not interpreted. The next policy can use it
    without opening the join again.
    """

    transaction_id: int
    user_id: int
    cohort_id: str
    risk_tier: str
    occurred_at: datetime
    amount: Decimal
    moving_count: int
    moving_total: Decimal
    moving_average: Decimal
    peer_average: Decimal | None
    ratio: Decimal | None
    anomalous: bool


@dataclass(frozen=True, slots=True)
class Intelligence:
    """Level 5 result. Scores keep row identity. Gaps and baselines stay visible beside them."""

    scores: tuple[RiskScore, ...]
    gaps: tuple[Gap, ...]
    baselines: BaselineBook


def _ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    if denominator == 0:
        return None
    return (numerator / denominator).quantize(RATIO, rounding=ROUND_HALF_EVEN)


def _anomalous(moving_average: Decimal, peer_average: Decimal | None, multiple: Decimal) -> bool:
    if peer_average is None:
        return False
    if peer_average == 0:
        return moving_average > 0
    return moving_average > multiple * peer_average


def _frames(synthesis: Synthesis, window: int) -> dict[int, tuple[int, Decimal]]:
    """Map transaction_id to (count, total) over the time-ordered frame.

    The window walks time, not input order. Equal timestamps break ties by
    the smaller transaction_id, which is stable and independent of insertion.
    """

    by_user: dict[int, list[Hydrated]] = defaultdict(list)
    for row in synthesis.matched:
        by_user[row.transaction.user_id].append(row)

    frames: dict[int, tuple[int, Decimal]] = {}
    for rows in by_user.values():
        ordered = sorted(rows, key=lambda row: (row.transaction.ts, row.transaction.transaction_id))
        for index, row in enumerate(ordered):
            start = max(0, index - (window - 1))
            frame = ordered[start : index + 1]
            total = sum((item.transaction.amount for item in frame), Decimal("0"))
            frames[row.transaction.transaction_id] = (len(frame), total)
    return frames


def level_5(
    synthesis: Synthesis,
    baselines: BaselineBook,
    *,
    window: int = DEFAULT_WINDOW,
    anomaly_multiple: Decimal = DEFAULT_ANOMALY_MULTIPLE,
) -> Intelligence:
    """Score each matched row in place. The baseline is context, not a replacement for the row.

    A window over an already-grouped baseline would answer a different question.
    This level keeps the row, borrows the cohort's sum and count, and excludes
    the row from the normal it is judged against.
    """

    _expect(synthesis, Synthesis, "window accepts only a synthesis from level 3")
    _expect(baselines, BaselineBook, "window accepts only a baseline book from level 4")
    width = _window(window)
    multiple = _multiple(anomaly_multiple)
    frames = _frames(synthesis, width)

    scores: list[RiskScore] = []
    for row in synthesis.matched:
        count, total = frames[row.transaction.transaction_id]
        moving_average = (total / Decimal(count)).quantize(MONEY, rounding=ROUND_HALF_EVEN)
        baseline = baselines.for_cohort(row.profile.cohort_id)
        peer = baseline.peer_average(row.transaction.amount)
        ratio = None if peer is None else _ratio(moving_average, peer)
        scores.append(
            RiskScore(
                transaction_id=row.transaction.transaction_id,
                user_id=row.transaction.user_id,
                cohort_id=row.profile.cohort_id,
                risk_tier=row.profile.risk_tier,
                occurred_at=row.transaction.ts,
                amount=row.transaction.amount,
                moving_count=count,
                moving_total=total,
                moving_average=moving_average,
                peer_average=peer,
                ratio=ratio,
                anomalous=_anomalous(moving_average, peer, multiple),
            )
        )
    return Intelligence(tuple(scores), synthesis.gaps, baselines)


# --- Composition --------------------------------------------------------------


def compose(
    transactions: Iterable[Transaction],
    profiles: Iterable[UserProfile],
    *,
    window: int = DEFAULT_WINDOW,
    anomaly_multiple: Decimal = DEFAULT_ANOMALY_MULTIPLE,
) -> Intelligence:
    """Intelligence = level_5(level_4(level_3(level_2(level_1(facts)))))."""

    ledger = level_1(transactions)
    settled = level_2(ledger)
    synthesis = level_3(settled, profiles)
    baselines = level_4(synthesis)
    return level_5(
        synthesis,
        baselines,
        window=window,
        anomaly_multiple=anomaly_multiple,
    )


def conserves(settled: SettledLedger, report: Intelligence) -> bool:
    """Every settled unit is scored or named as a gap. Baselines account for the scored money.

    Declined money is already outside `settled`. Refusal is allowed to remove
    value from the question. The join is not allowed to lose what remains.
    """

    _expect(settled, SettledLedger, "conservation starts from a settled ledger")
    _expect(report, Intelligence, "conservation checks an intelligence report")
    settled_total = sum((entry.amount for entry in settled.entries), Decimal("0"))
    scored = sum((score.amount for score in report.scores), Decimal("0"))
    gaps = sum((gap.transaction.amount for gap in report.gaps), Decimal("0"))
    baselined = sum((cohort.total for cohort in report.baselines.cohorts), Decimal("0"))
    return scored + gaps == settled_total and baselined == scored


# --- The worked example and the checks that keep it honest -------------------


def _at(day: int, hour: int = 0) -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=day, hours=hour)


def _story() -> tuple[tuple[Transaction, ...], tuple[UserProfile, ...]]:
    """A small ledger with a spike, a refusal, a missing profile, and a cohort of one."""

    transactions = (
        Transaction(1, 1, "10", _at(0), False),
        Transaction(2, 1, "10", _at(1), False),
        Transaction(3, 1, "100", _at(2), False),
        Transaction(4, 1, "5000", _at(2, 1), True),
        Transaction(5, 2, "10", _at(0), False),
        Transaction(6, 3, "50", _at(0), False),
        Transaction(7, 4, "80", _at(0), False),
    )
    profiles = (
        UserProfile(1, "retail", "standard"),
        UserProfile(2, "retail", "standard"),
        UserProfile(4, "solo", "watch"),
    )
    return transactions, profiles


def _raises(label: str, func: object) -> None:
    try:
        func()  # type: ignore[operator]
    except CraftError:
        return
    raise CraftError(f"blueprint check failed: {label} was accepted")


def _check(label: str, condition: bool) -> None:
    if not condition:
        raise CraftError(f"blueprint check failed: {label}")


def _self_check() -> None:
    """Lock the wisdom with examples a later change has to keep true."""

    for number in range(1, 6):
        _check(f"question {number} is answered", answer(number).number == number)
    _raises("a sixth question", lambda: answer(6))
    _check("store is level 1", choose_level("store").number == 1)
    _check("filter is level 2", choose_level(" filter ").number == 2)
    _check("join is level 3", choose_level("join").number == 3)
    _check("baseline is level 4", choose_level("baseline").number == 4)
    _check("window is level 5", choose_level("window").number == 5)
    _raises("an unnamed need", lambda: choose_level("vibes"))

    _check(
        "half-even keeps the even cent",
        _money("1.005") == Decimal("1.00") and _money("1.015") == Decimal("1.02"),
    )
    _raises("float money", lambda: Transaction(1, 1, 1.0, _at(0), False))  # type: ignore[arg-type]
    _raises("bool identity", lambda: Transaction(True, 1, "1", _at(0), False))  # type: ignore[arg-type]
    _raises("naive time", lambda: Transaction(1, 1, "1", datetime(2026, 1, 1), False))
    _raises("negative money", lambda: Transaction(1, 1, "-1", _at(0), False))
    _raises("infinite money", lambda: Transaction(1, 1, "Infinity", _at(0), False))
    _raises("int dressed as a bool", lambda: Transaction(1, 1, "1", _at(0), 1))  # type: ignore[arg-type]
    _raises("a padded key", lambda: UserProfile(1, " retail", "standard"))
    _raises(
        "duplicate transaction identity",
        lambda: level_1(
            (
                Transaction(1, 1, "1", _at(0), False),
                Transaction(1, 1, "2", _at(1), False),
            )
        ),
    )

    transactions, profiles = _story()
    ledger = level_1(transactions)
    settled = level_2(ledger)
    _raises("joining before the filter", lambda: level_3(ledger, profiles))  # type: ignore[arg-type]
    _check("the gate refused the declined charge", [entry.transaction_id for entry in settled.entries] == [1, 2, 3, 5, 6, 7])

    report = compose(transactions, profiles)
    synthesis = level_3(settled, profiles)
    manual = level_5(synthesis, level_4(synthesis))
    _check("composition matches the separate levels", report == manual)
    _check("settled value is conserved", conserves(settled, report))
    _check("declined money never becomes a score or a gap", all(item != 4 for item in _ids(report)))
    _check("retail normal excludes the declined 5000", report.baselines.for_cohort("retail") == CohortBaseline("retail", 4, Decimal("130.00")))
    _check("a cohort of one is remembered as one", report.baselines.for_cohort("solo") == CohortBaseline("solo", 1, Decimal("80.00")))

    by_id = {score.transaction_id: score for score in report.scores}
    _check("the window sees the two predecessors", by_id[3].moving_total == Decimal("120.00") and by_id[3].moving_count == 3)
    _check("the spike is judged against peers of 10", by_id[3].peer_average == Decimal("10.00") and by_id[3].ratio == Decimal("4.0000") and by_id[3].anomalous)
    _check("an ordinary row is not a surprise", by_id[1].peer_average == Decimal("40.00") and not by_id[1].anomalous and by_id[1].moving_total == Decimal("10.00"))
    _check("the second row sees only its real past", by_id[2].moving_total == Decimal("20.00") and by_id[2].moving_count == 2)
    _check("a solo cohort is not guessed", by_id[7].peer_average is None and by_id[7].ratio is None and not by_id[7].anomalous)
    _check("risk tier is carried for the next policy", by_id[7].risk_tier == "watch")
    _check("the missing profile is a named gap", len(report.gaps) == 1 and report.gaps[0].transaction.transaction_id == 6 and "user_id=3" in report.gaps[0].reason)
    _check("only the spike is anomalous", [score.transaction_id for score in report.scores if score.anomalous] == [3])

    _check_time_order()
    _check_tie_break()
    _check_peer_of_zero()
    _check_edges()


def _ids(report: Intelligence) -> list[int]:
    return [score.transaction_id for score in report.scores] + [
        gap.transaction.transaction_id for gap in report.gaps
    ]


def _check_time_order() -> None:
    """Input order is the score order. The window still walks time."""

    base = _at(0)
    transactions = (
        Transaction(2, 1, "10", base + timedelta(days=1), False),
        Transaction(1, 1, "30", base, False),
    )
    profiles = (UserProfile(1, "c", "t"),)
    report = compose(transactions, profiles, window=2)
    by_id = {score.transaction_id: score for score in report.scores}
    _check("scores follow the settled input", [score.transaction_id for score in report.scores] == [2, 1])
    _check("the later row sees the earlier amount", by_id[2].moving_total == Decimal("40.00"))
    _check("the earlier row does not see the future", by_id[1].moving_total == Decimal("30.00"))


def _check_tie_break() -> None:
    stamp = _at(0)
    transactions = (
        Transaction(10, 1, "5", stamp, False),
        Transaction(9, 1, "7", stamp, False),
    )
    report = compose(transactions, (UserProfile(1, "c", "t"),), window=2)
    by_id = {score.transaction_id: score for score in report.scores}
    _check("the smaller identity is the earlier neighbor", by_id[9].moving_total == Decimal("7.00") and by_id[10].moving_total == Decimal("12.00"))


def _check_peer_of_zero() -> None:
    transactions = (
        Transaction(1, 1, "0", _at(0), False),
        Transaction(2, 2, "0", _at(0), False),
        Transaction(3, 3, "5", _at(0), False),
    )
    profiles = (
        UserProfile(1, "z", "t"),
        UserProfile(2, "z", "t"),
        UserProfile(3, "z", "t"),
    )
    report = compose(transactions, profiles, window=1)
    by_id = {score.transaction_id: score for score in report.scores}
    _check("a positive row among zero peers is anomalous without a fake ratio", by_id[3].peer_average == Decimal("0.00") and by_id[3].ratio is None and by_id[3].anomalous)
    _check("a zero row is not a surprise", not by_id[1].anomalous)


def _check_edges() -> None:
    empty = compose((), ())
    _check("an empty question has an empty answer", empty.scores == () and empty.gaps == () and empty.baselines.cohorts == ())

    unmatched = compose((Transaction(1, 9, "50", _at(0), False),), ())
    _check("a missing profile conserves the settled amount as a gap", len(unmatched.gaps) == 1 and unmatched.baselines.cohorts == ())
    _check(
        "conservation holds for a total gap",
        conserves(level_2(level_1((Transaction(1, 9, "50", _at(0), False),))), unmatched),
    )

    declined_unknown = (
        Transaction(1, 9, "50", _at(0), True),
        Transaction(2, 1, "10", _at(0), False),
    )
    profiles = (UserProfile(1, "retail", "standard"),)
    settled = level_2(level_1(declined_unknown))
    report = compose(declined_unknown, profiles)
    _check("a declined unknown user is refused before it can become a gap", report.gaps == () and conserves(settled, report))

    _raises("a zero window", lambda: compose(_story()[0], _story()[1], window=0))
    _raises("a float multiple", lambda: compose(_story()[0], _story()[1], anomaly_multiple=3))  # type: ignore[arg-type]
    _raises(
        "two profiles for one user",
        lambda: level_3(
            level_2(level_1((Transaction(1, 1, "10", _at(0), False),))),
            (UserProfile(1, "a", "t"), UserProfile(1, "b", "t")),
        ),
    )


def _print_blueprint(report: Intelligence, ledger: Ledger, settled: SettledLedger) -> None:
    print("The craft of programming in Python")
    print("Intelligence = level_5(level_4(level_3(level_2(level_1(facts)))))")
    print()
    for level in LEVELS:
        print(f"{level.number}. {level.question}")
        print(f"   {level.wisdom}")
    print()
    print("Rules you can build on")
    for rule in RULES:
        print(f"   - {rule}")
    print()
    print(f"Level 1  {len(ledger.entries)} facts")
    print(f"Level 2  {len(settled.entries)} settled, {len(ledger.entries) - len(settled.entries)} refused")
    print(f"Level 3  {len(report.scores)} hydrated, {len(report.gaps)} gap")
    print("Level 4  " + "; ".join(f"{cohort.cohort_id} total {cohort.total} over {cohort.count}" for cohort in report.baselines.cohorts))
    print("Level 5")
    for score in report.scores:
        peer = "none" if score.peer_average is None else f"{score.peer_average}"
        flag = " anomalous" if score.anomalous else ""
        print(
            f"   tx {score.transaction_id} user {score.user_id} "
            f"amount {score.amount} moving {score.moving_total} "
            f"peer {peer}{flag}"
        )
    for gap in report.gaps:
        print(f"   gap tx {gap.transaction.transaction_id}: {gap.reason}")
    print()
    print("Blueprint holds. Extend a level, or read Intelligence. Leave level 1 closed.")


def main() -> None:
    """Run the blueprint checks, then print the worked example."""

    _self_check()
    transactions, profiles = _story()
    ledger = level_1(transactions)
    settled = level_2(ledger)
    _print_blueprint(compose(transactions, profiles), ledger, settled)


if __name__ == "__main__":
    main()
