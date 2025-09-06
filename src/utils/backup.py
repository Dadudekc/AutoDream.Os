# src/utils/backup.py
from __future__ import annotations
import os
import shutil
from typing import List

class BackupManager:
    def __init__(self, root: str, dest: str) -> None:
        self.root = root
        self.dest = dest

    def create_backup(self, agents: List[str]) -> str:
        os.makedirs(self.dest, exist_ok=True)
        for a in agents:
            src = os.path.join(self.root, a)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(self.dest, a))
        return self.dest

    def rollback(self) -> None:
        # destructive rollback: restore directories from backup to root
        for name in os.listdir(self.dest):
            src = os.path.join(self.dest, name)
            dst = os.path.join(self.root, name)
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
