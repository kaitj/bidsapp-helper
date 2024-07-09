"""Custom types used for parser."""


def participant_label(participants: str | None) -> str | list[str] | None:
    """Split arguments and strip 'sub-' if necessary."""
    if not participants:
        return None

    out_args = participants.split()
    out_args = [participant.lstrip("sub-").rstrip(",") for participant in out_args]

    if len(out_args) == 1:
        return out_args[-1]
    return out_args
