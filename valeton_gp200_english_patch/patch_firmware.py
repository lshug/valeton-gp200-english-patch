#!/usr/bin/env python3
"""
Valeton Firmware Patcher
Translates Valeton guitar processor firmware from Chinese to English.

Supports:
- GP-50 (V1.0.5)
- GP-200 (V1.0.5)

Usage:
    python3 patch_firmware.py -i <firmware.bin> [-o <output.bin>] [--device gp200|gp50]
    python3 patch_firmware.py --scan <firmware.bin>  # Scan and generate translations JSON
    python3 patch_firmware.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Type alias for CJK string info
CJKStringInfo = dict[str, str | int]

CHECKSUM_OFFSET = 0x0E


def find_cjk_strings(data: bytes, search_start: int = 0, search_end: int | None = None) -> list[CJKStringInfo]:
    """
    Find all CJK (Chinese/Japanese/Korean) UTF-8 strings in a byte range.

    Args:
        data: Firmware binary data
        search_start: Start offset for scanning
        search_end: End offset for scanning (default: end of data)

    Returns:
        List of dictionaries with offset, string, and byte_length
    """
    if search_end is None:
        search_end = len(data)

    cjk_strings: list[CJKStringInfo] = []
    i = search_start

    while i < search_end - 2:
        # Check for CJK UTF-8 character start byte
        # E4-E9 covers CJK Unified Ideographs and common Japanese
        if 0xE4 <= data[i] <= 0xE9:
            # Find the start of the string (go back to find null or boundary)
            start = i
            while start > search_start and data[start - 1] != 0:
                start -= 1

            # Find the end (null terminator)
            end = i
            while end < search_end and data[end] != 0:
                end += 1

            if end > i:
                try:
                    string_bytes = data[start:end]
                    decoded = string_bytes.decode("utf-8")

                    # Count CJK characters (Chinese + Japanese Hiragana/Katakana)
                    cjk_chars = sum(
                        1
                        for c in decoded
                        if "\u4e00" <= c <= "\u9fff"  # CJK Unified
                        or "\u3040" <= c <= "\u30ff"
                    )  # Hiragana/Katakana

                    # Filter: must have meaningful CJK content
                    if cjk_chars >= 1 and len(decoded) >= 1:
                        # Skip if mostly non-printable
                        printable = sum(1 for c in decoded if c.isprintable() or c == "\n")
                        if printable >= len(decoded) * 0.8:
                            cjk_strings.append(
                                {
                                    "offset": start,
                                    "string": decoded,
                                    "byte_length": len(string_bytes),
                                }
                            )
                            i = end
                except (UnicodeDecodeError, ValueError):
                    pass
        i += 1

    # Remove duplicates while preserving first occurrence
    seen: set[str] = set()
    unique_strings: list[CJKStringInfo] = []
    for item in cjk_strings:
        string_val = str(item["string"])
        if string_val not in seen:
            seen.add(string_val)
            unique_strings.append(item)

    return unique_strings


def load_translations(json_path: str) -> dict[str, str]:
    """Load translations from a JSON file."""
    with open(json_path, encoding="utf-8") as f:
        result: dict[str, str] = json.load(f)
        return result


def save_translations(translations: dict[str, str], json_path: str) -> None:
    """Save translations to a JSON file."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)


def detect_device_type(data: bytes) -> tuple[str, str, bool]:
    """
    Detect the device type and version from firmware.

    Returns:
        Tuple of (device_name, version_string, is_valid)
    """
    # Check for GP-50 version at offset 0x90
    gp50_version_offset = 0x90
    if len(data) > gp50_version_offset + 4:
        version_bytes = data[gp50_version_offset : gp50_version_offset + 4]
        try:
            version_str = version_bytes.decode("ascii")
            if version_str == "V105":
                return "GP-50", "V1.0.5", True
        except Exception:
            pass

    # Check for GP-200 - larger firmware with specific characteristics
    # GP-200 firmware is typically larger (6+ MB)
    if len(data) > 6000000:
        # Look for GP-200 specific markers
        # The string region at 0x415xxx is characteristic of GP-200
        if len(data) > 0x415000:
            return "GP-200", "Unknown", True

    return "Unknown", "Unknown", False


def get_string_regions(device: str) -> list[tuple[int, int | None]]:
    """
    Get the regions containing translatable strings for a device.

    Returns:
        List of tuples (start_offset, end_offset)
    """
    if device == "GP-50":
        return [(0x165840, 0x166000)]
    elif device == "GP-200":
        # GP-200 has strings in the 0x415xxx region
        return [(0x415000, 0x41A000)]
    else:
        # Default: scan entire firmware
        return [(0, None)]


def patch_firmware(
    data: bytearray,
    translations: dict[str, str],
    regions: list[tuple[int, int | None]],
    verbose: bool = True,
) -> tuple[int, int, list[str]]:
    """
    Apply translations to firmware data.

    Args:
        data: Mutable firmware data (bytearray)
        translations: Dictionary mapping original strings to translations
        regions: List of (start, end) tuples defining scan regions
        verbose: Print progress information

    Returns:
        Tuple of (patched_count, skipped_count, error_messages)
    """
    patched = 0
    skipped = 0
    errors: list[str] = []

    for region_start, region_end in regions:
        if region_end is None:
            region_end = len(data)

        if verbose:
            print(f"Scanning region: 0x{region_start:X} - 0x{region_end:X}")

        # Find all strings in this region
        strings = find_cjk_strings(bytes(data), region_start, region_end)

        if verbose:
            print(f"Found {len(strings)} CJK strings in region")

        # Build a list of all string positions for boundary calculation
        string_positions = [(s["offset"], s["byte_length"]) for s in strings]
        string_positions.sort(key=lambda x: x[0] if isinstance(x[0], int) else 0)

        for s in strings:
            original = str(s["string"])
            offset = int(s["offset"])
            original_len = int(s["byte_length"])

            # Check if we have a translation
            if original not in translations:
                continue

            translation = translations[original]

            # Skip PLACEHOLDER entries (not yet translated)
            if translation == "PLACEHOLDER":
                continue

            # Calculate available space
            # We should only use the original string's byte length for padding,
            # NOT the space to the next CJK string (which may include English strings)
            available_space = original_len

            # Encode original and translation
            original_bytes = original.encode("utf-8")
            trans_bytes = translation.encode("utf-8")

            # Special handling for strings that end with a digit (e.g., "脚钉 4", "外部フットスイッチ4")
            # The firmware uses pointers to digit positions for parameter values like Mode 1/2/3/4
            # We must preserve the digit at its exact original byte offset
            if len(original_bytes) >= 1 and chr(original_bytes[-1]).isdigit():
                digit = chr(original_bytes[-1])
                digit_pos = original_len - 1  # Position of digit in original (0-indexed)

                # Check if translation ends with the same digit
                if trans_bytes[-1:] == digit.encode():
                    # Preserve digit position: write prefix + null padding + digit
                    prefix = trans_bytes[:-1]  # Translation without the digit

                    if len(prefix) + 1 <= original_len:  # +1 for the digit
                        for j in range(original_len):
                            if j < len(prefix):
                                data[offset + j] = prefix[j]
                            elif j == digit_pos:
                                data[offset + j] = ord(digit)
                            else:
                                data[offset + j] = 0x00
                        patched += 1
                        continue

            # Normal patching for strings that don't end with digits
            translation_bytes = trans_bytes + b"\x00"

            if len(translation_bytes) > available_space:
                errors.append(f"Translation too long at 0x{offset:X}: '{translation}' ({len(translation_bytes)} > {available_space} bytes)")
                skipped += 1
                continue

            # Apply the patch - only overwrite the original string's bytes
            for j in range(original_len):
                if j < len(translation_bytes):
                    data[offset + j] = translation_bytes[j]
                else:
                    data[offset + j] = 0x00  # Null padding

            patched += 1

    return patched, skipped, errors


def calculate_checksum(data: bytes) -> int:
    """
    Calculate the GP-200 firmware checksum.

    The checksum is a simple byte sum from offset 0x30 to end of file,
    truncated to 8 bits (mod 256).

    Args:
        data: Firmware binary data

    Returns:
        Checksum byte (0-255)
    """
    return sum(data[0x30:]) & 0xFF


def update_checksum(data: bytearray, verbose: bool = True) -> int:
    """
    Update the checksum byte in the firmware header.

    The checksum is stored at offset 0x0E and covers bytes from 0x30 to EOF.

    Args:
        data: Mutable firmware data (bytearray)
        verbose: Print progress information

    Returns:
        The new checksum value
    """

    old_checksum = data[CHECKSUM_OFFSET]
    new_checksum = calculate_checksum(bytes(data))

    if verbose:
        print("\nChecksum update:")
        print(f"  Old checksum at 0x{CHECKSUM_OFFSET:02X}: 0x{old_checksum:02X}")
        print(f"  New checksum: 0x{new_checksum:02X}")

    data[CHECKSUM_OFFSET] = new_checksum

    if verbose:
        if old_checksum != new_checksum:
            print("  Checksum updated successfully")
        else:
            print("  Checksum unchanged (no modifications affected checksum range)")

    return new_checksum


def verify_checksum(data: bytes) -> bool:
    """
    Verify that the firmware checksum is correct.

    Args:
        data: Firmware binary data

    Returns:
        True if checksum is valid, False otherwise
    """
    stored = data[0x0E]
    computed = calculate_checksum(data)
    return stored == computed


def scan_and_generate_json(firmware_path: str, output_json: str, regions: list[tuple[int, int | None]] | None = None) -> None:
    """
    Scan firmware for CJK strings and generate a translations JSON file.
    All translations are set to 'PLACEHOLDER'.
    """
    with open(firmware_path, "rb") as f:
        data = f.read()

    device, version, is_valid = detect_device_type(data)
    print(f"Detected device: {device} ({version}), is_valid: {is_valid}")

    if regions is None:
        regions = get_string_regions(device)

    all_strings: list[CJKStringInfo] = []
    for start, end in regions:
        strings = find_cjk_strings(data, start, end)
        all_strings.extend(strings)

    # Deduplicate
    seen: set[str] = set()
    unique_strings: list[CJKStringInfo] = []
    for s in all_strings:
        string_val = str(s["string"])
        if string_val not in seen:
            seen.add(string_val)
            unique_strings.append(s)

    # Create translations dict with PLACEHOLDER values
    translations: dict[str, str] = {str(s["string"]): "PLACEHOLDER" for s in unique_strings}

    save_translations(translations, output_json)

    print(f"Found {len(translations)} unique CJK strings")
    print(f"Translations template saved to: {output_json}")
    print("\nEdit the JSON file to add English translations, then run the patcher.")

    # Also print a summary by character type
    simplified = sum(1 for s in unique_strings if any("\u4e00" <= c <= "\u9fff" for c in str(s["string"])))
    print(f"Strings with CJK characters: {simplified}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Valeton Firmware Patcher - Translate firmware from Chinese to English",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan firmware and generate translations template
  python3 patch_firmware.py --scan firmware.bin

  # Patch firmware using translations file
  python3 patch_firmware.py -i firmware.bin -t translations_gp200.json

  # Patch with custom output file
  python3 patch_firmware.py -i firmware.bin -o patched.bin -t translations.json

  # Force patching (skip version check)
  python3 patch_firmware.py -i firmware.bin -t translations.json --force
""",
    )
    data: bytes | bytearray

    parser.add_argument("-i", "--input", metavar="FILE", help="Input firmware file")
    parser.add_argument("-o", "--output", metavar="FILE", help="Output firmware file (default: <input>-patched.bin)")
    parser.add_argument("-t", "--translations", metavar="FILE", help="JSON file with translations")
    parser.add_argument("--scan", metavar="FILE", help="Scan firmware and generate translations template JSON")
    parser.add_argument(
        "--scan-output",
        metavar="FILE",
        help="Output JSON file for --scan (default: translations_<device>.json)",
    )
    parser.add_argument(
        "--device",
        choices=["gp50", "gp200", "auto"],
        default="auto",
        help="Device type (default: auto-detect)",
    )
    parser.add_argument("--force", action="store_true", help="Skip version validation")
    parser.add_argument(
        "-r",
        "--region",
        nargs=2,
        metavar=("START", "END"),
        help="Custom hex region to patch (e.g., -r 0x415000 0x41A000)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Scan mode
    if args.scan:
        if not os.path.exists(args.scan):
            print(f"Error: File not found: {args.scan}", file=sys.stderr)
            sys.exit(1)

        # Determine output filename
        with open(args.scan, "rb") as f:
            data = f.read()
        device, _, _ = detect_device_type(data)

        output_json = args.scan_output or f"translations_{device.lower().replace('-', '')}.json"

        regions: list[tuple[int, int | None]] | None = None
        if args.region:
            try:
                start = int(args.region[0], 16) if args.region[0].startswith("0x") else int(args.region[0])
                end = int(args.region[1], 16) if args.region[1].startswith("0x") else int(args.region[1])
                regions = [(start, end)]
            except ValueError:
                print("Error: Invalid region format", file=sys.stderr)
                sys.exit(1)

        scan_and_generate_json(args.scan, output_json, regions)
        sys.exit(0)

    # Patch mode
    if not args.input:
        parser.print_help()
        print("\nError: Input file required. Use -i <firmware.bin>", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Load firmware
    with open(args.input, "rb") as f:
        data = bytearray(f.read())

    # Detect device type
    device, version, is_valid = detect_device_type(bytes(data))
    print(f"Detected device: {device} ({version})")

    if args.device != "auto":
        device = "GP-50" if args.device == "gp50" else "GP-200"
        print(f"Using device override: {device}")

    if not is_valid and not args.force:
        print("Error: Could not validate firmware. Use --force to patch anyway.", file=sys.stderr)
        sys.exit(1)

    # Get regions
    patch_regions: list[tuple[int, int | None]]
    if args.region:
        try:
            start = int(args.region[0], 16) if args.region[0].startswith("0x") else int(args.region[0])
            end = int(args.region[1], 16) if args.region[1].startswith("0x") else int(args.region[1])
            patch_regions = [(start, end)]
        except ValueError:
            print("Error: Invalid region format", file=sys.stderr)
            sys.exit(1)
    else:
        patch_regions = get_string_regions(device)

    # Load translations
    translations_file: str | None = args.translations
    if not translations_file:
        # Try to find a default translations file
        default_files = [
            f"translations_{device.lower().replace('-', '')}.json",
            "translations.json",
        ]
        for fname in default_files:
            if os.path.exists(fname):
                translations_file = fname
                break

        if not translations_file:
            print("Error: No translations file specified. Use -t <translations.json>", file=sys.stderr)
            print("       Or run with --scan to generate a template.", file=sys.stderr)
            sys.exit(1)

    if not os.path.exists(translations_file):
        print(f"Error: Translations file not found: {translations_file}", file=sys.stderr)
        sys.exit(1)

    translations = load_translations(translations_file)
    print(f"Loaded {len(translations)} translations from {translations_file}")

    # Count non-placeholder translations
    actual_translations = sum(1 for v in translations.values() if v != "PLACEHOLDER")
    print(f"  ({actual_translations} actual translations, {len(translations) - actual_translations} placeholders)")

    # Patch the firmware
    print("\nPatching firmware...")
    patched, skipped, errors = patch_firmware(data, translations, patch_regions, verbose=args.verbose)

    print(f"\nPatched: {patched} strings")
    if skipped > 0:
        print(f"Skipped: {skipped} strings (too long)")

    if errors:
        print("\nErrors:")
        for err in errors[:10]:  # Show first 10 errors
            print(f"  {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

    # Update checksum for GP-200 firmware
    if device == "GP-200" and patched > 0:
        update_checksum(data, verbose=True)

    # Save patched firmware
    output_path = args.output
    if not output_path:
        base = Path(args.input).stem
        output_path = f"{base}-patched.bin"

    with open(output_path, "wb") as out_f:
        out_f.write(data)

    print(f"\nPatched firmware saved to: {output_path}")


if __name__ == "__main__":
    main()
