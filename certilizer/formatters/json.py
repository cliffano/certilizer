"""A module for formatting data frames as JSON string."""


def format_report(data_frame) -> str:
    """Return the JSON representation of the data frame."""
    return data_frame.to_json(orient="records", indent=2)
