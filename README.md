# 🛡️ Python Network Packet Sniffer & IP Threat Analysis Dashboard

A Python-based network monitoring application that captures IP traffic, extracts source and destination IP addresses, checks destination IP reputation using the VirusTotal API, and displays the processed results through a Flask web dashboard.

---

## 📸 Project Dashboard

![Network Packet Sniffer Dashboard](/dashboard.png)

The dashboard displays recently captured network traffic along with the corresponding IP reputation status.

---

## 📌 Overview

This project demonstrates the use of **Python, Scapy, Flask, API integration, threading, caching, and network traffic analysis** to build a lightweight network monitoring application.

The application captures IP packets from network traffic using **Scapy**. For each newly observed destination IP address, the application queries the **VirusTotal API** and processes the returned analysis information to classify the address as:

* `SAFE`
* `MALICIOUS`
* `UNKNOWN`
* `ERROR`

The processed packet information is stored in memory and exposed through a Flask JSON endpoint. A web interface retrieves this information periodically and displays it in a simple monitoring dashboard.

---

## 🎯 Project Objectives

* Capture and inspect IP network traffic using Python.
* Extract source and destination IP addresses from captured packets.
* Identify newly observed destination IP addresses.
* Integrate an external threat-intelligence API for IP reputation analysis.
* Store and serve recent packet information through a Flask backend.
* Display captured information through a web-based dashboard.
* Apply caching to reduce repeated API requests.
* Run packet capture concurrently with the Flask application.

---

## 🏗️ System Architecture

```text
                 Network Traffic
                       │
                       ▼
              ┌─────────────────┐
              │  Scapy Sniffer  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  IP Detection   │
              │ Source / Dest.  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Duplicate Filter│
              │  Using `seen`   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  VirusTotal API │
              └────────┬────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │ IP Reputation Processing │
          └────────────┬─────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
       SAFE /                 UNKNOWN /
      MALICIOUS              ERROR
          │                         │
          └────────────┬────────────┘
                       ▼
              ┌─────────────────┐
              │  Data Store     │
              │ Latest 100      │
              │ Records         │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Flask Backend   │
              │    /data        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Web Dashboard   │
              └─────────────────┘
```

---

## ⚙️ How the Project Works

### 1. Packet Capture

The application uses **Scapy** to monitor network traffic.

When an IP packet is detected, the application checks whether the packet contains an IP layer.

The source and destination IP addresses are then extracted.

```python
src = packet[IP].src
dst = packet[IP].dst
```

---

### 2. Destination IP Filtering

The project maintains a `seen` set to keep track of destination IP addresses that have already been processed.

```python
seen = set()
```

This prevents the same destination IP from being repeatedly submitted for reputation checking during the current execution.

---

### 3. IP Reputation Checking

New destination IP addresses are sent to the VirusTotal API.

The application retrieves the analysis statistics associated with the IP address and checks the malicious count.

If malicious detections are present, the result is classified as:

```text
MALICIOUS
```

Otherwise, the current implementation classifies the result as:

```text
SAFE
```

If the API cannot provide a successful response, the application can return:

```text
UNKNOWN
```

or:

```text
ERROR
```

depending on the condition.

---

### 4. API Response Caching

The application maintains a cache:

```python
cache = {}
```

Once an IP address has been checked, its result is stored in the cache.

If the same IP address is requested again, the cached result can be returned instead of making another VirusTotal request.

This helps reduce unnecessary external API calls.

---

### 5. Data Storage

Processed packet information is stored in an in-memory list.

Each record contains:

```json
{
    "src": "source_ip",
    "dst": "destination_ip",
    "status": "SAFE"
}
```

The application returns the most recent 100 stored records.

---

### 6. Flask Backend

The project uses **Flask** to provide the backend web application.

The root route:

```text
/
```

loads the dashboard.

The:

```text
/data
```

endpoint returns packet information in JSON format.

Example:

```json
[
    {
        "src": "192.168.1.10",
        "dst": "8.8.8.8",
        "status": "SAFE"
    }
]
```

---

### 7. Background Packet Capture

Packet sniffing is started in a separate daemon thread.

This allows the packet-capture process to run concurrently with the Flask application.

The project therefore has two main activities:

```text
Packet Capture
      +
Flask Web Application
```

running together.

---

## 🧰 Technologies Used

| Technology         | Purpose                                      |
| ------------------ | -------------------------------------------- |
| **Python**         | Main programming language                    |
| **Scapy**          | Network packet capture and inspection        |
| **Flask**          | Backend web application                      |
| **Requests**       | HTTP communication with VirusTotal API       |
| **VirusTotal API** | IP reputation analysis                       |
| **HTML**           | Dashboard structure                          |
| **JavaScript**     | Fetching packet data from the Flask endpoint |
| **Threading**      | Running packet capture in the background     |
| **JSON**           | Data exchange between backend and dashboard  |

---

## 📁 Project Structure

```text
python-packet-sniffer/
│
├── app.py
│
├── sniffer.py
│
├── data_store.py
│
├── vt_check.py
│
├── templates/
│   └── index.html
│
├── screenshots/
│   └── dashboard.png
│
├── .env.example
│
├── .gitignore
│
├── requirements.txt
│
└── README.md
```

---

## 🔍 Main Components

### `app.py`

Responsible for:

* Creating the Flask application.
* Serving the dashboard.
* Providing the `/data` endpoint.
* Starting the packet sniffer.

---

### `sniffer.py`

Responsible for:

* Capturing network traffic using Scapy.
* Detecting IP packets.
* Extracting source and destination IP addresses.
* Filtering previously seen destination IPs.
* Calling the IP reputation checker.
* Sending processed information to the data store.
* Running the sniffer in a background thread.

---

### `data_store.py`

Responsible for:

* Maintaining captured packet information in memory.
* Adding new packet records.
* Returning the latest 100 records.

---

### `vt_check.py`

Responsible for:

* Communicating with the VirusTotal API.
* Checking destination IP reputation.
* Processing VirusTotal analysis statistics.
* Caching previously checked IP addresses.
* Returning the corresponding status.

---

### `templates/index.html`

Provides the web dashboard used to display the captured packet information returned by the Flask backend.

---

## 🔄 Data Flow

```text
Captured Packet
      │
      ▼
Check for IP Layer
      │
      ▼
Extract Source & Destination IP
      │
      ▼
Check Whether Destination IP Was Seen
      │
      ▼
New IP?
  │         │
 NO        YES
  │         │
  │         ▼
  │   VirusTotal API
  │         │
  │         ▼
  │   Process Reputation
  │         │
  │         ▼
  └──► Store Result
            │
            ▼
       Flask /data
            │
            ▼
       Web Dashboard
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/shravani1004/python-packet-sniffer.git
```

Move into the project directory:

```bash
cd python-packet-sniffer
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Key Configuration

The project uses the VirusTotal API.

Do **not** hard-code your real API key inside the source code.

Set the API key using an environment variable:

```text
VIRUSTOTAL_API_KEY=your_api_key_here
```

The repository includes `.env.example` as a template.

Your actual `.env` file should **never be uploaded to GitHub**.

---

## ▶️ Running the Application

After installing the dependencies and configuring the API key:

```bash
python app.py
```

Then open the Flask application in your browser:

```text
http://127.0.0.1:5000
```

The dashboard will display the packet information received from the backend.

---

## 🌐 API

### `GET /data`

Returns the recently processed packet information.

Example response:

```json
[
    {
        "src": "192.168.1.5",
        "dst": "8.8.8.8",
        "status": "SAFE"
    },
    {
        "src": "192.168.1.5",
        "dst": "example.ip",
        "status": "UNKNOWN"
    }
]
```

---

## 📊 Dashboard

The dashboard periodically requests data from:

```text
/data
```

and updates the displayed network traffic information.

The interface provides a simple view of:

* Source IP
* Destination IP
* IP reputation status

### Screenshot

Place your screenshot at:

```text
screenshots/dashboard.png
```

It will automatically appear near the top of this README.

---

## 🔐 Security Considerations

This project demonstrates basic security-conscious development practices.

### API key protection

The VirusTotal API key should be supplied through an environment variable instead of being committed to the repository.

### API timeout

The VirusTotal request uses a timeout so that an external API request does not wait indefinitely.

### API response handling

The application handles unsuccessful API responses and request exceptions by returning an appropriate status.

### Caching

Previously checked IP addresses are cached to reduce repeated external API requests.

---

## 🧠 Key Technical Concepts Demonstrated

### Python Network Programming

Working with packet-level network information using Python and Scapy.

### Packet Capture

Monitoring network traffic and identifying packets containing an IP layer.

### API Integration

Communicating with an external HTTP API and processing its JSON response.

### Backend Development

Building a Flask application and exposing packet information through a JSON endpoint.

### Data Processing

Extracting, organizing, and storing packet-related information.

### Caching

Using an in-memory cache to avoid unnecessary repeated IP reputation requests.

### Multithreading

Running the packet sniffer in a background daemon thread alongside the Flask application.

### Network Monitoring

Displaying captured network information through a web-based monitoring interface.

---

## 📚 Learning Outcomes

Through this project, I developed practical experience with:

* Python programming
* Network packet capture
* Scapy
* TCP/IP networking concepts
* Flask backend development
* JSON-based API responses
* External API integration
* HTTP requests
* API response processing
* Caching
* Background threading
* Network monitoring
* Debugging and problem solving

---

## 🔮 Possible Future Improvements

The current project can be extended with additional capabilities such as:

* Persistent database storage
* User authentication
* More detailed packet protocol analysis
* Improved dashboard visualizations
* Advanced logging
* Configurable monitoring filters
* Better error handling
* Performance monitoring
* Automated testing
* Containerized deployment

These are **future improvements and are not part of the current implementation**.

---

## ⚠️ Disclaimer

This project is intended for educational and network-monitoring purposes.

Only capture and analyze network traffic on systems and networks for which you have appropriate authorization.

---

## 👩‍💻 Author

**Shravani S**

Electronics & Communication Engineering

GitHub: [shravani1004](https://github.com/shravani1004)

LinkedIn: [Shravani S](https://www.linkedin.com/in/shravani-s-658a74304)

---

## ⭐ Project Highlights

```text
Python
   │
   ├── Scapy Packet Capture
   │
   ├── Flask Backend
   │
   ├── VirusTotal API
   │
   ├── IP Reputation Analysis
   │
   ├── Caching
   │
   ├── Threading
   │
   └── Web Dashboard
```

This project combines **network programming, backend development, API integration, data processing, and basic security analysis** into a single Python application.
