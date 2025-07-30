#!/opt/homebrew/bin/python3
import sys
import os
import argparse

def encode_ucs2 (text, encoding):
    # UCS-2 encoding is a fixed-length encoding that uses 2 bytes for each character
    # It can only represent characters in the Basic Multilingual Plane (BMP)
    # UCS-2 is not commonly used anymore, as UTF-16 is more widely adopted
    # However, we can still demonstrate how to encode a string using UCS-2
    if any(ord(c) > 0xFFFF for c in text):
        raise UnicodeEncodeError("ucs-2", text, -1, -1, "Character outside BMP not allowed in UCS-2")
  
    # Use equivalent UTF-16 encoding to simulate UCS-2
    encoding_map = {
        "ucs-2le": "utf-16le",
        "ucs-2be": "utf-16be",
        "ucs-2"   : "utf-16"

    }
    return text.encode(encoding_map[encoding])

def encode_dogs(dogs, encodings):    
    for encoding in encodings:       
        good_dogs = []     
        bad_dogs = []     
        char_count = 0  
        byte_count = 0
        for dog in dogs:        
            try:
                if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                    encoded_dog = encode_ucs2(dog, encoding)
                else:
                    encoded_dog = dog.encode(encoding)                
                good_dogs.append(dog)
                hex_string = ' '.join(f"{b:02X}" for b in encoded_dog)
                print(f"✅ {encoding + ':':<8} Good {dog} [{hex_string.lower()}] ({len(encoded_dog)} bytes)")                
            except UnicodeEncodeError:                                
                print(f"❌ {encoding + ':':<8} Bad {dog}")                            


def encode_all_dogs(dogs, encoding):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0
    for dog in dogs:        
        try:
            if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                encoded_dog = encode_ucs2(dog, encoding)
            else:
                encoded_dog = dog.encode(encoding)                

            good_dogs.append(dog)
            byte_count += len(encoded_dog)
            char_count += len(dog)
        except UnicodeEncodeError:
            bad_dogs.append(dog)

    bytes_per_char = byte_count / char_count if char_count else 0        
    print(f"✅ {encoding}: {len(good_dogs)} good dogs")        
    print(f"✅ {encoding}: {char_count} chars encoded in {byte_count} bytes, {bytes_per_char:.1f} bytes per char")        
    if bad_dogs:
        print(f"❌ {encoding}: {len(bad_dogs)} bad dogs:")
        for i in range(0, len(bad_dogs), 8):
            print(f"❌ {encoding}: " + '  '.join(bad_dogs[i:i+8]))
    else:
        print("✅  No bad dogs")


def process_text(texts, encodings, binary=False):    
    good_dogs = []     
    bad_dogs = []     
    char_count = 0  
    byte_count = 0

    for encoding in encodings:
        for text in texts.split(','):
            try:
                if encoding == "ucs-2" or encoding == "ucs-2le" or encoding == "ucs-2be":
                    encoded_text = encode_ucs2(text, encoding)
                else:
                    encoded_text = text.encode(encoding)                
                if binary:
                    bin_string = ' '.join(f"{b:08b}" for b in encoded_text)
                    print(f"✅ {encoding + ':':<8} \"{text}\"=[{bin_string}]")
                else:
                    hex_string = ' '.join(f"{b:02X}" for b in encoded_text)
                    print(f"✅ {encoding + ':':<8} \"{text}\"=[{hex_string.lower()}]")
            except UnicodeEncodeError:
                print(f"❌ {encoding}: Failed to encode {text}")

def main():        
    parser = argparse.ArgumentParser(description="Check if text can be encoded with a given encoding, and report good and bad dogs.")
    parser.add_argument("encodings", help="Comma-separated of encodings (e.g., ascii,utf-8,utf-16)")
    parser.add_argument("text", nargs="?", help="Comma-separated of text to encode (e.g., WOOF,woof)")
    parser.add_argument("--list", action="store_true", help="List good and bad dogs after encoding")

    parser.add_argument("-f", "--file", action="store_true", help="Process dogs.txt")
    parser.add_argument("-d", "--dogs", help="Comma-separated dogs to process")   
    parser.add_argument("-b", "--binary", action="store_true", help="Output in binary instead of hexadecimal")

    args = parser.parse_args()

    encodings = args.encodings.split(',')        

    if args.text:        
        process_text(args.text, encodings, args.binary)
        sys.exit(1)
    elif args.dogs:        
        dogs = [dog.strip() for dog in args.dogs.split(',')]        
        encode_dogs(dogs, encodings)
    elif not sys.stdin.isatty():
        # Reading from stdin (e.g., encode.py utf-8 < dogs.txt)
        dogs = [line.strip() for line in sys.stdin]
        encode_all_dogs(dogs, encodings[0])
    else:
        print("Either --file, --dogs, --text, or piped input must be provided.")
        sys.exit(1)

if __name__ == "__main__":
    print ("__Main__")
    main()