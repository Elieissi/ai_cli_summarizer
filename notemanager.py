
import json
from json import JSONDecodeError
from pathlib import Path

class NoteManager:
    def __init__(self):
        """Initialize with empty list of notes"""
        self.notes = []

    def add_note(self, text, summarizer):
        """
        Use Summarizer to generate summary.
        Store dict: { 'text': ..., 'summary': ... } in notes list.
        """
        summary = summarizer.summarize(text)
        self.notes.append({"text": text, "summary": summary})


    def list_notes(self):
        """
        Print all stored notes and their summaries.
        """
        for index, dic in enumerate(self.notes):
            print(f"{index}:\n{dic}\n")

    def save_to_file(self):
        """
        Save notes list (text + summary) to JSON file.
        """
        with open("notes.json", "w") as file:
            json.dump(self.notes, file, indent=4)

    
    def load_from_file(self):
        """
        Load notes list from JSON file into self.notes.
        """
        if Path("notes.json").exists(): 
            try:
                with open("notes.json", "r") as file:
                    contents = json.load(file)
                    if isinstance(contents, list):  # check if wrapped in list
                        for d in contents:  # for each dictionary in said list
                            if not isinstance(d, dict):  # if it's not a dict like I want
                                self.notes = []
                                return
                            if "text" not in d or "summary" not in d:  # missing keys
                                self.notes = []
                                return
                        self.notes = contents  # all checks pass
                        return
                    else:
                        self.notes = []
            except JSONDecodeError:  # malformed case
                with open("notes.json", "w") as file:
                    json.dump([], file, indent=4)
                self.notes = []
        else:  # if path doesn't exist
            with open("notes.json", "w") as file:
                json.dump([], file, indent=4)
            self.notes = []
