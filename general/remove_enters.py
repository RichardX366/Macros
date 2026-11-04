from time import sleep

from AppKit import NSPasteboard  # type: ignore

while True:
    pasteboard = NSPasteboard.generalPasteboard()

    text = pasteboard.stringForType_("public.utf8-plain-text")

    if text is not None:
        # Remove Enter/newline characters
        text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")

        pasteboard.clearContents()
        pasteboard.setString_forType_(text, "public.utf8-plain-text")
    sleep(1)
