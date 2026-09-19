import csv
import os
import re
import sys

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
REQUIRED_FIELDS = ["user_id", "email", "signup_date"]


def is_row_invalid(row: dict) -> bool:
    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            return True
    if not EMAIL_RE.match(row["email"]):
        return True
    return False


def main():
    completion_index = os.environ.get("JOB_COMPLETION_INDEX")
    node_name = os.environ.get("NODE_NAME", "unknown-node")
    pod_name = os.environ.get("POD_NAME", "unknown-pod")

    if completion_index is None:
        print("ERROR: JOB_COMPLETION_INDEX not set - is this running as an Indexed Job?", file=sys.stderr)
        sys.exit(1)

    shard_path = f"/shards/shard_{completion_index}.csv"
    if not os.path.exists(shard_path):
        print(f"ERROR: shard file {shard_path} not found", file=sys.stderr)
        sys.exit(1)

    total_rows = 0
    invalid_rows = 0
    with open(shard_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if is_row_invalid(row):
                invalid_rows += 1

    print(
        f"RESULT shard_index={completion_index} pod={pod_name} node={node_name} "
        f"total_rows={total_rows} invalid_rows={invalid_rows}"
    )


if __name__ == "__main__":
    main()
