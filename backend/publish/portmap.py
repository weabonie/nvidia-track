# portmap.py
import json, os, random, socket
from pathlib import Path

class PortMap:
    def __init__(self, path: Path, base: int = 18080, limit: int = 2000):
        self.path = Path(path)
        self.base = base
        self.limit = limit
        self._load()

    def _load(self):
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {}
            self._save()

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def _is_port_in_use(self, port: int) -> bool:
        """Check if a port is already in use on the system"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return False
            except OSError:
                return True

    def assign(self, slug: str) -> int:
        if slug in self.data:
            # Check if previously assigned port is still free
            port = self.data[slug]
            if not self._is_port_in_use(port):
                return port
            # If in use, reassign
            
        # deterministic but spread: hash to a window
        rng = random.Random(slug)
        port = self.base + rng.randrange(self.limit)
        
        # avoid collisions with both our map AND system ports
        max_attempts = 100
        attempts = 0
        while (port in self.data.values() or self._is_port_in_use(port)) and attempts < max_attempts:
            port = self.base + rng.randrange(self.limit)
            attempts += 1
            
        if attempts >= max_attempts:
            raise RuntimeError(f"Could not find available port after {max_attempts} attempts")
            
        self.data[slug] = port
        self._save()
        return port
