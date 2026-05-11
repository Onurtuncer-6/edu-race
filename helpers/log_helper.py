# helpers/log_helper.py
import logging;
from flask import request;
from datetime import datetime;
import os;

if not os.path.exists('log'):
    os.makedirs('log');

logging.basicConfig(
    filename="log/edurace_access.log",
    level=logging.INFO,
    format="%(message)s",
    encoding="utf-8"
)

def log_request():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S");
    ip = request.remote_addr;
    method = request.method;
    path = request.path;
    log_entry = f"[{now}] IP: {ip} | METHOD: {method} | Path: {path}";
    logging.info(log_entry);
    print(log_entry);