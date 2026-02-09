# CHANGELOG

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


