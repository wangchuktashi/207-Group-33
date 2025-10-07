
class Comment:
    def __init__(self, user, text, created_at):
        self.user = user
        self.text = text
        self.created_at = created_at

    def __repr__(self):
        return f"User {self.user} · {self.created_at}\n{self.text}"


class Event:
    def __init__(
        self, id, title, sport, venue, start_text, end_text,
        image, hero_image, description, status
    ):
        self.id = id
        self.title = title
        self.sport = sport
        self.venue = venue
        self.start_text = start_text   # e.g. "Sat, Oct 18 • 7:30 PM"
        self.end_text = end_text       # e.g. "9:30 PM"
        self.image = image             # small/card image (in static/img/)
        self.hero_image = hero_image   # big banner image (in static/img/)
        self.description = description
        self.status = status           # "Open" | "Sold Out" | "Cancelled" | "Inactive"
        self.comments = []

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    # Convenience for Bootstrap badge colour in your cards
    @property
    def badge(self):
        return {
            "Open": "success",
            "Sold Out": "dark",
            "Cancelled": "danger",
            "Inactive": "secondary",
        }.get(self.status, "secondary")

    def __repr__(self):
        return f"<Event {self.id} {self.title}>"