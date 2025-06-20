from summarizer import Summarizer
from notemanager import NoteManager

def main():
    """
    prompt for key.
    Initialize Summarizer and NoteManager.
    Load notes from file (optional).
    Show CLI menu:
        1. Add new note
        2. View notes
        3. Save notes
        4. Exit
    """
    key = input("Enter your OpenAI API key: ")
    summarizer = Summarizer(key)
    manager = NoteManager()
    manager.load_from_file()

    while True:
        print("\nMenu:")
        print("1. Add new note")
        print("2. View notes")
        print("3. Save notes")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            text = input("Enter text to summarize:\n")
            manager.add_note(text, summarizer)
            print("Note added and summarized.")
        elif choice == "2":
            manager.list_notes()
        elif choice == "3":
            manager.save_to_file()
            print("Notes saved.")
        elif choice == "4":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
