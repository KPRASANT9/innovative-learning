"""Python: the craft of the language, as a map you can use.

Sibling of SQL.md. That note is how a question moves through data.
This one is the language itself, from a single value up to a verb
that acts on other verbs. Climb only as far as the question.

    {Result} = L5( L4( L3( L2( L1( value ) ) ) ) )

The pictures are the framework. LAYER_LADDER is the descent from
higher order down to the value. ELEMENT_MAP is every core element
in its layer. USE_DIAGRAM is how you choose, with ease.

                 [ L5: HIGHER ORDER ]
                            |
              (map, filter, reduce, compose,
               generator, decorator)
                            |
                            v
                 [ L4: THE BOUNDARY ]
                            |
           (function, protocol, class, with,
            raise: the name hides the shape)
                            |
                            v
               [ L3: ADT OPERATIONS ]
                            |
        (index, slice, get, add, push, pop,
         union, heappop, unpack, iterate)
                            |
                            v
               [ L2: DATA STRUCTURES ]
                            |
         (list, tuple, dict, set, deque, heap)
                            |
                            v
                 [ L1: DATA TYPES ]
                            |
        (int, bool, str, bytes, Decimal, None)
                            |
                            v
                      [ THE VALUE ]
"""

from __future__ import annotations

import array
import heapq
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from functools import reduce
from typing import Callable, Iterable


CELL_W = 22
GAP = "  "
CANVAS = 4 * CELL_W + 3 * len(GAP)


class CraftError(Exception):
    """The framework was asked to guess, or a picture broke its frame."""


@dataclass(frozen=True, slots=True)
class Layer:
    """One altitude of the language, and when to stop climbing."""

    number: int
    name: str
    question: str
    you_have: str
    you_pick: str
    stop_when: str
    wisdom: str


LAYERS: tuple[Layer, ...] = (
    Layer(
        1,
        "DATA TYPES",
        "What is this one value?",
        "a raw atom crossing the edge of the program",
        "int, bool, float, complex, Decimal, Fraction, str, bytes, None, datetime",
        "the question is about that single value",
        "Give the value a type that can carry its law: exactness, order, text, octets, truth, or absence.",
    ),
    Layer(
        2,
        "DATA STRUCTURES",
        "How will these values be asked for?",
        "many values, and a way you intend to reach them",
        "list, tuple, range, dict, set, frozenset, deque, heap",
        "one shape answers the access, and only this place uses it",
        "Choose the shape by the access law: position, key, membership, either end, or the next extreme.",
    ),
    Layer(
        3,
        "ADT OPERATIONS",
        "Which verb does that shape allow?",
        "a structure and one question to ask it",
        "index, slice, get, add, push, pop, union, heappop, unpack, iterate",
        "the verb is used in one place",
        "Use the verb that belongs to the shape. The spelling of `in` is shared; the law under it is not.",
    ),
    Layer(
        4,
        "THE BOUNDARY",
        "Who is allowed to see the container?",
        "a verb that more than one caller needs",
        "a function, a protocol, a dataclass, a raised error, a with-block",
        "callers can depend on the name, and the verb is not being lifted across a whole collection",
        "Name the verb, and let the name hide the container.",
    ),
    Layer(
        5,
        "HIGHER ORDER",
        "Does this verb apply to many values, or to other verbs?",
        "a verb that repeats across items, or a verb whose subject is another verb",
        "map, filter, reduce, comprehension, generator, partial, compose, decorator",
        "the lift itself is the whole question",
        "Lift a verb across items, or a verb across verbs. Otherwise you have already climbed far enough.",
    ),
)

RULES: tuple[str, ...] = (
    "Pick the type before the structure.",
    "Pick the structure by the access law you will actually use.",
    "A queue is popleft on a deque. The end of a list is a stack.",
    "Membership walks a sequence and hashes a set or a dict.",
    "A key is hashable and stays unchanged for its whole life in the structure.",
    "Name a verb the moment a second caller needs it.",
    "A comprehension returns a collection. A generator waits to be asked. compose runs the inner verb first.",
    "None is absence. A broken promise raises. An empty structure is empty.",
)


@dataclass(frozen=True, slots=True)
class DataType:
    name: str
    family: str
    mutable: bool
    hashable: bool
    law: str


TYPES: tuple[DataType, ...] = (
    DataType("int", "number", False, True, "Exact integer, unbounded."),
    DataType("bool", "truth", False, True, "A truth value. It subclasses int; keep it for truth."),
    DataType("float", "number", False, True, "A binary approximation. Right for measurement, wrong for money."),
    DataType("complex", "number", False, True, "Real and imaginary parts. It has no order."),
    DataType("Decimal", "number", False, True, "Exact base-10. The type for money and decimal facts."),
    DataType("Fraction", "number", False, True, "An exact ratio of two integers."),
    DataType("str", "text", False, True, "Unicode text. Indexing it yields characters."),
    DataType("bytes", "octets", False, True, "Immutable octets. Text arrives only through an encoding."),
    DataType("bytearray", "octets", True, False, "Mutable octets."),
    DataType("None", "absence", False, True, "The single value that means absence."),
    DataType("datetime", "time", False, True, "A moment. Finish it with a timezone."),
)


@dataclass(frozen=True, slots=True)
class Structure:
    name: str
    access: str
    verb: str
    mutable: bool
    law: str


STRUCTURES: tuple[Structure, ...] = (
    Structure("list", "position", "items[i]; items.append(x)", True, "Ordered and mutable. Membership walks. It cannot be a key."),
    Structure("tuple", "position", "record[i]; a, b = record", False, "Fixed sequence. A record when each index has a meaning. Hashable when its items are."),
    Structure("range", "position", "range(start, stop)", False, "An arithmetic progression. It stores the bounds, not the integers."),
    Structure("str", "position", "text[i]", False, "A value that is also a sequence of characters."),
    Structure("bytes", "position", "buf[i]", False, "A value that is also a sequence of octets."),
    Structure("dict", "key", "mapping[key]", True, "Key to value, in insertion order. The key is hashable and stays unchanged."),
    Structure("set", "membership", "item in pool; a & b", True, "Unique hashable items. Unordered."),
    Structure("frozenset", "membership", "item in pool", False, "An immutable set. It may itself be a key."),
    Structure("deque", "both ends", "d.append(x); d.popleft()", True, "Either end is O(1). This is the queue."),
    Structure("heap", "next extreme", "heapq.heappop(heap)", True, "A list kept in heap order. The smallest comes out first."),
    Structure("Counter", "key", "Counter(items)[item]", True, "A mapping from item to count. A multiset."),
    Structure("defaultdict", "key", "groups[key].append(x)", True, "A mapping that builds a missing value. A plain dict raises instead."),
    Structure("array", "position", 'array.array("i", numbers)', True, "Packed, homogeneous atoms. A list holds references; this holds the atoms."),
)


@dataclass(frozen=True, slots=True)
class Operation:
    name: str
    spelling: str
    law: str


@dataclass(frozen=True, slots=True)
class ADT:
    """A set of verbs. The structure behind them is a costume."""

    name: str
    purpose: str
    operations: tuple[Operation, ...]
    title: str = ""
    cell: tuple[str, str] | None = None
    row: int | None = None
    column: int | None = None

    def label(self) -> str:
        return self.title or self.name


def _ops(*rows: tuple[str, str, str]) -> tuple[Operation, ...]:
    return tuple(Operation(name, spelling, law) for name, spelling, law in rows)


ADTS: tuple[ADT, ...] = (
    ADT(
        "sequence",
        "Read by position, in order.",
        _ops(
            ("length", "len(items)", "The number of items."),
            ("index", "items[i]", "From the start. A negative index counts from the end."),
            ("slice", "items[i:j]", "A sequence operation that returns a sequence."),
            ("concat", "left + right", "A new sequence. Concat does not extend a list in place."),
            ("iterate", "for item in items", "The structure yields items in its own order."),
            ("contains", "item in items", "On a sequence, membership walks."),
            ("unpack", "a, b = items", "The names and the items agree in count."),
        ),
        cell=("index, slice", "iterate, unpack"),
        row=0,
        column=0,
    ),
    ADT(
        "list",
        "A sequence that grows, usually at the end.",
        _ops(
            ("append", "items.append(x)", "Grow at the end."),
            ("extend", "items.extend(more)", "Absorb another sequence at the end."),
            ("insert", "items.insert(i, x)", "Open a hole at a position. The tail moves."),
            ("pop", "items.pop()", "Take the end. pop(0) walks; a queue does not live here."),
            ("sort", "items.sort()", "Order in place. sorted(items) returns a new list."),
        ),
    ),
    ADT(
        "stack",
        "Last in, first out. The end of a list is the top.",
        _ops(
            ("push", "stack.append(x)", "The new top sits at the end."),
            ("pop", "stack.pop()", "The latest item comes back first."),
            ("peek", "stack[-1]", "Look at the top and leave it there."),
        ),
        cell=("append", "pop, peek"),
        row=1,
        column=0,
    ),
    ADT(
        "queue",
        "First in, first out. A deque, with the exit at the left.",
        _ops(
            ("enqueue", "queue.append(x)", "Arrive at the right."),
            ("dequeue", "queue.popleft()", "Leave from the left."),
            ("peek", "queue[0]", "The next item to leave, still waiting."),
        ),
        cell=("append", "popleft"),
        row=1,
        column=1,
    ),
    ADT(
        "deque",
        "Both ends, each in constant time.",
        _ops(
            ("append", "d.append(x)", "Grow at the right."),
            ("appendleft", "d.appendleft(x)", "Grow at the left."),
            ("pop", "d.pop()", "Shrink at the right."),
            ("popleft", "d.popleft()", "Shrink at the left."),
        ),
        cell=("appendleft", "pop either end"),
        row=1,
        column=2,
    ),
    ADT(
        "mapping",
        "Reach a value by a hashable key.",
        _ops(
            ("put", "mapping[key] = value", "The key stays unchanged while it lives here."),
            ("get", "mapping.get(key, default)", "A bare mapping[key] raises when the key is absent."),
            ("delete", "del mapping[key]", "Remove the pair."),
            ("contains", "key in mapping", "A hash lookup, not a walk."),
            ("items", "mapping.items()", "Key and value together, in insertion order."),
        ),
        cell=("get, put, del", "key in mapping"),
        row=0,
        column=1,
    ),
    ADT(
        "set",
        "Membership, uniqueness, and the algebra of collections.",
        _ops(
            ("add", "pool.add(x)", "A second add of an equal item changes nothing."),
            ("discard", "pool.discard(x)", "Absence is a no-op. remove raises."),
            ("contains", "x in pool", "A hash lookup."),
            ("union", "a | b", "Items that live in either."),
            ("intersection", "a & b", "Items that live in both."),
            ("difference", "a - b", "Items that live only in a."),
            ("symmetric", "a ^ b", "Items that live in one side only."),
            ("subset", "a <= b", "Every item of a is an item of b."),
        ),
        cell=("add, discard", "&  |  -  ^"),
        row=0,
        column=2,
    ),
    ADT(
        "priority queue",
        "Always extract the smallest.",
        _ops(
            ("push", "heapq.heappush(heap, x)", "Keep the heap ordered as the item arrives."),
            ("pop", "heapq.heappop(heap)", "The smallest item."),
            ("peek", "heap[0]", "The smallest, left in place. The heap must not be empty."),
            ("heapify", "heapq.heapify(items)", "Turn a list into a heap in place."),
        ),
        title="heap",
        cell=("heappush", "heappop"),
        row=0,
        column=3,
    ),
    ADT(
        "record",
        "A fixed shape. Position or field, never a growing end.",
        _ops(
            ("construct", "Point(x, y)", "A tuple when names would be noise. A dataclass when the law belongs in construction."),
            ("project", "point.x", "A tuple projects by index: record[0]."),
            ("unpack", "x, y = record", "Bind each part in one step."),
        ),
        cell=("field, unpack", "fixed shape"),
        row=1,
        column=3,
    ),
    ADT(
        "iterator",
        "The one traversal every structure shares.",
        _ops(
            ("iter", "iter(items)", "Ask a structure for its stream."),
            ("next", "next(stream)", "StopIteration ends a finite stream."),
        ),
    ),
    ADT(
        "higher order",
        "A verb applied to values, or to other verbs.",
        _ops(
            ("map", "map(verb, items)", "The same verb, each item, lazily."),
            ("filter", "filter(keep, items)", "Items that pass the test, lazily."),
            ("reduce", "reduce(combine, items, start)", "Fold the items into one value."),
            ("comprehend", "[verb(x) for x in items if keep(x)]", "Map and filter that return a collection."),
            ("generate", "(verb(x) for x in items)", "A sequence that does not exist until asked. yield suspends one step."),
            ("partial", "partial(verb, fixed)", "Fix some arguments. Leave the rest open."),
            ("compose", "compose(outer, inner)(value)", "Inner runs first. This is L5(L4(...(value)))."),
            ("decorate", "@boundary", "compose, applied when the function is defined."),
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class Element:
    """A law of the language that is not itself a container."""

    name: str
    layer: int
    spelling: str
    law: str


ELEMENTS: tuple[Element, ...] = (
    Element("binding", 1, "name = value", "A name is a bond to a value. Rebinding the name does not edit the value."),
    Element("equality", 1, "a == b", "Equality asks whether two values agree."),
    Element("identity", 1, "a is b", "Identity asks whether two names share one object. Reserve it for None and sentinels."),
    Element("truth", 1, "bool(value)", "None, False, zero, and empty containers are false. That test is not a type check."),
    Element("encode", 1, 'text.encode("utf-8")', "Text and octets meet at an encoding you write down."),
    Element("hash", 2, "hash(value)", "Hashable values may be keys and set members. They stay unchanged."),
    Element("copy", 2, "items.copy()", "Copying a structure copies the references it holds, not the inner objects."),
    Element("function", 4, "def verb(value): ...", "Name the operation. Callers receive the verb, not the container."),
    Element("protocol", 4, "collections.abc.Mapping", "An ADT written as the operations a caller may rely on."),
    Element("dataclass", 4, "@dataclass(frozen=True)", "A named record. Construction is where its law lives."),
    Element("exception", 4, "raise ValueError(reason)", "A broken promise. Absence stays None. Failure raises."),
    Element("context", 4, "with resource as handle:", "Acquire and release are one shape."),
    Element("namespace", 4, "local, enclosing, global, built-in", "A name resolves outward in that order."),
    Element("mutable default", 4, "def verb(items=None):", "A default is born once. Build a fresh mutable inside the function."),
    Element("closure", 5, "def adder(n): return lambda x: x + n", "A function keeps the bindings it was born with."),
    Element("recursion", 5, "def walk(node): ... walk(child)", "A verb defined on a smaller value of the same shape."),
)


@dataclass(frozen=True, slots=True)
class Choice:
    """One need, and the element that answers it without a climb too far."""

    need: str
    aliases: tuple[str, ...]
    layer: int
    element: str
    adt: str
    operations: tuple[str, ...]
    spelling: str
    why: str


CHOICES: tuple[Choice, ...] = (
    Choice("integer", ("count", "int"), 1, "int", "", ("construct",), "int(text)", "An exact count or index."),
    Choice("truth", ("flag", "bool"), 1, "bool", "", ("construct",), "True", "A yes or a no. Keep arithmetic off it."),
    Choice("money", ("decimal", "exact decimal"), 1, "Decimal", "", ("construct",), 'Decimal("10.20")', "Base-10 facts, including money."),
    Choice("ratio", ("fraction",), 1, "Fraction", "", ("construct",), "Fraction(1, 3)", "An exact ratio of integers."),
    Choice("approximation", ("float", "measurement"), 1, "float", "", ("construct",), "float(text)", "A measured quantity, where binary approximation is acceptable."),
    Choice("text", ("string", "str"), 1, "str", "sequence", ("index", "iterate"), "text", "Whole text is the value. Index only when you mean characters."),
    Choice("octets", ("bytes", "binary"), 1, "bytes", "sequence", ("index",), 'b"octets"', "Raw octets, already encoded."),
    Choice("absence", ("nothing", "none"), 1, "None", "", ("identity",), "None", "Absence of a value. A failed promise is an exception."),
    Choice("moment", ("time", "datetime"), 1, "datetime", "", ("construct",), "datetime(2026, 1, 1, tzinfo=timezone.utc)", "A finished moment carries a timezone."),
    Choice("record", ("fixed", "tuple"), 2, "tuple", "record", ("construct", "project", "unpack"), "(x, y)", "The length is part of the meaning."),
    Choice("named record", ("dataclass",), 4, "dataclass", "record", ("construct", "project"), "@dataclass(frozen=True)", "The parts have names, and construction keeps the law."),
    Choice("sequence", ("ordered", "list", "grow at the end"), 2, "list", "list", ("append", "extend"), "items.append(x); items[i]", "Order matters, and the collection grows at the end."),
    Choice("both ends", ("deque",), 2, "deque", "deque", ("append", "appendleft", "pop", "popleft"), "deque([a, b])", "Growth or shrinkage happens at both ends."),
    Choice("stack", ("lifo", "last in first out"), 3, "list", "stack", ("push", "pop", "peek"), "stack.append(x); stack.pop()", "The latest arrival is the next to leave."),
    Choice("queue", ("fifo", "first in first out"), 3, "deque", "queue", ("enqueue", "dequeue", "peek"), "q.append(x); q.popleft()", "The earliest arrival is the next to leave."),
    Choice("lookup", ("key", "dict", "mapping"), 2, "dict", "mapping", ("put", "get", "contains"), "m[key] = value", "The question is the key, and the answer is the value."),
    Choice("membership", ("unique", "set"), 2, "set", "set", ("add", "contains", "intersection"), "pool.add(x); a & b", "Uniqueness, or the algebra of who belongs."),
    Choice("frozen membership", ("frozenset",), 2, "frozenset", "set", ("contains", "union"), "frozenset(items)", "A set that must be shared or used as a key."),
    Choice("next extreme", ("priority", "heap", "smallest"), 3, "heap", "priority queue", ("push", "pop", "peek"), "heapq.heappush(h, x); heapq.heappop(h)", "Each extraction wants the smallest waiting item."),
    Choice("count items", ("multiset", "counter"), 2, "Counter", "mapping", ("put", "get"), "Counter(items)", "Each item answers with how many times it appeared."),
    Choice("missing key", ("default factory", "defaultdict"), 2, "defaultdict", "mapping", ("get", "put"), "defaultdict(list)", "Every missing key should be born the same way."),
    Choice("dense integers", ("array", "packed"), 2, "array", "sequence", ("index",), 'array.array("i", numbers)', "The atoms are uniform and should sit packed, not boxed."),
    Choice("progression", ("range",), 2, "range", "sequence", ("index", "iterate"), "range(start, stop)", "The integers follow from a start, a stop, and a step."),
    Choice("encode", ("text as octets", "decode"), 1, "encode", "", ("encode",), 'text.encode("utf-8")', "Cross the text and octets boundary with the encoding visible."),
    Choice("walk", ("iterate", "loop"), 3, "iterator", "iterator", ("iter", "next"), "for item in items", "Visit each item. The structure decides the order."),
    Choice("name the verb", ("hide", "function", "boundary"), 4, "function", "", ("call",), "def verb(items): ...", "More than one caller needs the operation."),
    Choice("protocol", ("abc", "interface"), 4, "protocol", "", ("call",), "collections.abc.Mapping", "Callers may rely on the verbs, and on nothing behind them."),
    Choice("failure", ("exception", "raise"), 4, "exception", "", ("raise",), "raise ValueError(reason)", "The operation cannot keep its promise."),
    Choice("resource", ("with", "context"), 4, "context", "", ("enter",), "with resource as handle:", "Something is acquired and must be released."),
    Choice("lift", ("every item", "comprehension", "map over"), 5, "higher order", "higher order", ("comprehend", "map", "filter"), "[verb(x) for x in items]", "One verb applies to every item, and you want the collection."),
    Choice("lazy", ("generator", "yield"), 5, "higher order", "higher order", ("generate",), "(verb(x) for x in items)", "The items are produced when a consumer asks."),
    Choice("compose verbs", ("pipeline", "compose"), 5, "higher order", "higher order", ("compose",), "compose(outer, inner)(value)", "One verb's result is the next verb's input. Inner runs first."),
    Choice("decorate", ("decorator",), 5, "higher order", "higher order", ("decorate",), "@boundary", "A verb should be wrapped at the moment it is defined."),
    Choice("fresh container", ("mutable default",), 4, "mutable default", "", ("construct",), "def verb(items=None):", "Each call needs its own list, dict, or set."),
)

AMBIGUOUS: dict[str, str] = {
    "map": "say 'lookup' for a dict, or 'lift' to apply a verb across items",
}


def _norm(need: str) -> str:
    return " ".join(need.split()).lower()


def _index_choices() -> dict[str, Choice]:
    index: dict[str, Choice] = {}
    for choice in CHOICES:
        keys = (choice.need, *choice.aliases)
        for key in keys:
            folded = _norm(key)
            if folded in index:
                raise CraftError(f"need alias collides: {key}")
            index[folded] = choice
    return index


_BY_NEED = _index_choices()


def choose(need: str) -> Choice:
    """Name the need in plain words. Receive the layer, the element, and the verb."""

    if not isinstance(need, str):
        raise CraftError("name the need with a string")
    key = _norm(need)
    if key in AMBIGUOUS:
        raise CraftError(AMBIGUOUS[key])
    try:
        return _BY_NEED[key]
    except KeyError as exc:
        known = ", ".join(choice.need for choice in CHOICES)
        raise CraftError(f"unknown need {need!r}. The framework knows: {known}") from exc


def known_needs() -> tuple[str, ...]:
    """The canonical needs. Aliases reach the same choices."""

    return tuple(choice.need for choice in CHOICES)


def flow(value: object, *steps: Callable[[object], object]) -> object:
    """Move a value left to right. The first step is the inner one, closest to the value."""

    for step in steps:
        value = step(value)
    return value


def compose(*steps: Callable[[object], object]) -> Callable[[object], object]:
    """Inside-out form. compose(L5, L4, L3, L2, L1)(value) applies L1 first.

    {Result} = L5( L4( L3( L2( L1( value ) ) ) ) )
    """

    def applied(value: object) -> object:
        return flow(value, *reversed(steps))

    return applied


def _pad(line: str, width: int = CANVAS) -> str:
    if len(line) > width:
        raise CraftError(f"diagram line is wider than the frame: {line}")
    return line.center(width)


def _box(lines: Iterable[str], width: int) -> list[str]:
    body = tuple(lines)
    inner = width - 2
    for line in body:
        if len(line) > inner:
            raise CraftError(f"diagram line is wider than its box: {line}")
    bar = "+" + "-" * inner + "+"
    return [bar, *(f"|{line.center(inner)}|" for line in body), bar]


def _row(cells: Iterable[tuple[str, ...]]) -> list[str]:
    boxes = [_box(lines, CELL_W) for lines in cells]
    height = max(len(box) for box in boxes)
    padded: list[list[str]] = []
    for box in boxes:
        blank = " " * CELL_W
        pad = height - len(box)
        padded.append(box + [blank] * pad)
    return [GAP.join(box[i] for box in padded) for i in range(height)]


def _arrow(label: str) -> list[str]:
    return [_pad(label), _pad("|"), _pad("v")]


def _cells_by_row() -> tuple[tuple[tuple[str, ...], ...], ...]:
    placed = [adt for adt in ADTS if adt.row is not None]
    rows = sorted({adt.row for adt in placed})
    picture: list[tuple[tuple[str, ...], ...]] = []
    for row in rows:
        in_row = sorted((adt for adt in placed if adt.row == row), key=lambda adt: adt.column or 0)
        columns = [adt.column for adt in in_row]
        if columns != list(range(4)):
            raise CraftError(f"layer picture row {row} is missing a column")
        picture.append(tuple((adt.label(), *adt.cell) for adt in in_row if adt.cell is not None))
    return tuple(picture)


def element_map() -> str:
    """The language drawn as layers: higher order on top, the value at the bottom."""

    l2_names = (
        (("list", "tuple", "range"), "by position"),
        (("dict",), "by key"),
        (("set", "frozenset"), "by membership"),
        (("deque", "heap"), "ends, extreme"),
    )
    lines = [
        _pad("THE LANGUAGE, LAYER BY LAYER"),
        _pad("{Result} = L5( L4( L3( L2( L1( value ) ) ) ) )"),
        _pad("Climb only as far as the question."),
        "",
        *_box(
            (
                "L5   HIGHER ORDER",
                "map   filter   reduce   compose",
                "comprehension   generator   decorator",
                "a verb across values, or across verbs",
            ),
            CANVAS,
        ),
        *_arrow("lift a named verb"),
        *_box(
            (
                "L4   THE BOUNDARY",
                "function   protocol   dataclass",
                "exception   context manager",
                "the caller sees the verb, not the list",
            ),
            CANVAS,
        ),
        *_arrow("a name for a lawful verb"),
        _pad("L3   ADT OPERATIONS"),
    ]
    for row in _cells_by_row():
        lines.extend(_row(row))
    lines.extend(
        [
            *_arrow("a shape for each access law"),
            _pad("L2   DATA STRUCTURES"),
            *_row(tuple((", ".join(names), subtitle) for names, subtitle in l2_names)),
            *_arrow("each item is a typed value"),
            *_box(
                (
                    "L1   DATA TYPES",
                    "int   bool   float   complex   Decimal   Fraction",
                    "str   bytes   bytearray   None   datetime",
                    "str and bytes are values, and also sequences",
                ),
                CANVAS,
            ),
            *_arrow("born as one honest value"),
            _pad("[ THE VALUE ]"),
        ]
    )
    return "\n".join(lines)


ELEMENT_MAP = element_map()

LAYER_LADDER = """\
                 [ L5: HIGHER ORDER ]
                            |
              (map, filter, reduce, compose,
               generator, decorator)
                            |
                            v
                 [ L4: THE BOUNDARY ]
                            |
           (function, protocol, class, with,
            raise: the name hides the shape)
                            |
                            v
               [ L3: ADT OPERATIONS ]
                            |
        (index, slice, get, add, push, pop,
         union, heappop, unpack, iterate)
                            |
                            v
               [ L2: DATA STRUCTURES ]
                            |
         (list, tuple, dict, set, deque, heap)
                            |
                            v
                 [ L1: DATA TYPES ]
                            |
        (int, bool, str, bytes, Decimal, None)
                            |
                            v
                      [ THE VALUE ]
"""

def _ink(marks: dict[int, str]) -> str:
    """One picture row. Marks are column to character, on a blank canvas."""

    line = [" "] * CANVAS
    for column, glyph in marks.items():
        if not 0 <= column < CANVAS:
            raise CraftError(f"diagram mark falls outside the frame: {column}")
        line[column] = glyph
    return "".join(line)


def _span(start: int, stop: int, joints: tuple[int, ...] = ()) -> str:
    """A horizontal rule from start to stop, inclusive, with + at the joints."""

    lo, hi = sorted((start, stop))
    marks = {column: "-" for column in range(lo, hi + 1)}
    marks[lo] = "+"
    marks[hi] = "+"
    for joint in joints:
        marks[joint] = "+"
    return _ink(marks)


def _stems(columns: tuple[int, ...], glyph: str) -> str:
    return _ink({column: glyph for column in columns})


def _center_block(block: list[str]) -> list[str]:
    width = len(block[0])
    side = (CANVAS - width) // 2
    if side < 0 or any(len(line) != width for line in block):
        raise CraftError("a diagram block does not fit the frame")
    return [f"{' ' * side}{line}{' ' * (CANVAS - width - side)}" for line in block]


def _lbox(title: tuple[str, ...], rows: tuple[str, ...], width: int) -> list[str]:
    inner = width - 2
    bar = "+" + "-" * inner + "+"
    body = ["|" + line.center(inner) + "|" for line in title]
    body.append("|" + (" " * inner) + "|")
    for row in rows:
        padded = f"  {row}"
        if len(padded) > inner:
            raise CraftError(f"diagram row is wider than its panel: {row}")
        body.append("|" + padded.ljust(inner) + "|")
    return [bar, *body, bar]


def _cbox(lines: tuple[str, ...], width: int) -> list[str]:
    inner = width - 2
    bar = "+" + "-" * inner + "+"
    return [bar, *("|" + line.center(inner) + "|" for line in lines), bar]


def _pair(left: list[str], right: list[str], gap: int) -> tuple[list[str], int, int]:
    """Place two blocks on one row. Return the row and each block's center column."""

    height = max(len(left), len(right))
    left_width = len(left[0])
    right_width = len(right[0])
    left = left + [" " * left_width] * (height - len(left))
    right = right + [" " * right_width] * (height - len(right))
    used = left_width + gap + right_width
    side = (CANVAS - used) // 2
    if side < 0:
        raise CraftError("diagram panels do not fit side by side")
    tail = CANVAS - used - side
    mid = " " * gap
    rows = [f"{' ' * side}{a}{mid}{b}{' ' * tail}" for a, b in zip(left, right)]
    left_center = side + left_width // 2
    right_center = side + left_width + gap + right_width // 2
    return rows, left_center, right_center


def _labeled(label: str, value: str, label_width: int = 14) -> str:
    return f"{label:<{label_width}}{value}"


def use_diagram() -> str:
    """The framework as a picture: one value or many, then climb only if you must."""

    one_value = _lbox(
        ("ONE VALUE", "a type, then stop at L1"),
        (
            _labeled("exact", "int, Decimal, Fraction"),
            _labeled("truth", "bool, None"),
            _labeled("text", "str"),
            _labeled("octets", "bytes"),
            _labeled("time", "datetime, with a zone"),
            _labeled("encode", 'text.encode("utf-8")'),
            _labeled("absence", "None is not a failure"),
        ),
        46,
    )
    many_values = _lbox(
        ("MANY VALUES", "an access law, then L2"),
        (
            _labeled("position", "list, tuple, range"),
            _labeled("key", "dict"),
            _labeled("membership", "set, frozenset"),
            _labeled("both ends", "deque"),
            _labeled("extreme", "heap, smallest out"),
            _labeled("stack", "append, then pop"),
            _labeled("queue", "append, then popleft"),
        ),
        46,
    )
    panels, left_center, right_center = _pair(one_value, many_values, gap=2)
    fork = (left_center + right_center) // 2
    stay_rows, no_center, yes_center = _pair(
        _cbox(("no", "L3  use the verb", "in this one place"), 30),
        _cbox(("yes", "L4  name the verb", "function or protocol"), 30),
        gap=8,
    )
    stop_rows, stop_center, lift_center = _pair(
        _cbox(("no", "stop here", "the name suffices", "climb no further"), 28),
        _cbox(("yes", "L5  lift it", "map  filter  reduce", "generator  compose"), 28),
        gap=8,
    )
    lift_fork = (stop_center + lift_center) // 2
    lines = [
        _pad("HOW TO USE THE ELEMENTS"),
        _pad("Climb only as far as the question."),
        "",
        *panels,
        _stems((left_center, right_center), "|"),
        _span(left_center, right_center, (fork,)),
        _stems((fork,), "|"),
        _stems((fork,), "v"),
        *_center_block(_cbox(("Do other callers need this verb?",), 46)),
        _stems((fork,), "|"),
        _span(no_center, yes_center, (fork,)),
        _stems((no_center, yes_center), "|"),
        _stems((no_center, yes_center), "v"),
        *stay_rows,
        "",
        _pad("if yes, keep climbing"),
        _stems((yes_center,), "|"),
        _span(lift_fork, yes_center),
        _stems((lift_fork,), "|"),
        _stems((lift_fork,), "v"),
        *_center_block(_cbox(("Across every item, or across a verb?",), 52)),
        _stems((lift_fork,), "|"),
        _span(stop_center, lift_center, (lift_fork,)),
        _stems((stop_center, lift_center), "|"),
        _stems((stop_center, lift_center), "v"),
        *stop_rows,
    ]
    return "\n".join(lines)


USE_DIAGRAM = use_diagram()


def framework() -> str:
    """The five layers as a decision record: what you have, what you pick, when you stop."""

    lines = ["WHEN TO STAND ON A LAYER", "Climb only as far as the question.", ""]
    for layer in LAYERS:
        lines.append(f"L{layer.number}  {layer.name}")
        lines.append(f"    Question    {layer.question}")
        lines.append(f"    You have    {layer.you_have}")
        lines.append(f"    You pick    {layer.you_pick}")
        lines.append(f"    Stop when   {layer.stop_when}")
        lines.append(f"    Wisdom      {layer.wisdom}")
        lines.append("")
    return "\n".join(lines).rstrip()


def types_strip() -> str:
    lines = ["DATA TYPES", ""]
    for item in TYPES:
        change = "mutable" if item.mutable else "immutable"
        key = "hashable" if item.hashable else "unhashable"
        lines.append(f"  {item.name:<12} {item.family:<10} {change:<12} {key:<12} {item.law}")
    return "\n".join(lines)


def access_strip() -> str:
    lines = ["DATA STRUCTURES AND THEIR ACCESS LAWS", ""]
    for item in STRUCTURES:
        change = "mutable" if item.mutable else "immutable"
        lines.append(f"  {item.name:<14} {item.access:<14} {change:<12} {item.verb}")
        lines.append(f"  {'':<14} {item.law}")
    return "\n".join(lines)


def adt_matrix() -> str:
    """Every ADT verb, the way it is spelled, and the law that keeps it honest."""

    lines = ["ADT OPERATIONS", ""]
    for adt in ADTS:
        lines.append(f"{adt.name}    {adt.purpose}")
        for op in adt.operations:
            lines.append(f"    {op.name:<12} {op.spelling:<42} {op.law}")
        lines.append("")
    return "\n".join(lines).rstrip()


def other_strip() -> str:
    lines = ["OTHER ELEMENTS OF THE CRAFT", ""]
    for item in ELEMENTS:
        lines.append(f"  L{item.layer}  {item.name:<18} {item.spelling}")
        lines.append(f"       {item.law}")
    return "\n".join(lines)


def guide_strip() -> str:
    lines = ["GIVEN A NEED, REACH FOR THIS", ""]
    for choice in CHOICES:
        ops = ", ".join(choice.operations)
        lines.append(f"  {choice.need}")
        lines.append(f"      L{choice.layer}  {choice.element}    {ops}")
        lines.append(f"      {choice.spelling}")
        lines.append(f"      {choice.why}")
    return "\n".join(lines)


def rules_strip() -> str:
    lines = ["RULES YOU CAN BUILD ON", ""]
    for index, rule in enumerate(RULES, start=1):
        lines.append(f"  {index}. {rule}")
    return "\n".join(lines)


def render() -> str:
    """The whole blueprint, pictures first, then the index that makes them usable."""

    parts = (
        "LAYER LADDER\n\n" + LAYER_LADDER.rstrip(),
        ELEMENT_MAP,
        USE_DIAGRAM.rstrip(),
        framework(),
        types_strip(),
        access_strip(),
        adt_matrix(),
        other_strip(),
        guide_strip(),
        rules_strip(),
    )
    return "\n\n".join(parts)


def _names() -> set[str]:
    names = {item.name for item in TYPES}
    names |= {item.name for item in STRUCTURES}
    names |= {item.name for item in ADTS}
    names |= {item.name for item in ELEMENTS}
    names.add("higher order")
    return names


def _adt(name: str) -> ADT:
    for adt in ADTS:
        if adt.name == name:
            return adt
    raise CraftError(f"unknown ADT {name}")


def _check(label: str, condition: bool) -> None:
    if not condition:
        raise CraftError(f"blueprint check failed: {label}")


def _raises(label: str, func: Callable[[], object], kind: type[BaseException] = CraftError) -> None:
    try:
        func()
    except kind:
        return
    raise CraftError(f"blueprint check failed: {label} was accepted")


def _self_check() -> None:
    """Lock the map: every picture names a real element, and the classic laws still hold."""

    _check("five layers", [layer.number for layer in LAYERS] == [1, 2, 3, 4, 5])
    for layer in LAYERS:
        _check(layer.name, layer.name in LAYER_LADDER and layer.name in ELEMENT_MAP)
    _check("the ladder reaches the value", "[ THE VALUE ]" in LAYER_LADDER)
    _check("the use diagram branches", "ONE VALUE" in USE_DIAGRAM and "MANY VALUES" in USE_DIAGRAM)
    picture_lines = [line for line in USE_DIAGRAM.splitlines() if line]
    _check("the use diagram holds its frame", all(len(line) == CANVAS for line in picture_lines))
    _check("the use diagram climbs to higher order", "L5  lift it" in USE_DIAGRAM and "popleft" in USE_DIAGRAM)

    for line in ELEMENT_MAP.splitlines():
        _check("element map fits the frame", len(line) <= CANVAS)
    box_lines = [line for line in ELEMENT_MAP.splitlines() if line.startswith("+")]
    _check("element map boxes span the canvas", box_lines and all(len(line) == CANVAS for line in box_lines))

    catalog = _names()
    for choice in CHOICES:
        _check(f"{choice.need} names a real element", choice.element in catalog)
        _check(f"{choice.need} has a spelling", choice.spelling != "" and choice.why != "")
        resolved = choose(choice.need)
        _check(f"{choice.need} resolves", resolved is choice)
        for alias in choice.aliases:
            _check(alias, choose(alias) is choice)
        if choice.adt:
            operations = {op.name for op in _adt(choice.adt).operations}
            missing = [name for name in choice.operations if name not in operations]
            _check(f"{choice.need} verbs belong to {choice.adt}", missing == [])

    _raises("an ambiguous need", lambda: choose("map"))
    _raises("an unknown need", lambda: choose("vibes"))
    _check("lookup is a dict", choose("key").element == "dict" and choose("lookup").layer == 2)
    _check("a queue leaves from the left", "popleft" in choose("fifo").spelling)
    _check("money is Decimal", choose("money").element == "Decimal")
    _check("lifting is higher order", choose("every item").layer == 5)

    _check("decimal addition is exact", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
    _check("float addition is the approximation the type admits", (0.1 + 0.2) != 0.3)
    _check("bool is the truth type the language subclasses from int", isinstance(True, int) and choose("truth").element == "bool")
    _check("a tuple of atoms can be a key", hash((1, "a")) == hash((1, "a")))
    _raises("a list used as a key", lambda: hash([]), TypeError)
    _check("a moment without a zone is unfinished", datetime(2026, 1, 1).tzinfo is None)
    _check("a zoned moment is a finished value", datetime(2026, 1, 1, tzinfo=timezone.utc).utcoffset() is not None)

    queue: deque[int] = deque([1, 2])
    queue.append(3)
    _check("dequeue yields the earliest item", queue.popleft() == 1 and list(queue) == [2, 3])
    heap = [3, 1, 2]
    heapq.heapify(heap)
    _check("the heap yields the smallest", heapq.heappop(heap) == 1)
    _check("intersection keeps the shared members", {1, 2, 3} & {2, 3, 4} == {2, 3})
    _check("a counter is a multiset", Counter("aba")["a"] == 2)
    _check("a missing defaultdict key is born on use", defaultdict(list)["k"] == [])
    _check("a packed array indexes like a sequence", array.array("i", [1, 2, 3])[1] == 2)

    def _fresh(items: list[int] | None = None) -> list[int]:
        items = [] if items is None else items
        return items

    _check("each call receives its own container", _fresh() is not _fresh())
    _check(
        "flow moves left to right and compose runs the inner verb first",
        flow(1, lambda n: n + 1, lambda n: n * 10) == compose(lambda n: n * 10, lambda n: n + 1)(1) == 20,
    )
    _check("reduce folds a sequence into one value", reduce(lambda total, item: total + item, (1, 2, 3), 0) == 6)
    _check("the rendered blueprint contains every picture", "HOW TO USE THE ELEMENTS" in render() and "ADT OPERATIONS" in render())


def main() -> None:
    """Print the layered map, the way to use it, and the index of elements."""

    _self_check()
    print(render())
    print()
    print("Blueprint holds. Climb only as far as the question.")


if __name__ == "__main__":
    main()
