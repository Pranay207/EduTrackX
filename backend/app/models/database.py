import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class Database:
    def __init__(self, db_file='database.json'):
        self.db_file = db_file
        self.data = self._load_db()
    
    def _load_db(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {
            'users': [],
            'subjects': [],
            'marks': [],
            'assignments': [],
            'attendance': [],
            'study_sessions': [],
            'notifications': [],
            'gamification': []
        }
    
    def _save_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def insert(self, collection: str, document: Dict) -> Dict:
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        document['created_at'] = datetime.now().isoformat()
        document['updated_at'] = datetime.now().isoformat()
        self.data[collection].append(document)
        self._save_db()
        return document
    
    def find(self, collection: str, query: Dict) -> List[Dict]:
        results = []
        for doc in self.data[collection]:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results
    
    def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        results = self.find(collection, query)
        return results[0] if results else None
    
    def update(self, collection: str, query: Dict, update: Dict) -> int:
        count = 0
        for doc in self.data[collection]:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                doc.update(update)
                doc['updated_at'] = datetime.now().isoformat()
                count += 1
        if count > 0:
            self._save_db()
        return count
    
    def delete(self, collection: str, query: Dict) -> int:
        initial_len = len(self.data[collection])
        self.data[collection] = [
            doc for doc in self.data[collection]
            if not all(doc.get(k) == v for k, v in query.items())
        ]
        count = initial_len - len(self.data[collection])
        if count > 0:
            self._save_db()
        return count
    
    def get_all(self, collection: str) -> List[Dict]:
        return self.data[collection]

db = Database()
