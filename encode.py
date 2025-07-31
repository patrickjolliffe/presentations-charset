#!/opt/homebrew/bin/python3
import sys
import argparse
import codecs
from typing import Set, Tuple, List, Optional

# Constants
ITEMS_PER_ROW = 12
TICK = "✅"
CROSS = "❌"

def test_encoding(dogs: List[str], encoding: str) -> Tuple[Set[str], Set[str], int, int]:
    """Test which dogs can be encoded with the given encoding."""
    good_dogs = set()
    bad_dogs = set()
    char_count = 0
    byte_count = 0
    
    for dog in dogs:
        try:
            encoded_dog = dog.encode(encoding)
            good_dogs.add(dog)
            char_count += len(dog)
            byte_count += len(encoded_dog)
        except UnicodeEncodeError:
            bad_dogs.add(dog)
    
    return good_dogs, bad_dogs, char_count, byte_count

def print_dog_list(dogs: Set[str], items_per_row: int = ITEMS_PER_ROW) -> None:
    """Print dogs in rows with specified number of items per row."""
    dogs_sorted = sorted(dogs)
    for i in range(0, len(dogs_sorted), items_per_row):
        print("  " + "  ".join(dogs_sorted[i:i+items_per_row]))

def print_section(dogs: Set[str], status_text: str, description: str) -> None:
    """Print a section with dogs if the set is not empty."""
    if dogs:
        print()  # Always add blank line before section
        print(f"{status_text}: {len(dogs)} {description}")
        print_dog_list(dogs)

def validate_encoding(encoding: str) -> None:
    """Validate that an encoding name is supported."""
    try:
        codecs.lookup(encoding)
    except LookupError:
        print(f"Error: Unknown encoding '{encoding}'")
        sys.exit(1)

def print_encoding_stats(encoding: str, good_count: int, char_count: int, byte_count: int) -> None:
    """Print encoding statistics."""
    bytes_per_char = byte_count / char_count if char_count > 0 else 0
    print(f"{TICK} {encoding:<8}: {good_count} good dogs, {char_count} chars encoded in {byte_count:>4} bytes, {bytes_per_char:>4.2f} bytes per char")

def main() -> None:
    """
    Main entry point for the encoding compatibility test script.
    
    Parses command line arguments and orchestrates the encoding test process.
    """
    parser = argparse.ArgumentParser(
        description="Test character encoding compatibility with dog names from file",
        epilog="Examples:\n  %(prog)s 80dogs.txt utf-8\n  %(prog)s 80dogs.txt utf-8 ascii",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('filename', help='File containing dog names (one per line)')
    parser.add_argument('primary_encoding', help='Primary encoding to test')
    parser.add_argument('secondary_encoding', nargs='?', help='Optional second encoding for comparison')
    
    args = parser.parse_args()
    filename = args.filename
    primary_encoding = args.primary_encoding
    secondary_encoding = args.secondary_encoding

    # Validate encodings
    validate_encoding(primary_encoding)
    if secondary_encoding:
        validate_encoding(secondary_encoding)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dogs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
    
    if secondary_encoding:
        # Comparison mode
        print()  # Add blank line at the start
        good1, bad1, char_count1, byte_count1 = test_encoding(dogs, primary_encoding)
        good2, bad2, char_count2, byte_count2 = test_encoding(dogs, secondary_encoding)
        
        # Categorize dogs
        good_good = good1 & good2
        bad_good = bad1 & good2
        good_bad = good1 & bad2
        bad_bad = bad1 & bad2
        
        # Print results
        print_section(good_good, f"{TICK} {primary_encoding} {TICK} {secondary_encoding}", "good dogs")
        print_section(bad_good, f"{CROSS} {primary_encoding} {TICK} {secondary_encoding}", "dogs were bad, now good")
        print_section(good_bad, f"{TICK} {primary_encoding} {CROSS} {secondary_encoding}", "good dogs gone bad")
        print_section(bad_bad, f"{CROSS} {primary_encoding} {CROSS} {secondary_encoding}", "bad dogs")
        
        # Print summary statistics
        print()
        print_encoding_stats(primary_encoding, len(good1), char_count1, byte_count1)
        print_encoding_stats(secondary_encoding, len(good2), char_count2, byte_count2)
    
    else:
        # Single encoding mode
        print()  # Add blank line at the start
        good, bad, char_count, byte_count = test_encoding(dogs, primary_encoding)
        
        print_section(good, f"{TICK} {primary_encoding}", "good dogs")
        print_section(bad, f"{CROSS} {primary_encoding}", "bad dogs")
        
        print()
        print_encoding_stats(primary_encoding, len(good), char_count, byte_count)

if __name__ == "__main__":
    main()
