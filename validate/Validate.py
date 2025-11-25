def load_dataset(filepath):
    """Loads a comma-separated dataset and returns a list of integers."""
    try:
        with open(filepath, "r") as file:
            data = file.read().strip()
            return [int(x) for x in data.split(",")]
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return []
    except ValueError:
        print(f"[ERROR] File contains invalid/non-integer values: {filepath}")
        return []