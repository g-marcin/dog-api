import psutil
import os

# @deprecated @redundant: same machine-level metrics are already collected by
# node_exporter and shipped via Prometheus remote_write; see /performance route.
def check_system_performance():
    process = psutil.Process(os.getpid())
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    thread_count = process.num_threads()
    uptime_seconds = psutil.time.time() - process.create_time()
    
    return {
        'cpu_usage': f'{cpu_usage}%',
        'memory_usage': f'{memory_info.percent}%',
        'disk_usage': f'{disk_usage.percent}%',
        "thread_count": thread_count,
        "uptime_seconds": round(uptime_seconds, 2)
    }

def check_health():
    return "ok"