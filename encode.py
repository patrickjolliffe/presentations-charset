#!/opt/homebrew/bin/python3
import sys

def test_encoding(dogs, encoding):
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

def print_dog_list(dogs, items_per_row=12):
    """Print dogs in rows with specified number of items per row."""
    dogs_sorted = sorted(dogs)
    for i in range(0, len(dogs_sorted), items_per_row):
        print("  " + "  ".join(dogs_sorted[i:i+items_per_row]))

def print_encoding_stats(encoding, good_count, char_count, byte_count):
    """Print encoding statistics."""
    bytes_per_char = byte_count / char_count if char_count > 0 else 0
    print(f"✅ {encoding:<8}: {good_count} good dogs, {char_count} chars encoded in {byte_count:>4} bytes, {bytes_per_char:>4.2f} bytes per char")

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: encode.py ENCODING1 [ENCODING2] < dogs.txt")
        sys.exit(1)

    enc1 = sys.argv[1]
    enc2 = sys.argv[2] if len(sys.argv) == 3 else None

    if sys.stdin.isatty():
        print("No input provided. Please pipe dog names through stdin.")
        sys.exit(1)

    dogs = [line.strip() for line in sys.stdin if line.strip()]
    
    if enc2:
        # Comparison mode
        print()  # Add blank line at the top
        good1, bad1, char_count1, byte_count1 = test_encoding(dogs, enc1)
        good2, bad2, char_count2, byte_count2 = test_encoding(dogs, enc2)
        
        # Categorize dogs
        good_both = good1 & good2
        bad_enc1_good_enc2 = bad1 & good2
        good_enc1_bad_enc2 = good1 & bad2
        bad_both = bad1 & bad2
        
        # Print results
        first_section = True
        
        if good_both:
            if not first_section:
                print()
            print(f"✅ {enc1} ✅ {enc2}: {len(good_both)} good dogs")
            print_dog_list(good_both)
            first_section = False
        
        if bad_enc1_good_enc2:
            if not first_section:
                print()
            print(f"❌ {enc1} ✅ {enc2}: {len(bad_enc1_good_enc2)} dogs were bad, now good")
            print_dog_list(bad_enc1_good_enc2)
            first_section = False
        
        if good_enc1_bad_enc2:
            if not first_section:
                print()
            print(f"✅ {enc1} ❌ {enc2}: {len(good_enc1_bad_enc2)} good dogs gone bad")
            print_dog_list(good_enc1_bad_enc2)
            first_section = False
        
        if bad_both:
            if not first_section:
                print()
            print(f"❌ {enc1} ❌ {enc2}: {len(bad_both)} bad dogs")
            print_dog_list(bad_both)
        
        # Print summary statistics
        print()
        print_encoding_stats(enc1, len(good1), char_count1, byte_count1)
        print_encoding_stats(enc2, len(good2), char_count2, byte_count2)
    
    else:
        # Single encoding mode
        print()  # Add blank line at the top
        good, bad, char_count, byte_count = test_encoding(dogs, enc1)
        
        print(f"✅ {enc1}: {len(good)} good dogs")
        print_dog_list(good)
        
        if bad:
            print()
            print(f"❌ {enc1}: {len(bad)} bad dogs")
            print_dog_list(bad)
        
        print()
        print_encoding_stats(enc1, len(good), char_count, byte_count)

if __name__ == "__main__":
    main()
