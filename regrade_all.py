"""
Regrade all submissions for a Gradescope assignment.
Mimics the "Regrade All Submissions" button on the submissions page.
"""

from typing import Union

from rich.console import Console

from api.client import GradescopeAPI

CONSOLE = Console(highlight=False)


def main(
    course_id: Union[str, int],
    assignment_id: Union[str, int],
    cookie_file="cookies.json",
    dry_run=False,
):
    api = GradescopeAPI(cookie_file=cookie_file)

    _, csrf_data = api.fetch_submission_page_data(course_id, assignment_id)
    _, csrf_token = csrf_data

    if dry_run:
        CONSOLE.print(
            f"[green]DRY RUN:[/green] Would regrade all submissions for "
            f"course [blue]{course_id}[/blue], assignment [blue]{assignment_id}[/blue]"
        )
        return

    CONSOLE.print(
        f"Regrading all submissions for "
        f"course [blue]{course_id}[/blue], assignment [blue]{assignment_id}[/blue]..."
    )
    api.regrade_all_submissions(course_id, assignment_id, csrf_token)
    CONSOLE.print("[green]Regrade request sent successfully.[/green]")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Regrade all submissions for a Gradescope assignment."
    )

    parser.add_argument("course_id", type=int, help="Gradescope course id")
    parser.add_argument("assignment_id", type=int, help="Gradescope assignment id")

    parser.add_argument(
        "--cookies", default="cookies.json", help="Filename for the cookie cache"
    )

    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry run; does not submit the regrade request",
    )

    args = parser.parse_args()
    main(
        course_id=args.course_id,
        assignment_id=args.assignment_id,
        cookie_file=args.cookies,
        dry_run=args.dry_run,
    )
