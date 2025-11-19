"""
Shared utility functions for the engg.pk application.

This module contains common functionality used across multiple apps.
"""

from typing import TypeVar, Generic
from django.db import models
from django.contrib.auth.models import User

# Type variable for model instances
ModelType = TypeVar('ModelType', bound=models.Model)


def toggle_like(obj: ModelType, user: User) -> tuple[bool, int]:
    """
    Toggle a user's like on any model that has a 'likes' ManyToManyField.

    This utility function eliminates duplicated like-toggle logic across
    feed posts, comments, forum posts, and replies.

    Args:
        obj: The model instance (FeedPost, Comment, ForumPost, Reply, etc.)
        user: The user toggling the like

    Returns:
        tuple[bool, int]: A tuple of (is_liked, like_count)
            - is_liked: True if user liked the object, False if unliked
            - like_count: The current total number of likes

    Raises:
        AttributeError: If obj doesn't have a 'likes' attribute

    Example:
        >>> post = FeedPost.objects.get(pk=1)
        >>> user = request.user
        >>> is_liked, count = toggle_like(post, user)
        >>> print(f"Liked: {is_liked}, Total likes: {count}")
    """
    if not hasattr(obj, 'likes'):
        raise AttributeError(f"{obj.__class__.__name__} doesn't have a 'likes' attribute")

    # Use exists() for better performance
    if obj.likes.filter(id=user.id).exists():
        obj.likes.remove(user)
        is_liked = False
    else:
        obj.likes.add(user)
        is_liked = True

    # Get the current like count
    like_count = obj.likes.count()

    return is_liked, like_count


def validate_text_length(
    text: str,
    field_name: str = "Text",
    max_length: int = 5000,
    min_length: int = 1
) -> tuple[bool, str]:
    """
    Validate text input for length constraints.

    Args:
        text: The text to validate
        field_name: Name of the field for error messages (default: "Text")
        max_length: Maximum allowed length (default: 5000)
        min_length: Minimum allowed length (default: 1)

    Returns:
        tuple[bool, str]: A tuple of (is_valid, error_message)
            - is_valid: True if validation passed, False otherwise
            - error_message: Error message if validation failed, empty string otherwise

    Example:
        >>> is_valid, error = validate_text_length(comment, "Comment", 5000)
        >>> if not is_valid:
        ...     return HttpResponse(error, status=400)
    """
    text = text.strip()

    if len(text) < min_length:
        return False, f'<p class="text-red-500">{field_name} cannot be empty</p>'

    if len(text) > max_length:
        return False, f'<p class="text-red-500">{field_name} too long (max {max_length} characters)</p>'

    return True, ""


def parse_comma_separated_list(value: str, max_items: int = 20) -> list[str]:
    """
    Parse a comma-separated string into a list of stripped values.

    This utility eliminates duplicated parsing logic across forms.

    Args:
        value: The comma-separated string to parse
        max_items: Maximum number of items allowed (default: 20)

    Returns:
        list[str]: List of stripped non-empty values

    Example:
        >>> topics = parse_comma_separated_list("software, civil , electrical")
        >>> print(topics)
        ['software', 'civil', 'electrical']
    """
    if not value:
        return []

    items = [item.strip() for item in value.split(',') if item.strip()]
    return items[:max_items]  # Limit to max_items
