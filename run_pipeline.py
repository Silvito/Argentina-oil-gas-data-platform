
import subprocess
import sys

STAGES = [
    ("Silver - PySpark", "src/transformation/silver_spark.py"),
    ("Gold - PySpark", "src/transformation/gold_spark.py"),
]


def main():
    for stage_name, script_path in STAGES:
        print(f"\n{'=' * 60}", flush=True)
        print(f"Ejecutando etapa: {stage_name}", flush=True)
        print(f"{'=' * 60}", flush=True)

        result = subprocess.run(
            [sys.executable, script_path],
            check=False,
        )

        if result.returncode != 0:
            print(
                f"ERROR: falló la etapa {stage_name} "
                f"(código {result.returncode}).",
                flush=True,
            )
            sys.exit(result.returncode)

    print("\nPipeline Silver → Gold completado.", flush=True)


if __name__ == "__main__":
    main()
