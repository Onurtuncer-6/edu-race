# routes/api.py
from flask import Blueprint, jsonify, request;
import psutil;
import platform;

api_bp = Blueprint('api', __name__, url_prefix='/api');

@api_bp.route("/health", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "project": [
            "Project Name: Edu-Race",
            "Description: School management system for educational institutions.",
            "version 1.0.0"
        ],
        "developer": {
            "GitHub": "profile/Onurtuncer-6"
        },
        "dependencies": [
            "Python 3.8+",
            "Flask 2.0+",
        ],
        "Timestamp": request.args.get("timestamp", "N/A")
    });

@api_bp.route("/monitor", methods=["GET"])
def monitor():
    # Ram usage information
    ram = psutil.virtual_memory();

    # Disk usage information
    disk = psutil.disk_usage('/');

    return jsonify({
        "server_info" : {
            "os": platform.system(),
            "os_release": platform.release(),
            "processor": platform.processor()
        },
        "cpu": {
            "usage_percent": psutil.cpu_percent(interval=1),
            "core_count": psutil.cpu_count()
        },
        "memory" : {
            "total_gb": round(ram.total / (1024 ** 3), 2),
            "used_gb": round(ram.used / (1024**3), 2),
            "percent": ram.percent
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "percent": disk.percent
        },
        "timestamp": request.args.get("timestamp", "N/A")
    })