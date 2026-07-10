# Reflection Questions & Answers

Here are the detailed answers to the reflection questions for Phase 4:

### 1. Why is cleaning done before joining tables?
- **Performance & Efficiency:** Cleaning data (removing null keys, duplicates, and invalid rows) reduces the size of the datasets before they are joined. Joining is a high-cost operation in distributed systems like Spark because it requires shuffling data across the network. Smaller, cleaner datasets minimize shuffle write/read times.
- **Data Integrity:** Filtering invalid or malformed data beforehand ensures that the join outputs are clean and that we do not perform joins on corrupted or irrelevant keys.

### 2. What would go wrong if null keys are not removed?
- **Data Skew & Performance Issues:** In Spark, rows with `null` keys will all be hashed to the same partition during a join. This causes a single executor node to do most of the work (data skew), leading to bottlenecks, slow runtimes, or Out-Of-Memory (OOM) errors.
- **Incorrect Insights:** Joining on `null` keys can lead to incorrect aggregation metrics, inflating totals or producing meaningless records under a blank or `null` category.

### 3. How did you decide join order?
- **Broadcasting and Key Joins:** The transaction/fact table (`sales`) contains the bulk of the records, while the dimension table (`customers`) is relatively small. We join `sales` with `customers` using an inner join on `customer_id`. In a production setting, this allows us to leverage broadcast joins if the dimension table is small enough, avoiding expensive shuffles.

### 4. Which step was most difficult and why?
- **Designing Clean Segmentation Logic and Final Consolidation:** Designing the final consolidated reporting table (Task 6) required careful aggregation of both `total_spend` and `order_count` while preserving customer metadata (`customer_name` and `city`) without double-counting or losing records. Implementing the segmentation business logic inside the final schema required proper sequencing of transformations.

### 5. How is SQL logic similar to PySpark?
- **Declarative Operations:** Both PySpark DataFrame APIs and SQL specify *what* data to retrieve and transform rather than *how* to physically execute it. For example:
  - SQL `WHERE` maps directly to PySpark `.filter()` / `.where()`.
  - SQL `GROUP BY` and `SUM()` map to PySpark `.groupBy()` and `.agg(sum())`.
  - SQL `CASE WHEN` maps to PySpark `when().otherwise()`.
- **Under the Hood:** Both compile down to the same Spark execution plan optimized by the Catalyst Optimizer, meaning they run with identical performance.

### 6. What challenges will appear with large data?
- **Shuffle Disk Spill:** When datasets exceed executor memory during grouping or joining, Spark spills the intermediate data to disk, severely slowing down execution.
- **Data Skew:** If a few customers have millions of orders, the executor processing those keys will bottleneck the entire pipeline.
- **Out of Memory (OOM) Errors:** Insufficient executor memory can crash the driver or worker nodes if memory configurations are not properly scaled.

### 7. Can you explain your pipeline in simple steps?
1. **Extract:** Read the raw CSV datasets (`customers.csv` and `sales.csv`) into Spark DataFrames.
2. **Clean:** 
   - Enforce correct schemas (integers for IDs, doubles for amounts).
   - Remove null keys (where `customer_id` or `order_id` is missing).
   - Deduplicate rows to prevent double-counting.
   - Filter out invalid records (where `amount <= 0`).
3. **Aggregate & Analyze:**
   - Summarize daily sales and city revenue.
   - Segment customers based on total spend (Gold, Silver, Bronze).
   - Combine all cleaned customer insights into a unified reporting table.
4. **Load/Save:** Write the final reporting table back to disk as a CSV and save summary files for verification.
