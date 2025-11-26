from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class TargetFingerprint:
    allowed_extensions: List[str] = field(default_factory=list)
    allowed_mimes: List[str] = field(default_factory=list)
    rejected_extensions: List[str] = field(default_factory=list)
    upload_dir_leaked: bool = False
    upload_path: Optional[str] = None
    server_technologies: List[str] = field(default_factory=list)

class TargetProfile:
    def __init__(self, url, method="POST", file_field="file", other_fields=None):
        self.url = url
        self.method = method
        self.file_field = file_field
        self.other_fields = other_fields if other_fields else {}
        self.fingerprint = TargetFingerprint()

    def update_fingerprint(self, fingerprint: TargetFingerprint):
        self.fingerprint = fingerprint
