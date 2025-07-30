#!/opt/homebrew/bin/python3
import sys
import os

def encode_dogs(dogs, encodings):    
    for encoding in encodings:       
        good_dogs = []     
        bad_dogs = []     
        char_count = 0  
        byte_count = 0
        for dog in dogs:        
            try:
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
    print(f"✅ {encoding}: {char_count} chars encoded in {byte_count} bytes, {bytes_per_char:.2f} bytes per char")        
    if bad_dogs:
        print(f"❌ {encoding}: {len(bad_dogs)} bad dogs:")
        for i in range(0, len(bad_dogs), 8):
            print(f"❌ {encoding}: " + '  '.join(bad_dogs[i:i+8]))    


def main():        
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: encode.py ENCODING1 [ENCODING2] < dogs.txt")
        sys.exit(1)

    enc1 = sys.argv[1]
    enc2 = sys.argv[2] if len(sys.argv) == 3 else None

    if not sys.stdin.isatty():
        dogs = [line.strip() for line in sys.stdin]
        if enc2:
            # comparison mode
            bad1 = set()
            bad2 = set()
            good1 = set()
            good2 = set()

            byte_count1 = 0
            byte_count2 = 0
            char_count1 = 0
            char_count2 = 0

            for dog in dogs:
                try:
                    encoded_dog = dog.encode(enc1)
                    byte_count1 += len(encoded_dog)
                    char_count1 += len(dog)
                    good1.add(dog)                    
                except UnicodeEncodeError:
                    bad1.add(dog)
                try:
                    encoded_dog = dog.encode(enc2)
                    byte_count2 += len(encoded_dog)
                    char_count2 += len(dog)
                    good2.add(dog)
                except UnicodeEncodeError:
                    bad2.add(dog)

            good_both = sorted(good1 & good2)
            bad_enc1_good_enc2 = sorted(bad1 & good2)
            good_enc1_bad_enc2 = sorted(good1 & bad2)
            bad_both = sorted(bad1 & bad2)
            
            if good_both:
                print(f"✅ {enc1} ✅ {enc2}: {len(good_both)} good dogs")
                for i in range(0, len(good_both), 12):
                    print("  " + "  ".join(good_both[i:i+12]))

            if bad_enc1_good_enc2:
                print(f"❌ {enc1} ✅ {enc2}: {len(bad_enc1_good_enc2)} bad dogs turned good")
                for i in range(0, len(bad_enc1_good_enc2), 12):
                    print("  " + "  ".join(bad_enc1_good_enc2[i:i+12]))
            if good_enc1_bad_enc2:
                print(f"✅ {enc1} ❌ {enc2}: {len(good_enc1_bad_enc2)} good dogs gone bad")
                for i in range(0, len(good_enc1_bad_enc2), 12):
                    print("  " + "  ".join(good_enc1_bad_enc2[i:i+12]))

            if bad_both:
                print(f"❌ {enc1} ❌ {enc2}: {len(bad_both)} bad dogs")
                for i in range(0, len(bad_both), 12):
                    print("  " + "  ".join(bad_both[i:i+12]))

            print(f"\n✅ {enc1}→{enc2}: {len(good_both)}→{len(good_both) + len(bad_enc1_good_enc2)} good dogs")
            print(f"✅ {enc1}: {char_count1} chars encoded in {byte_count1} bytes, {byte_count1 / char_count1:.2f} bytes per char")
            print(f"✅ {enc2}: {char_count2} chars encoded in {byte_count2} bytes, {byte_count2 / char_count2:.2f} bytes per char")
        else:
            # single encoding mode
            good = []
            bad = []
            for dog in dogs:
                try:
                    encoded_dog = dog.encode(enc1)
                    good.append(dog)
                except UnicodeEncodeError:
                    bad.append(dog)

            if bad:
                print(f"✅ {enc1}: {len(good)} good dogs")
                for i in range(0, len(good), 12):
                    print("  " + "  ".join(good[i:i+12]))

                print(f"❌ {enc1}: {len(bad)} bad dogs")
                for i in range(0, len(bad), 12):
                    print("  " + "  ".join(bad[i:i+12]))            

                byte_count = sum(len(dog.encode(enc1)) for dog in good)
                char_count = sum(len(dog) for dog in good)
                print(f"✅ {enc1}: {char_count} chars encoded in {byte_count} bytes, {byte_count / char_count:.2f} bytes per char\n")
            else:
                byte_count = sum(len(dog.encode(enc1)) for dog in good)
                char_count = sum(len(dog) for dog in good)
                print(f"✅ {enc1}: {len(good)} good dogs")
                print(f"✅ {enc1}: {char_count} chars encoded in {byte_count} bytes, {byte_count / char_count:.2f} bytes per char")

if __name__ == "__main__":    
    main()