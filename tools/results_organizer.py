import os
import json
from datetime import datetime
from typing import Optional, Dict, Any

class ResultsOrganizer:
    def __init__(self, base_results_dir: str = "results"):
        self.base_results_dir = base_results_dir
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        if not os.path.exists(self.base_results_dir):
            os.makedirs(self.base_results_dir, exist_ok=True)
    
    def get_tool_results_dir(self, tool_name: str) -> str:
        tool_dir = os.path.join(self.base_results_dir, tool_name)
        if not os.path.exists(tool_dir):
            os.makedirs(tool_dir, exist_ok=True)
        return tool_dir
    
    def get_session_dir(self, tool_name: str, session_time: Optional[datetime] = None) -> str:
        if session_time is None:
            session_time = datetime.now()
        
        timestamp = session_time.strftime("%Y-%m-%d_%H-%M-%S")
        tool_dir = self.get_tool_results_dir(tool_name)
        session_dir = os.path.join(tool_dir, timestamp)
        
        if not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)
        
        return session_dir
    
    def get_hits_file_path(self, tool_name: str, session_time: Optional[datetime] = None) -> str:
        session_dir = self.get_session_dir(tool_name, session_time)
        return os.path.join(session_dir, "hit.txt")
    
    def get_stats_file_path(self, tool_name: str, session_time: Optional[datetime] = None) -> str:
        session_dir = self.get_session_dir(tool_name, session_time)
        return os.path.join(session_dir, "stats.json")
    
    def save_hit(self, tool_name: str, hit_data: str, session_time: Optional[datetime] = None):
        hits_file = self.get_hits_file_path(tool_name, session_time)
        
        with open(hits_file, "a", encoding="utf-8") as f:
            f.write(f"{hit_data}\n")
    
    def save_stats(self, tool_name: str, stats: Dict[str, Any], session_time: Optional[datetime] = None):
        stats_file = self.get_stats_file_path(tool_name, session_time)
        
        stats['session_time'] = session_time.strftime("%Y-%m-%d %H:%M:%S") if session_time else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats['tool_name'] = tool_name
        
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def get_latest_hits(self, tool_name: str) -> Optional[str]:
        tool_dir = self.get_tool_results_dir(tool_name)
        
        if not os.path.exists(tool_dir):
            return None
        
        session_dirs = [d for d in os.listdir(tool_dir) if os.path.isdir(os.path.join(tool_dir, d))]
        session_dirs.sort(reverse=True)
        
        if not session_dirs:
            return None
        
        latest_session = session_dirs[0]
        return os.path.join(tool_dir, latest_session, "hit.txt")
    
    def get_tool_summary(self, tool_name: str) -> Dict[str, Any]:
        tool_dir = self.get_tool_results_dir(tool_name)
        
        if not os.path.exists(tool_dir):
            return {"total_sessions": 0, "total_hits": 0}
        
        total_hits = 0
        sessions = []
        
        for session_dir in os.listdir(tool_dir):
            session_path = os.path.join(tool_dir, session_dir)
            if os.path.isdir(session_path):
                hits_file = os.path.join(session_path, "hit.txt")
                stats_file = os.path.join(session_path, "stats.json")
                
                hit_count = 0
                if os.path.exists(hits_file):
                    with open(hits_file, "r", encoding="utf-8") as f:
                        hit_count = len([line for line in f.readlines() if line.strip()])
                
                stats = {}
                if os.path.exists(stats_file):
                    try:
                        with open(stats_file, "r", encoding="utf-8") as f:
                            stats = json.load(f)
                    except:
                        pass
                
                sessions.append({
                    "session": session_dir,
                    "hits": hit_count,
                    "stats": stats
                })
                
                total_hits += hit_count
        
        return {
            "total_sessions": len(sessions),
            "total_hits": total_hits,
            "sessions": sessions
        }