# Stage 1

## Core Actions

### 1. Create Notification

POST /notifications

Request:

```json
{
  "studentId": 1042,
  "type": "Placement",
  "message": "Company hiring drive"
}
```

Response:

```json
{
  "status": "success",
  "notificationId": "uuid"
}
```

### 2. Get Notifications

GET /notifications/{studentId}

### 3. Get Unread Notifications

GET /notifications/{studentId}/unread

### 4. Mark Notification As Read

PUT /notifications/{notificationId}/read

### 5. Mark All Notifications As Read

PUT /notifications/{studentId}/read-all

### 6. Delete Notification

DELETE /notifications/{notificationId}

### Real-Time Notification Mechanism

Use WebSockets.

Flow:

1. Notification created
2. Stored in DB
3. Published to WebSocket server
4. Student receives notification instantly
5. Notification also stored for later retrieval

---

# Stage 2

## Database Choice

PostgreSQL

Reasons:

* ACID compliance
* Strong indexing support
* Handles large datasets efficiently
* Reliable for transactional systems

### Schema

Students

```sql
CREATE TABLE students(
    studentId BIGINT PRIMARY KEY,
    name VARCHAR(100)
);
```

Notifications

```sql
CREATE TABLE notifications(
    id UUID PRIMARY KEY,
    studentId BIGINT,
    notificationType VARCHAR(20),
    message TEXT,
    isRead BOOLEAN DEFAULT FALSE,
    createdAt TIMESTAMP,
    FOREIGN KEY(studentId) REFERENCES students(studentId)
);
```

Potential Scaling Issues:

* Slow reads
* Large table scans
* High write load

Solutions:

* Indexing
* Partitioning
* Caching
* Read replicas

---

# Stage 3

Original Query

```sql
SELECT *
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC;
```

Why Slow?

Without indexes, database scans millions of rows.

Recommended Index

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(studentID, isRead, createdAt DESC);
```

Complexity:

Before:
O(N)

After:
O(log N)

Adding indexes on every column is NOT recommended because:

* Increased storage
* Slower inserts/updates
* Unused indexes waste resources

Placement Notifications Last 7 Days

```sql
SELECT *
FROM notifications
WHERE notificationType='Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```

---

# Stage 4

Performance Improvements

1. Redis Cache

   * Faster reads
   * Extra memory usage

2. Pagination

   * Smaller payloads
   * More API calls

3. Read Replicas

   * Distributes load
   * Replication overhead

4. WebSocket Push

   * Reduces repeated polling
   * Persistent connections required

---

# Stage 5

Problems With Existing Approach

* Sequential processing
* Slow execution
* Failures cause inconsistency
* Not scalable

Improved Design

Use Queue (RabbitMQ/Kafka).

Pseudo Code

```python
def notify_all(student_ids, message):
    save_notification(message)

    for student in student_ids:
        publish_to_queue(student, message)

worker():
    send_email()
    push_notification()
```

Benefits:

* Reliable
* Retry support
* Scalable
* Faster processing

Database save and email sending should NOT be in one transaction because external email services can fail independently.

---

# Stage 6

Priority Logic

Weights:

Placement = 3
Result = 2
Event = 1

Priority Score:

score = weight + recency_factor

Implementation:

Use Min Heap of size 10.

Benefits:

* O(log 10)
* Efficient updates
* Supports continuous incoming notifications
