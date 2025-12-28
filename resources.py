import json
import os

class Entry:
    
    printed = False
    
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        self.entries = [] if entries is None else entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self
        
    def json(self):
        res = {
            'title': self.title,
            'entries': [e.json() for e in self.entries]
        }
        return res
    
    @classmethod
    def from_json(cls, value):
        new_entry = cls(value['title'])
        for val in value.get('entries', []):
            new_entry.add_entry(cls.from_json(val))
        return new_entry
        
    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent+1)
            
    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as f:
            json.dump(self.json(), f)
    
    @classmethod            
    def load(cls, filename):
        with open(filename, 'r') as f:
            return cls.from_json(json.load(f))


class EntryManager:

    def __init__(self, data_path):
        self.data_path: str = data_path
        self.entries: list[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for dr in os.listdir(self.data_path):
            if dr.endswith('.json'):
                entry = Entry.load(os.path.join(self.data_path, dr))
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))
        
            
def print_with_indent(value, indent=0):
    tab = '\t' * indent
    print(f'{tab}{value}')
