#!/usr/bin/env python3
"""
Monitor ID Tagging Script for {{CLIENT_NAME}}

This script adds 'id:<monitor_id>' tags to all Datadog monitors
that don't already have them. This makes monitors easier to find
and reference in the Datadog UI.

Usage:
    ./caller.py append     # Add id tags to all monitors missing them
    ./caller.py list       # List all monitors
    ./caller.py check      # Show monitors without id tags

Environment Variables Required:
    TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_api_key  (or DD_API_KEY)
    TF_VAR_{{CLIENT_NAME_UNDERSCORE}}_app_key  (or DD_APP_KEY)

Run after terraform apply to ensure all monitors are tagged.
"""
import sys
import monitors


def print_usage():
    print(__doc__)
    print("Commands:")
    print("  append  - Add id tags to monitors that don't have them")
    print("  list    - List all monitors with their tags")
    print("  check   - Show monitors without id tags (dry run)")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "append":
        print("Adding id tags to monitors...")
        stats = monitors.append_id_tag_to_tags()
        print(f"\nResults:")
        print(f"  Tagged:  {stats['tagged']}")
        print(f"  Skipped: {stats['skipped']} (already had id tag)")
        print(f"  Failed:  {stats['failed']}")

    elif command == "list":
        monitors.list_monitors()

    elif command == "check":
        missing = monitors.list_monitors_without_id_tag()
        print(f"Monitors without id tag: {len(missing)}")
        for m in missing:
            print(f"  {m['id']}: {m['name']}")

    elif command in ["-h", "--help", "help"]:
        print_usage()

    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
