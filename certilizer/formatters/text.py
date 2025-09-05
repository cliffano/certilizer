"""A module for formatting data frames as text."""

from tabulate import tabulate


def format_report(data_frame) -> str:
    """Return the text representation of the data frame table."""
    return tabulate(data_frame, showindex=False, headers="keys", tablefmt="simple_grid")
