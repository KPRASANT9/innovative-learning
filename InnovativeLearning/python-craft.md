# Python: The Craft of the Language

Climb only as far as the question.

```text
{Result} = L5( L4( L3( L2( L1( value ) ) ) ) )
```

## Questions

Ask these in order. The first question that finishes the work is the layer you stand on.

### 1. What type can carry what this value really is?

**Level 1 — Data types.**

You have a raw atom crossing the edge of the program.
You pick `int`, `bool`, `float`, `complex`, `Decimal`, `Fraction`, `str`, `bytes`, `None`, `datetime`.
Stop when the question is about that single value.

The wisdom: Give the value a type that can carry its law: exactness, order, text, octets, truth, or absence.

### 2. How will you reach one value among many?

**Level 2 — Data structures.**

You have many values, and a way you intend to reach them.
You pick `list`, `tuple`, `range`, `dict`, `set`, `frozenset`, `deque`, `heap`.
Stop when one shape answers the access, and only this place uses it.

The wisdom: Choose the shape by the access law: position, key, membership, either end, or the next extreme.

### 3. Which operation is lawful for that shape?

**Level 3 — ADT operations.**

You have a structure and one question to ask it.
You pick `index`, `slice`, `get`, `add`, `push`, `pop`, `union`, `heappop`, `unpack`, `iterate`.
Stop when the verb is used in one place.

The wisdom: Use the verb that belongs to the shape. The spelling of `in` is shared; the law under it is not.

### 4. Should callers see the container, or only the operation's name?

**Level 4 — The boundary.**

You have a verb that more than one caller needs.
You pick a function, a protocol, a dataclass, a raised error, a with-block.
Stop when callers can depend on the name, and the verb is not being lifted across a whole collection.

The wisdom: Name the verb, and let the name hide the container.

### 5. Does this operation apply to every value, or to another operation?

**Level 5 — Higher order.**

You have a verb that repeats across items, or a verb whose subject is another verb.
You pick `map`, `filter`, `reduce`, a comprehension, a generator, `partial`, `compose`, a decorator.
Stop when the lift itself is the whole question.

The wisdom: Lift a verb across items, or a verb across verbs. Otherwise you have already climbed far enough.

## The layer ladder

Read downward. Each layer rests on the one below it. The value is the ground.

```text
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
```

## The element map

Higher order sits on a named operation. The operation sits on a shape. The shape holds typed values.

```text
                                 THE LANGUAGE, LAYER BY LAYER                                 
                        {Result} = L5( L4( L3( L2( L1( value ) ) ) ) )                        
                              Climb only as far as the question.                              

+--------------------------------------------------------------------------------------------+
|                                     L5   HIGHER ORDER                                      |
|                              map   filter   reduce   compose                               |
|                           comprehension   generator   decorator                            |
|                           a verb across values, or across verbs                            |
+--------------------------------------------------------------------------------------------+
                                      lift a named verb                                       
                                              |                                               
                                              v                                               
+--------------------------------------------------------------------------------------------+
|                                     L4   THE BOUNDARY                                      |
|                              function   protocol   dataclass                               |
|                                exception   context manager                                 |
|                           the caller sees the verb, not the list                           |
+--------------------------------------------------------------------------------------------+
                                   a name for a lawful verb                                   
                                              |                                               
                                              v                                               
                                     L3   ADT OPERATIONS                                      
+--------------------+  +--------------------+  +--------------------+  +--------------------+
|      sequence      |  |      mapping       |  |        set         |  |        heap        |
|    index, slice    |  |   get, put, del    |  |    add, discard    |  |      heappush      |
|  iterate, unpack   |  |   key in mapping   |  |     &  |  -  ^     |  |      heappop       |
+--------------------+  +--------------------+  +--------------------+  +--------------------+
+--------------------+  +--------------------+  +--------------------+  +--------------------+
|       stack        |  |       queue        |  |       deque        |  |       record       |
|       append       |  |       append       |  |     appendleft     |  |   field, unpack    |
|     pop, peek      |  |      popleft       |  |   pop either end   |  |    fixed shape     |
+--------------------+  +--------------------+  +--------------------+  +--------------------+
                                 a shape for each access law                                  
                                              |                                               
                                              v                                               
                                     L2   DATA STRUCTURES                                     
+--------------------+  +--------------------+  +--------------------+  +--------------------+
| list, tuple, range |  |        dict        |  |   set, frozenset   |  |    deque, heap     |
|    by position     |  |       by key       |  |   by membership    |  |   ends, extreme    |
+--------------------+  +--------------------+  +--------------------+  +--------------------+
                                  each item is a typed value                                  
                                              |                                               
                                              v                                               
+--------------------------------------------------------------------------------------------+
|                                      L1   DATA TYPES                                       |
|                     int   bool   float   complex   Decimal   Fraction                      |
|                         str   bytes   bytearray   None   datetime                          |
|                        str and bytes are values, and also sequences                        |
+--------------------------------------------------------------------------------------------+
                                   born as one honest value                                   
                                              |                                               
                                              v                                               
                                        [ THE VALUE ]                                         
```

## How to use the elements

One value, or many. Then climb only when a second caller needs the operation, or the operation itself is the subject.

```text
                                   HOW TO USE THE ELEMENTS                                    
                              Climb only as far as the question.                              

+--------------------------------------------+  +--------------------------------------------+
|                 ONE VALUE                  |  |                MANY VALUES                 |
|          a type, then stop at L1           |  |           an access law, then L2           |
|                                            |  |                                            |
|  exact         int, Decimal, Fraction      |  |  position      list, tuple, range          |
|  truth         bool, None                  |  |  key           dict                        |
|  text          str                         |  |  membership    set, frozenset              |
|  octets        bytes                       |  |  both ends     deque                       |
|  time          datetime, with a zone       |  |  extreme       heap, smallest out          |
|  encode        text.encode("utf-8")        |  |  stack         append, then pop            |
|  absence       None is not a failure       |  |  queue         append, then popleft        |
+--------------------------------------------+  +--------------------------------------------+
                       |                                               |                      
                       +-----------------------+-----------------------+                      
                                               |                                              
                                               v                                              
                        +--------------------------------------------+                        
                        |      Do other callers need this verb?      |                        
                        +--------------------------------------------+                        
                                               |                                              
                            +------------------+------------------+                           
                            |                                     |                           
                            v                                     v                           
             +----------------------------+        +----------------------------+             
             |             no             |        |            yes             |             
             |      L3  use the verb      |        |     L4  name the verb      |             
             |     in this one place      |        |    function or protocol    |             
             +----------------------------+        +----------------------------+             

                                    if yes, keep climbing                                     
                                                                  |                           
                                               +------------------+                           
                                               |                                              
                                               v                                              
                     +--------------------------------------------------+                     
                     |       Across every item, or across a verb?       |                     
                     +--------------------------------------------------+                     
                                               |                                              
                             +-----------------+-----------------+                            
                             |                                   |                            
                             v                                   v                            
               +--------------------------+        +--------------------------+               
               |            no            |        |           yes            |               
               |        stop here         |        |       L5  lift it        |               
               |    the name suffices     |        |   map  filter  reduce    |               
               |     climb no further     |        |    generator  compose    |               
               +--------------------------+        +--------------------------+               
```

## When to stand on a layer

| Level | Question | Stop when |
|---|---|---|
| 1. Data types | What type can carry what this value really is? | the question is about that single value |
| 2. Data structures | How will you reach one value among many? | one shape answers the access, and only this place uses it |
| 3. ADT operations | Which operation is lawful for that shape? | the verb is used in one place |
| 4. The boundary | Should callers see the container, or only the operation's name? | callers can depend on the name, and the verb is not being lifted across a whole collection |
| 5. Higher order | Does this operation apply to every value, or to another operation? | the lift itself is the whole question |

## Data types

Level 1. A value has one honest type. The type decides equality, order, truth, and whether it may be a key.

| Type | Family | Life | As a key | Law |
|---|---|---|---|---|
| `int` | number | immutable | hashable | Exact integer, unbounded. |
| `bool` | truth | immutable | hashable | A truth value. It subclasses int; keep it for truth. |
| `float` | number | immutable | hashable | A binary approximation. Right for measurement, wrong for money. |
| `complex` | number | immutable | hashable | Real and imaginary parts. It has no order. |
| `Decimal` | number | immutable | hashable | Exact base-10. The type for money and decimal facts. |
| `Fraction` | number | immutable | hashable | An exact ratio of two integers. |
| `str` | text | immutable | hashable | Unicode text. Indexing it yields characters. |
| `bytes` | octets | immutable | hashable | Immutable octets. Text arrives only through an encoding. |
| `bytearray` | octets | mutable | unhashable | Mutable octets. |
| `None` | absence | immutable | hashable | The single value that means absence. |
| `datetime` | time | immutable | hashable | A moment. Finish it with a timezone. |

`str` and `bytes` are values, and also sequences of their atoms. Index them when you mean the atoms. Pass them whole when you mean the text or the octets.

## Data structures

Level 2. Choose the shape by the access law you will actually use.

| Shape | Access | Life | Verb | Law |
|---|---|---|---|---|
| `list` | position | mutable | `items[i]; items.append(x)` | Ordered and mutable. Membership walks. It cannot be a key. |
| `tuple` | position | immutable | `record[i]; a, b = record` | Fixed sequence. A record when each index has a meaning. Hashable when its items are. |
| `range` | position | immutable | `range(start, stop)` | An arithmetic progression. It stores the bounds, not the integers. |
| `str` | position | immutable | `text[i]` | A value that is also a sequence of characters. |
| `bytes` | position | immutable | `buf[i]` | A value that is also a sequence of octets. |
| `dict` | key | mutable | `mapping[key]` | Key to value, in insertion order. The key is hashable and stays unchanged. |
| `set` | membership | mutable | `item in pool; a & b` | Unique hashable items. Unordered. |
| `frozenset` | membership | immutable | `item in pool` | An immutable set. It may itself be a key. |
| `deque` | both ends | mutable | `d.append(x); d.popleft()` | Either end is O(1). This is the queue. |
| `heap` | next extreme | mutable | `heapq.heappop(heap)` | A list kept in heap order. The smallest comes out first. |
| `Counter` | key | mutable | `Counter(items)[item]` | A mapping from item to count. A multiset. |
| `defaultdict` | key | mutable | `groups[key].append(x)` | A mapping that builds a missing value. A plain dict raises instead. |
| `array` | position | mutable | `array.array("i", numbers)` | Packed, homogeneous atoms. A list holds references; this holds the atoms. |

## ADT operations

Level 3, and the higher-order verbs of Level 5. The structure behind a verb is a costume. Use the verb the shape permits.

### sequence

Read by position, in order.

| Operation | Spelling | Law |
|---|---|---|
| length | `len(items)` | The number of items. |
| index | `items[i]` | From the start. A negative index counts from the end. |
| slice | `items[i:j]` | A sequence operation that returns a sequence. |
| concat | `left + right` | A new sequence. Concat does not extend a list in place. |
| iterate | `for item in items` | The structure yields items in its own order. |
| contains | `item in items` | On a sequence, membership walks. |
| unpack | `a, b = items` | The names and the items agree in count. |

### list

A sequence that grows, usually at the end.

| Operation | Spelling | Law |
|---|---|---|
| append | `items.append(x)` | Grow at the end. |
| extend | `items.extend(more)` | Absorb another sequence at the end. |
| insert | `items.insert(i, x)` | Open a hole at a position. The tail moves. |
| pop | `items.pop()` | Take the end. pop(0) walks; a queue does not live here. |
| sort | `items.sort()` | Order in place. sorted(items) returns a new list. |

### stack

Last in, first out. The end of a list is the top.

| Operation | Spelling | Law |
|---|---|---|
| push | `stack.append(x)` | The new top sits at the end. |
| pop | `stack.pop()` | The latest item comes back first. |
| peek | `stack[-1]` | Look at the top and leave it there. |

### queue

First in, first out. A deque, with the exit at the left.

| Operation | Spelling | Law |
|---|---|---|
| enqueue | `queue.append(x)` | Arrive at the right. |
| dequeue | `queue.popleft()` | Leave from the left. |
| peek | `queue[0]` | The next item to leave, still waiting. |

### deque

Both ends, each in constant time.

| Operation | Spelling | Law |
|---|---|---|
| append | `d.append(x)` | Grow at the right. |
| appendleft | `d.appendleft(x)` | Grow at the left. |
| pop | `d.pop()` | Shrink at the right. |
| popleft | `d.popleft()` | Shrink at the left. |

### mapping (Dict))

Reach a value by a hashable key.

| Operation | Spelling | Law |
|---|---|---|
| put | `mapping[key] = value` | The key stays unchanged while it lives here. |
| get | `mapping.get(key, default)` | A bare mapping[key] raises when the key is absent. |
| delete | `del mapping[key]` | Remove the pair. |
| contains | `key in mapping` | A hash lookup, not a walk. |
| items | `mapping.items()` | Key and value together, in insertion order. |

### set

Membership, uniqueness, and the algebra of collections.

| Operation | Spelling | Law |
|---|---|---|
| add | `pool.add(x)` | A second add of an equal item changes nothing. |
| discard | `pool.discard(x)` | Absence is a no-op. remove raises. |
| contains | `x in pool` | A hash lookup. |
| union | `a \| b` | Items that live in either. |
| intersection | `a & b` | Items that live in both. |
| difference | `a - b` | Items that live only in a. |
| symmetric | `a ^ b` | Items that live in one side only. |
| subset | `a <= b` | Every item of a is an item of b. |

### priority queue

Always extract the smallest.

| Operation | Spelling | Law |
|---|---|---|
| push | `heapq.heappush(heap, x)` | Keep the heap ordered as the item arrives. |
| pop | `heapq.heappop(heap)` | The smallest item. |
| peek | `heap[0]` | The smallest, left in place. The heap must not be empty. |
| heapify | `heapq.heapify(items)` | Turn a list into a heap in place. |

### record

A fixed shape. Position or field, never a growing end.

| Operation | Spelling | Law |
|---|---|---|
| construct | `Point(x, y)` | A tuple when names would be noise. A dataclass when the law belongs in construction. |
| project | `point.x` | A tuple projects by index: record[0]. |
| unpack | `x, y = record` | Bind each part in one step. |

### iterator

The one traversal every structure shares.

| Operation | Spelling | Law |
|---|---|---|
| iter | `iter(items)` | Ask a structure for its stream. |
| next | `next(stream)` | StopIteration ends a finite stream. |

### higher order

A verb applied to values, or to other verbs.

| Operation | Spelling | Law |
|---|---|---|
| map | `map(verb, items)` | The same verb, each item, lazily. |
| filter | `filter(keep, items)` | Items that pass the test, lazily. |
| reduce | `reduce(combine, items, start)` | Fold the items into one value. |
| comprehend | `[verb(x) for x in items if keep(x)]` | Map and filter that return a collection. |
| generate | `(verb(x) for x in items)` | A sequence that does not exist until asked. yield suspends one step. |
| partial | `partial(verb, fixed)` | Fix some arguments. Leave the rest open. |
| compose | `compose(outer, inner)(value)` | Inner runs first. This is L5(L4(...(value))). |
| decorate | `@boundary` | compose, applied when the function is defined. |

## Other elements

Laws of the language that are not themselves containers.

| Level | Element | Spelling | Law |
|---|---|---|---|
| 1 | binding | `name = value` | A name is a bond to a value. Rebinding the name does not edit the value. |
| 1 | equality | `a == b` | Equality asks whether two values agree. |
| 1 | identity | `a is b` | Identity asks whether two names share one object. Reserve it for None and sentinels. |
| 1 | truth | `bool(value)` | None, False, zero, and empty containers are false. That test is not a type check. |
| 1 | encode | `text.encode("utf-8")` | Text and octets meet at an encoding you write down. |
| 2 | hash | `hash(value)` | Hashable values may be keys and set members. They stay unchanged. |
| 2 | copy | `items.copy()` | Copying a structure copies the references it holds, not the inner objects. |
| 4 | function | `def verb(value): ...` | Name the operation. Callers receive the verb, not the container. |
| 4 | protocol | `collections.abc.Mapping` | An ADT written as the operations a caller may rely on. |
| 4 | dataclass | `@dataclass(frozen=True)` | A named record. Construction is where its law lives. |
| 4 | exception | `raise ValueError(reason)` | A broken promise. Absence stays None. Failure raises. |
| 4 | context | `with resource as handle:` | Acquire and release are one shape. |
| 4 | namespace | `local, enclosing, global, built-in` | A name resolves outward in that order. |
| 4 | mutable default | `def verb(items=None):` | A default is born once. Build a fresh mutable inside the function. |
| 5 | closure | `def adder(n): return lambda x: x + n` | A function keeps the bindings it was born with. |
| 5 | recursion | `def walk(node): ... walk(child)` | A verb defined on a smaller value of the same shape. |

## Given a need, reach for this

Name the need in plain words. `craft.choose` returns the same row. The word `map` alone is ambiguous: say `lookup` for a dict, or `lift` to apply an operation across items.

| Need | Level | Element | Spelling | Why |
|---|---|---|---|---|
| integer | 1 | `int` | `int(text)` | An exact count or index. |
| truth | 1 | `bool` | `True` | A yes or a no. Keep arithmetic off it. |
| money | 1 | `Decimal` | `Decimal("10.20")` | Base-10 facts, including money. |
| ratio | 1 | `Fraction` | `Fraction(1, 3)` | An exact ratio of integers. |
| approximation | 1 | `float` | `float(text)` | A measured quantity, where binary approximation is acceptable. |
| text | 1 | `str` | `text` | Whole text is the value. Index only when you mean characters. |
| octets | 1 | `bytes` | `b"octets"` | Raw octets, already encoded. |
| absence | 1 | `None` | `None` | Absence of a value. A failed promise is an exception. |
| moment | 1 | `datetime` | `datetime(2026, 1, 1, tzinfo=timezone.utc)` | A finished moment carries a timezone. |
| record | 2 | `tuple` | `(x, y)` | The length is part of the meaning. |
| named record | 4 | `dataclass` | `@dataclass(frozen=True)` | The parts have names, and construction keeps the law. |
| sequence | 2 | `list` | `items.append(x); items[i]` | Order matters, and the collection grows at the end. |
| both ends | 2 | `deque` | `deque([a, b])` | Growth or shrinkage happens at both ends. |
| stack | 3 | `list` | `stack.append(x); stack.pop()` | The latest arrival is the next to leave. |
| queue | 3 | `deque` | `q.append(x); q.popleft()` | The earliest arrival is the next to leave. |
| lookup | 2 | `dict` | `m[key] = value` | The question is the key, and the answer is the value. |
| membership | 2 | `set` | `pool.add(x); a & b` | Uniqueness, or the algebra of who belongs. |
| frozen membership | 2 | `frozenset` | `frozenset(items)` | A set that must be shared or used as a key. |
| next extreme | 3 | `heap` | `heapq.heappush(h, x); heapq.heappop(h)` | Each extraction wants the smallest waiting item. |
| count items | 2 | `Counter` | `Counter(items)` | Each item answers with how many times it appeared. |
| missing key | 2 | `defaultdict` | `defaultdict(list)` | Every missing key should be born the same way. |
| dense integers | 2 | `array` | `array.array("i", numbers)` | The atoms are uniform and should sit packed, not boxed. |
| progression | 2 | `range` | `range(start, stop)` | The integers follow from a start, a stop, and a step. |
| encode | 1 | `encode` | `text.encode("utf-8")` | Cross the text and octets boundary with the encoding visible. |
| walk | 3 | `iterator` | `for item in items` | Visit each item. The structure decides the order. |
| name the verb | 4 | `function` | `def verb(items): ...` | More than one caller needs the operation. |
| protocol | 4 | `protocol` | `collections.abc.Mapping` | Callers may rely on the verbs, and on nothing behind them. |
| failure | 4 | `exception` | `raise ValueError(reason)` | The operation cannot keep its promise. |
| resource | 4 | `context` | `with resource as handle:` | Something is acquired and must be released. |
| lift | 5 | `higher order` | `[verb(x) for x in items]` | One verb applies to every item, and you want the collection. |
| lazy | 5 | `higher order` | `(verb(x) for x in items)` | The items are produced when a consumer asks. |
| compose verbs | 5 | `higher order` | `compose(outer, inner)(value)` | One verb's result is the next verb's input. Inner runs first. |
| decorate | 5 | `higher order` | `@boundary` | A verb should be wrapped at the moment it is defined. |
| fresh container | 4 | `mutable default` | `def verb(items=None):` | Each call needs its own list, dict, or set. |

## Rules you can build on

1. Pick the type before the structure.
2. Pick the structure by the access law you will actually use.
3. A queue is popleft on a deque. The end of a list is a stack.
4. Membership walks a sequence and hashes a set or a dict.
5. A key is hashable and stays unchanged for its whole life in the structure.
6. Name a verb the moment a second caller needs it.
7. A comprehension returns a collection. A generator waits to be asked. compose runs the inner verb first.
8. None is absence. A broken promise raises. An empty structure is empty.

## Prepare on top of this

Extend a level, or read the result of a named operation. Leave Level 1 closed.
A wrong type makes every later operation a precise-looking lie. A second caller is the moment an operation earns a name. A repeated operation is the moment it earns a lift.
