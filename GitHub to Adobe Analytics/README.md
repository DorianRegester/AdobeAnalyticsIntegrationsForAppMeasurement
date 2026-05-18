# Server-Side GitHub Portfolio Auditor

**Server-Side GitHub Portfolio Auditor** is a high-precision utility designed to ingest GitHub engagement metrics directly into **Adobe Analytics**. By utilizing a Python-based middleware and the **Adobe Data Insertion API**, this solution bypasses the need for client-side JavaScript (AppMeasurement.js). It allows for persistent, long-term auditing of repository performance, stars, and file-level interactions across a large-scale portfolio of 75+ repositories.

## Key Capabilities

*   **Server-to-Server Tracking:** Sends XML-formatted payloads directly to Adobe’s collection servers, ensuring data integrity without a browser.
*   **Automated Auditing:** Loops through all owned repositories to capture stars, forks, views, and clones.
*   **Granular Pathing:** Maps specific GitHub file paths to Adobe eVars, enabling deep-dive analysis into which sub-folders or documentation files drive engagement.
*   **Timestamp Precision:** Uses the `<timestamp>` node to ensure data is attributed to the correct date/time, regardless of when the GitHub Action finishes execution.

## Project Structure

To maintain a clean repository, the automation logic is separated into individual files:

*   **`adobe_sync.py`**: The core Python engine that fetches GitHub data and transmits XML payloads to the Data Insertion API.
*   **`.github/workflows/adobe_sync.yml`**: The GitHub Actions configuration that triggers the daily synchronization at 12:30 AM.
*   **`requirements.txt`**: Lists necessary Python dependencies (e.g., `requests`).

## Step 1: Architect the Adobe Schema

Before execution, reserve these variables within the Adobe Analytics Admin Console (**Analytics > Admin > Report Suites > Edit Settings > Conversion**).

| GitHub Data Point | Adobe Variable | Type | Example Value |
| :--- | :--- | :--- | :--- |
| **Repo Name** | `eVar1` | Success Variable | `DorianRegester/aem-plugin-x` |
| **File/Folder Path**| `eVar2` | Success Variable | `/src/main.js` |
| **Daily Views** | `event1` | Counter | `1` |
| **Daily Clones** | `event2` | Counter | `1` |
| **Total Stars** | `event3` | Counter | `1` |
| **Total Forks** | `event4` | Counter | `1` |

> **Architect's Note:** Set `eVar1` and `eVar2` to **Full Sub-relation** to allow for multi-dimensional breakdowns in Analysis Workspace.

## Step 2: Configure Environment Secrets

In your monitoring repository, navigate to **Settings > Secrets and variables > Actions** and store the following:

*   `PAT_TOKEN`: Your GitHub Personal Access Token (Fine-grained).
*   `ADOBE_RSID`: Your destination Report Suite ID.
*   `ADOBE_TRACKING_SERVER`: Your collection domain (e.g., `namespace.sc.omtrdc.net`).

## Step 3: Reporting in Analysis Workspace

Once the first sync is complete, leverage the data in **Analysis Workspace**:

1.  **Project Setup:** Create a new Freeform Table.
2.  **Dimensions:** Drop `eVar1` (Repo Name) as the primary row.
3.  **Metrics:** Add `event1` (Daily Views), `event2` (Daily Clones), and `event3` (Total Stars).
4.  **Drill-down:** Drag `eVar2` (File Path) onto a specific repository row to see folder-level engagement.
5.  **Calculated Metric:** Create a **Clone Conversion Rate** by dividing `Daily Clones` by `Daily Views` to measure asset utility.

## Implementation Audit

*   **Timestamp Check:** Verify in Report Suite Settings that "Timestamp Required" or "Timestamp Optional" is enabled to allow the API to backfill data to the correct hit time.
*   **Validation:** Inspect the status codes in the GitHub Action logs. A **200 OK** confirms that Adobe successfully received and queued the XML payload.

## Version History

| Version | Date | Changes |
| :--- | :--- | :--- |
| **1.0.0** | May 2026 | Initial Architecture: Full migration from AppMeasurement to Data Insertion API for automated GitHub auditing. |

**License:** MIT License - Developed by Dorian D. Regester
