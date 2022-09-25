import sys

# Helper functions

def render_nice_message(message, full_display_length=100):
    """
    Render a message that is more noticeable.
    """
    message_wrap_length = int((full_display_length - len(message) - 2) / 2)

    if len(message) % 2 != 0:
        full_display_length -= 1 # Message length is odd, so adjust full_display_length to accommodate.

    print(f"{'-' * full_display_length}")
    print(f"{'*' * message_wrap_length} {message.upper()} {'*' * message_wrap_length}")
    print(f"{'-' * full_display_length}\n")

    return None

def get_input(message):
    """
    Ask for input, and check for early quit.
    """
    input_value = input(message)

    if input_value.upper() == "Q":
        print("Game ended early after pressing 'Q'!")
        sys.exit(0)

    return input_value

