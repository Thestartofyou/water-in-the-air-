import datetime
import sqlite3

# Create or connect to a SQLite database
conn = sqlite3.connect('keycard_tracker.db')
cursor = conn.cursor()

# Create a table to store key card entry data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entry_log (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id TEXT,
        entry_timestamp TIMESTAMP
    )
''')
conn.commit()

def log_entry(card_id):
    entry_timestamp = datetime.datetime.now()
    
    # Insert the entry into the database
    cursor.execute('INSERT INTO entry_log (card_id, entry_timestamp) VALUES (?, ?)', (card_id, entry_timestamp))
    conn.commit()

def track_pattern(card_id, days=7):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    
    # Retrieve entry data for the specified card within the past 'days' days
    cursor.execute('SELECT entry_timestamp FROM entry_log WHERE card_id = ? AND entry_timestamp >= ? AND entry_timestamp <= ?', (card_id, start_date, end_date))
    entries = cursor.fetchall()
    
    if len(entries) == 0:
        return f"No entries found for card {card_id} in the last {days} days."
    
    # Extract the time of day from each entry and count occurrences
    time_counts = {}
    for entry in entries:
        entry_time = entry[0].strftime('%H:%M')
        if entry_time in time_counts:
            time_counts[entry_time] += 1
        else:
            time_counts[entry_time] = 1
    
    # Sort the time counts by entry time
    sorted_counts = sorted(time_counts.items(), key=lambda x: x[0])
    
    # Print the pattern
    print(f"Entry pattern for card {card_id} in the last {days} days:")
    for entry_time, count in sorted_counts:
        print(f"{entry_time}: {count} entries")
    
    return sorted_counts

if __name__ == "__main__":
    card_id = "your_key_card_id"
    log_entry(card_id)
    pattern_data = track_pattern(card_id)

