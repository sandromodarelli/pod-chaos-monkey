"""
Configuration module
"""
import os

NAMESPACE = os.getenv("NAMESPACE", "workloads")
LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()
SLEEP = int(os.getenv("SLEEP", "30"))
