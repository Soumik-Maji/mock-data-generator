# Mock Data Generator
This python project generates mock data in various format & forms to serve as source for Spark learning.

**Requirement:** - RustFS docker (rustfs/rustfs:latest), SFTP docker (atmoz/sftp:alpine)

**Purpose:**
- Generates data using Faker lib & some other basic randomisation
- Injects errors into data while storing as well as while exporting to simulate real world cell level data issues
- Provides data as unordered/duplicate file send to simulate file level data issues
- Can export as CSV, JSON, zipped version of them, REST API
- Provides the data as full snapshots, all CDC in a single table, incremental data
- Traget locations for export are RustFS (object store), atmoz (SFTP)

**Later addition:** A light weight kafka like streaming named mockkafka to provide data as message stream as well