### SQL: The Art of Data Manipulation

## Level 1: Data At Rest (The Blueprint)
The Wisdom: Bind raw primitives into a strongly-typed, persistent matrix.

CREATE TABLE Relation_Name (
    Primitive_Key INT PRIMARY KEY,
    Attribute_1   VARCHAR(50),
    Attribute_2   TIMESTAMP
);
INSERT INTO Relation_Name (Primitive_Key, Attribute_1, Attribute_2)VALUES (1, 'Raw_Value', CURRENT_TIMESTAMP);

## Level 2: Basic Retrieval (Dimensional Slicing)
The Wisdom: Isolate exactly what you need. Project columns (vertical) and select rows (horizontal).

SELECT Attribute_1, Attribute_2          -- Vertical ProjectionFROM Relation_Name WHERE Attribute_1 = 'Target_Primitive';  -- Horizontal Selection

## Level 3: Relational Synthesis (Topology Building)
The Wisdom: Combine discrete entities using primary-foreign key relationships to form a unified context.

SELECT A.Attribute_1, B.Attribute_3FROM Relation_A AJOIN Relation_B B 
  ON A.Primitive_Key = B.Foreign_Key;    -- Synthesizing a new virtual ADT

## Level 4: Data Compression (Statistical Distillation)
The Wisdom: Collapse high-volume raw data into structural groups to extract macro insights.

SELECT Attribute_1, 
       COUNT(Primitive_Key) AS Total,    -- Aggregate Primitive
       SUM(Attribute_Numeric) AS Matrix  -- Aggregate PrimitiveFROM Relation_AWHERE Attribute_2 > '2026-01-01'        -- Filter raw data
       GROUP BY Attribute_1                     -- Compress into bucketsHAVING SUM(Attribute_Numeric) > 5000;    -- Filter compressed buckets

## Level 5: The Complex Apex (Context-Aware Analytics)
The Wisdom: Allow individual rows to evaluate neighboring data without losing their unique identity.

SELECT Attribute_1, Attribute_Numeric,
       -- Look horizontally & vertically across a moving frame
       SUM(Attribute_Numeric) OVER (
           PARTITION BY Attribute_1 
           ORDER BY Attribute_2
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS Moving_Total,
       LAG(Attribute_Numeric, 1) OVER (
           PARTITION BY Attribute_1 ORDER BY Attribute_2
       ) AS Previous_Row_PrimitiveFROM Relation_A;


### Evolutionary Connection Graph:


```
                 [ LEVEL 5: CONTEXT-AWARE APEX ]
                                │
                    (Window Frames / Partitions)
                                │
                                ▼
               [ LEVEL 4: STATISTICAL COMPRESSION ]
                                │
                    (Aggregated / Grouped Rows)
                                │
                                ▼
               [ LEVEL 3: RELATIONAL SYNTHESIS ]
                                │
                   (Multi-Table Virtual Views)
                                │
                                ▼
               [ LEVEL 2: DIMENSIONAL SLICING ]
                                │
                     (Filtered Normal Matrices)
                                │
                                ▼
                  [ LEVEL 1: PERSISTENT MATRIX ]
                                │
                        (Table Schemas)
                                │
                                ▼
                     [ THE ATOMIC PRIMITIVES ]
                    (INT, VARCHAR, GEOMETRY, etc.)
```


### Supported ADT operations:

Here is the matrix mapping each architectural level to the specific SQL ADT operations it supports:

| Architectural Level | Supported SQL ADT Operations |
|---|---|
| Level 1: Persistent Matrix | CREATE TABLE, INSERT INTO, ALTER TABLE, DROP TABLE, TRUNCATE |
| Level 2: Dimensional Slicing | SELECT (Projection), WHERE (Selection), DISTINCT, LIMIT / FETCH |
| Level 3: Relational Synthesis | INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, CROSS JOIN, UNION, UNION ALL, INTERSECT, EXCEPT / MINUS, AS (Aliasing) |
| Level 4: Statistical Compression | GROUP BY, HAVING, Aggregates (SUM, COUNT, AVG, MIN, MAX, STRING_AGG, LISTAGG) |
| Level 5: Context-Aware Apex | Windowing (OVER), Partitioning (PARTITION BY), Sorting (ORDER BY within window), Framing (ROWS / RANGE / GROUPS BETWEEN), Offsets (LEAD, LAG), Rankings (ROW_NUMBER, RANK, DENSE_RANK, NTILE) |

### How to use it:

Based on Data Density (how much data you are collapsing) and Relational Cardinality (how many entities you are connecting).
------------------------------
## 🏛️ The Decision Framework: When to Use Which Level

| Metric / Need | Use Level 1 | Use Level 2 | Use Level 3 | Use Level 4 | Use Level 5 |
|---|---|---|---|---|---|
| Primary Goal | Define & Store | Filter & Search | Relate & Synthesize | Compress & Summarize | Compare & Stream |
| Input Data State | Raw Primitives | Single Entity | Scattered Entities | High-Volume Logs | Sequential Timeline |
| Output Data State | Persistent Table | Reduced Sub-table | Unified Virtual View | Macro Metric Grid | Context-Aware Rows |
| Performance Focus | Index Layout | Search Index Hits | Join Algorithms | Memory Hashing | Sorting Buffers |

------------------------------

## 🎨 Elegant Representation Structure: The "Functional Pipeline Notation"

Represent in the form of Functional Composition Pipeline.

You can read a complex SQL query from the inside out (or bottom to top) using this elegant functional representation:

{Intelligence} = {Level}_5 ( {Level}_4 ( {Level}_3 ( {Level}_2 ( {Level}_1 ) ) ) )

## Concrete Architectural Example: Financial Risk Engine
Instead of writing a messy 100-line SQL query immediately, you map your architecture out like this:

-- 1. Storage Layer (Define the physical schema bounds)
L1_Storage   = Base_Relation(transaction_id: INT, user_id: INT, amount: DECIMAL, ts: TIMESTAMP)
-- 2. Security Boundary (Discard invalid data instantly)
L2_Filtered  = Select(L1_Storage) WHERE is_declined = FALSE
-- 3. Identity Synthesis (Hydrate the log with user risk profiles)
L3_Hydrated  = Join(L2_Filtered, User_Profiles) ON user_id
-- 4. Macro Baseline (Calculate the historical normal behavior of this cohort)
L4_Baseline  = GroupBy(L3_Hydrated, cohort_id) -> Calculate(AVG(amount))
-- 5. Contextual Apex (Analyze the moving timeline pattern to detect anomalies)
L5_RiskScore = Window(L4_Baseline) PARTITION BY user_id ORDER BY ts ROWS(2 PRECEDING)

## 🧠 The Rules of Thumb for Architecture

   1. Never jump to Level 4 or 5 if your Level 1 is poorly modeled. If your primitive types are wrong (e.g., storing dates as strings), your window functions will fail or run incredibly slowly.
   2. Push filtering down as low as possible. Running a Level 2 filter after a Level 3 join destroys database performance. Apply your WHERE clauses directly to the Level 1 matrices before synthesising them.
   3. If you need to keep the row details, you cannot use Level 4. The moment you write GROUP BY, individual identities vanish into a summary statistics grid. If you need the individual records plus the macro statistics, bypass Level 4 compression and step straight into Level 5 windowing.


