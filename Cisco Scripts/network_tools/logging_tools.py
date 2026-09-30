from datetime import datetime
from pathlib import Path
from csv import DictWriter
from datetime import datetime
from pathlib import Path


def write_results_log(
    results,
    script_name,
    site=None
):
    """Write script execution results to a timestamped log file."""
    project_root = Path(__file__).resolve().parent.parent

    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = log_dir / f"{script_name}_{timestamp}.log"

    successful = [
        result for result in results
        if result.get("status") == "success"
    ]

    skipped = [
        result for result in results
        if result.get('status') == "skipped"
    ]

    failed = [
        result for result in results
        if result.get("status") == "failed"
    ]

    with open(log_file, "w") as file:
        file.write("=" * 60 + "\n")
        file.write(f"Script: {script_name}\n")
        file.write(
            f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        if site:
            file.write(f"Site Filter: {site}\n")

        file.write(f"Devices Processed: {len(results)}\n")
        file.write(f"Successful: {len(successful)}\n")
        file.write(f"Skipped: {len(skipped)}\n")
        file.write(f"Failed: {len(failed)}\n")
        file.write("=" * 60 + "\n\n")

        for heading, group in (
            ("Successful", successful),
            ("Skipped", skipped),
            ("Failed", failed),
        ):
            file.write(f"{heading}\n")
            file.write("=" * 60 + "\n")

            for result in group:
                hostname = result.get("hostname", "Unknown")
                ip = result.get("ip", "Unknown")
                reason = result.get("reason", "")

                file.write(f"{hostname} - {ip}")

                if reason:
                    file.write(f" - {reason}")

                file.write("\n")

            file.write("\n")

    return log_file

def write_results_csv(results, script_name):
    """Write script execution results to a timestamped CSV log."""

    project_root = Path(__file__).resolve().parent.parent

    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    run_time = datetime.now()
    timestamp = run_time.strftime("%Y-%m-%d_%H-%M-%S")

    log_file = log_dir / f"{script_name}_{timestamp}.csv"

    fieldnames = [
        "timestamp",
        "script",
        "site",
        "hostname",
        "ip",
        "status",
        "reason",
        "acl_name",
    ]

    with open(
        log_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        for result in results:
            row = {
                "timestamp": run_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "script": script_name,
                "site": result.get("site", ""),
                "hostname": result.get("hostname", ""),
                "ip": result.get("ip", ""),
                "status": result.get("status", ""),
                "reason": result.get("reason", ""),
                "acl_name": result.get("acl_name", ""),
            }

            writer.writerow(row)

    return log_file