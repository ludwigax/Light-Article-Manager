import os
import json
from typing import List, Dict
from collections import UserDict, namedtuple, UserList

class Sylva(UserList):
    sylva_path = "./cache/sylva.json"

    def __setattr__(self, name: str, value: list) -> None: # deprecated
        try:
            if name in ['data', '_next_id', '_index']:
                super().__setattr__(name, value)
            else:
                for item in self.data:
                    if item['name'] == name:
                        item['data'] = value
                        return
                self.data.append({'name': name, 'data': value})
        except Exception as e:
            raise AttributeError(f"Error setting attribute {name}: {e}")
    
    def __getattr__(self, name: str) -> list:
        try:
            for item in self.data:
                if item['name'] == name:
                    return item
            raise AttributeError(f"No such attribute: {name}")
        except KeyError as e:
            raise AttributeError(f"Error getting attribute {name}: {e}")
        
    def setitem(self, id: int, name: str = None, value: list = None) -> None:
        item = self.index(id)
        if not item:
            raise ValueError(f"No such id: {id}")
        if name is not None:
            item['name'] = name
        if value is not None:
            item['data'] = value

    def newitem(self, name: str, value: list = []):
        if name is None:
            raise ValueError("Name cannot be None")
        if value is None:
            value = []
        self.data.append({
            'name': name,
            'data': value,
            'id': self._next_id
        })
        self._next_id += 1
        self._index = [data["id"] for data in self.data]
        return self.data[-1]

    def newitem_at(self, idx: int, name: str, value: list = []):
        if name is None:
            raise ValueError("Name cannot be None")
        if value is None:
            value = []
        self.data.insert(idx, {
            'name': name,
            'data': value,
            'id': self._next_id
        })
        self._next_id += 1
        self._index = [data["id"] for data in self.data]
        return self.data[idx]

    def delitem(self, id: int) -> None:
        idx = self._index.index(id)
        if idx:
            self.data.pop(idx)
            self._index = [data["id"] for data in self.data]
        else:
            raise ValueError(f"No such id: {id}")
        
    def find(self, name: str):
        for item in self.data:
            if item['name'] == name:
                return item
        return None
    
    def index(self, id: int):
        idx = self._index.index(id)
        if idx:
            return self.data[idx]
        return None
        
    def load(self) -> None:
        if not os.path.exists(Sylva.sylva_path):
            with open(Sylva.sylva_path, 'w') as f:
                json.dump({}, f)
        with open(Sylva.sylva_path, 'r') as f:
            data = json.load(f)
        self.data = data.get('stores', [])
        self._next_id = data.get('next_id', 0)
        self._index = data.get('index', [])

    def save(self) -> None:
        data = {
            'next_id': self._next_id,
            'stores': self.data,
            'index': self._index
        }
        with open(Sylva.sylva_path, 'w') as f:
            json.dump(data, f, indent=4)

# retieve data from database and give a inferface to access it
class NamedDict(UserDict):
    def __init__(self, **kwargs):
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in self._fields()}
        super().__init__(filtered_kwargs)
        for key in self._fields():
            if key not in self.data:
                self.data[key] = None

    def _fields(self):
        raise NotImplementedError
    
    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if key in self._fields():
            self.data[key] = value
        else:
            super().__setattr__(key, value)

    @property
    def id(self):
        return self.data['id']

    def to_dict(self):
        return dict(self.data)
    
    def to_space(self):
        for key in self._fields():
            if self.data[key] is None:
                self.data[key] = ''
        return self
    
FolderData = lambda folder_id, folder_name: ArticleData(id=folder_id, title=folder_name)
    
class ArticleData(NamedDict):
    def _fields(self):
        return ['id', 'title', 'author', 'journal', 'year', 'doi', 'local_path', 'add_time', 'abstract']
    
class NoteData(NamedDict):
    def _fields(self):
        return ['id', 'title', 'note', 'add_time', 'changed_time', 'quote', 'torder']
    
class AnnotationData(NamedDict):
    def _fields(self):
        return ['id', 'annot', 'refer', 'page_number', 'add_time', 'changed_time', 'colour', 'torder']

                         