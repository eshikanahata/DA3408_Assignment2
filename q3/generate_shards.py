import csv
import random

NUM_SHARDS = 8
ROWS_PER_SHARD = 40

COUNTRIES = ["US", "IN", "UK", "DE", "BR", "AU"]
DOMAINS = ["example.com", "mail.com", "test.org"]


def make_valid_email(i, domain):
    return f"user{i}@{domain}"


def make_invalid_email(i, kind):
    if kind == "no_at":
        return f"user{i}example.com"
    if kind == "no_domain":
        return f"user{i}@"
    if kind == "double_at":
        return f"user{i}@@example.com"
    return "" 


def generate_shard(shard_index: int):
    rng = random.Random(1000 + shard_index)
    rows = []
    num_invalid = 3 + (shard_index % 5)

    invalid_positions = set(rng.sample(range(ROWS_PER_SHARD), num_invalid))

    for row_num in range(ROWS_PER_SHARD):
        user_id = f"shard{shard_index}-user{row_num}"
        signup_date = f"2026-0{1 + (row_num % 9)}-15"
        country = rng.choice(COUNTRIES)

        if row_num in invalid_positions:
            fault = rng.choice(["bad_email", "missing_email", "missing_user_id"])
            if fault == "bad_email":
                kind = rng.choice(["no_at", "no_domain", "double_at"])
                email = make_invalid_email(row_num, kind)
            elif fault == "missing_email":
                email = ""
            else:
                user_id = ""
                email = make_valid_email(row_num, rng.choice(DOMAINS))
        else:
            email = make_valid_email(row_num, rng.choice(DOMAINS))

        rows.append([user_id, email, signup_date, country])

    return rows, num_invalid


def main():
    summary = {}
    for shard_index in range(NUM_SHARDS):
        rows, num_invalid = generate_shard(shard_index)
        filename = f"shard_{shard_index}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "email", "signup_date", "country"])
            writer.writerows(rows)
        summary[shard_index] = num_invalid
        print(f"Wrote {filename}: {ROWS_PER_SHARD} rows, {num_invalid} seeded invalid rows")

    print("\nGround-truth summary (for cross-checking pod output):")
    for idx, count in summary.items():
        print(f"  shard_{idx}.csv -> {count} invalid rows")
    print(f"  TOTAL invalid rows across all shards: {sum(summary.values())}")


if __name__ == "__main__":
    main()
