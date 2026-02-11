# CHANGELOG

## Onshape Git Sync v1 - 2026-02-10

# Pull Request - Containerize Onshape Snapshot Workflow with Automated Git Push via Cron

This PR introduces full containerization and automation for the Onshape project snapshot workflow, making it easily deployable and maintainable across Linux and macOS environments. Key updates include:

## What’s new:

1. **Docker containerization**
   - All Python scripts and dependencies are now encapsulated in a Docker image.
   - Ensures consistent execution environment across machines.

2. **Automated workflow via shell scripts and cron**
   - `start_onsync.sh` initializes the Docker build and runs the container.
   - Cron job added to execute the container hourly, continuously monitoring the Onshape project for new official versions.

3. **Automatic Git integration**
   - Added a shell script to push changes to the GitHub repository whenever a new Onshape version is detected.
   - Each official version results in a snapshot of the project, including metadata and assembly images, which is stored in the repository.

4. **Generated Markdown for snapshots**
   - Python script now writes a `README.md` (or markdown file) into the snapshots folder.
   - Contains the name, description, and images of each Onshape version for easy human viewing.

## Impact / Benefits:
- Fully automated, minimal-maintenance workflow for tracking Onshape project versions.
- Easy deployment on any system with Docker.
- Demonstrates hands-on experience with DevOps practices: containerization, automation with cron, and CI-like Git integration.

## Next steps / considerations:
- Merge into `main` to enable automated snapshot updates across environments.
- Potential future enhancement: add notifications or logging for snapshot updates.



## [Unreleased] - 2026-02-10

## Pull Request: Initial Onshape Version Sync, Snapshotting, and Assembly Imaging

### Summary

This PR introduces the first complete end-to-end sync pipeline between an Onshape document and a local Git-tracked archive. The project now reliably:

- Fetches and archives version metadata from the Onshape API
- Maintains an append-only JSON log of API responses
- Creates deterministic, timestamp-based snapshot folders per version
- Discovers assembly elements per version
- Generates shaded assembly images and archives them alongside version snapshots

This establishes a foundation for later Git mirroring, CI execution, and automation.

---

### What This Adds

#### 1. Version Fetching & Archival
- Fetches **all document versions** from the Onshape API
- Writes each successful API response to `logs/<timestamp>.json`
- Supports **offline mode**, allowing the pipeline to continue from the last known good archive

This mirrors real-world CI behavior where transient API failures should not halt downstream processing.

---

#### 2. Snapshot Directory Model
- Each Onshape version is mapped to a **stable snapshot directory** named by the version’s creation timestamp
- Snapshot structure is deterministic and idempotent:

```
snapshots/
  <version_timestamp>/
    snapshot.json
    elements.json
    img/
```

This avoids relying on user-defined version names and ensures consistent ordering across systems.

---

#### 3. Element Discovery
- For each version snapshot, the script fetches and archives `elements.json`
- Assembly elements are identified explicitly and separated from other element types
- Enables downstream processing without repeated API calls

---

#### 4. Assembly Image Generation
- For each assembly element, shaded view images are fetched via the Onshape API
- Images are written directly to disk from base64 payloads
- Overwrites are allowed to keep logic simple and deterministic
- Image generation is isolated per version and per element

This provides a human-readable artifact that complements version metadata and supports asynchronous review (e.g., hardware ↔ software teams).

---

### Design Decisions

- **Append-only logs** over in-place updates to preserve history and support debugging
- **Offline-first execution path** to tolerate API errors and rate limits
- **Timestamp-based identifiers** instead of human naming to avoid ambiguity
- **Small, composable Python functions** instead of monolithic scripts
- **Side-effect-aware orchestration** suitable for cron / EC2 execution

---

### What’s Next

- Detect new versions and selectively process only unseen snapshots
- Mirror snapshot changes into Git commits automatically
- Add CI execution (cron / EC2 / GitHub Actions)
- Extend imaging to exploded views where supported

---

### Notes for Reviewers

This PR intentionally prioritizes **observability, determinism, and failure tolerance** over feature completeness. The goal is to model how design data can move through a DevOps-style pipeline with minimal manual intervention.


## [Unreleased] - 2026-02-09

### Added

- **Basic functionality for syncing Onshape document versions to Git**  
  Implemented a script that fetches Onshape document versions using the Onshape API, archives them in local JSON files, and enables tracking of the most recent version.
  
- **Offline Mode Fallback**  
  Implemented an `OFFLINE_MODE` flag to allow testing and continuous functionality even without an active API connection. This fallback behavior ensures that even if the API fetch fails, the system can continue to function by reading from the last known valid JSON log. This increases resilience and allows for easy recovery from transient failures or rate-limited states.

- **Error Handling & Logging**  
  Error handling was added to deal with unexpected API fetch failures. The error messages are written to `.error.json` files with timestamps, enabling tracking of failures and retries. This ensures that any problem in data retrieval is well-documented without causing the program to crash.

### Changed

- **Code Refactoring for Readability and Maintainability**  
  The original API-fetching code was refactored into smaller, more manageable functions:
  - `fetch_versions_from_api`: Handles API interaction, authentication, and response retrieval.
  - `get_latest_valid_log`: Finds the most recent successful log file to use for processing.
  - `fetch_and_archive_versions`: Coordinates fetching and archiving in one place, with added error handling.
  
  These changes follow the principle of **single responsibility** and **modular design**, ensuring that each part of the script can be easily tested, extended, or debugged.

- **Added Timestamped Logging**  
  Each successful API fetch is logged with a timestamp in the `logs/` directory. This creates an immutable history of data retrieval, ensuring that any changes can be traced back to a specific point in time. The logs are stored as `YYYYMMDD_HHMMSS.json` files, allowing the system to always have access to previous API responses.

### Design Decisions

- **Use of Virtual Environments (Venv)**  
  To isolate project dependencies and ensure that the script can be run consistently across different systems, a virtual environment (`.venv`) was created. This prevents conflicts with the system Python environment and makes the project easier to manage in both development and production. This is a standard practice to **avoid dependency confusion** and ensures that development environment is both clean and reproducible.

- **Authentication Strategy**  
  The Onshape API requires **HMAC-based authentication**, which was not implemented in this entry. This is recognized as a necessary step moving forward for real-world API integration. For now, the script uses basic key/secret-based authentication, which works with publicly accessible Onshape document versions. A robust implementation will require correct HMAC signing.

- **Offline Mode for Stability**  
  The inclusion of an `OFFLINE_MODE` flag was an intentional decision to support resilience. This design allows the script to continue functioning even if the API is unreachable or temporarily fails (e.g., rate limiting). It ensures that the program can still read from the latest available log and proceed, without requiring constant online access to the API. This **reduces downtime** and **improves system reliability**.

- **Graceful Failure & Logging**  
  Instead of failing silently or crashing upon encountering a bad API call, the system gracefully handles API errors by logging them into error-specific files. This is done in a `logs/` folder, which serves as a form of **observability**. With this, one can trace back failed requests and retry them if necessary, which is a **key DevOps principle** for ensuring reliability in automated systems.

### Next Steps
  
- **Integrate Version Control (Git) Logic**  
  Moving forward, add logic to **track and commit new versions** of the Onshape document to a Git repository, effectively mirroring changes to the design over time. This will be used to demonstrate version management and show that the latest Onshape design can be kept in sync with Git.

- **Deploy on EC2 for Automation**  
  The script will be deployed to an EC2 instance with a scheduled task (e.g., cron job) that periodically fetches Onshape version data and updates the Git repository. This will demonstrate a fully automated CI/CD pipeline, pulling data from Onshape and pushing it to Git at regular intervals.

---

This change represents the first milestone in building a reliable DevOps pipeline for automating the synchronization of Onshape data to Git. It demonstrates key principles of **resilience**, **error handling**, and **automation**.


