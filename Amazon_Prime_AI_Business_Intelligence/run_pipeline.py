import subprocess
import sys

def run_script(script_name):
    print(f"\nStarting: {script_name}")

    try:
        subprocess.run(
            [sys.executable, script_name],
            check=True
        )
        print(f"Completed: {script_name}")

    except subprocess.CalledProcessError:
        print(f"Error while running: {script_name}")
        sys.exit(1)


if __name__ == "__main__":

    print("=" * 50)
    print("AI BUSINESS INTELLIGENCE AUTOMATION")
    print("=" * 50)

    # Step 1: Generate AI insights
    run_script("src/ai_insights.py")

    # Step 2: Generate PDF report
    run_script("src/report_automation.py")

    print("\n" + "=" * 50)
    print("AUTOMATION COMPLETED SUCCESSFULLY!")
    print("Check your reports folder.")
    print("=" * 50)