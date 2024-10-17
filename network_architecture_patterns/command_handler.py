# command_handler.py
class CommandHandler:
    def __init__(self, connection):
        self.connection = connection
        self.user_authenticated = False

    def handle(self, request):
        request = request.strip()
        print(f"Handling command: {request}")  # Debug line

        if request.startswith("USER"):
            username = request.split()[1] if len(request.split()) > 1 else ""
            return f"331 User {username} okay, need password."
        elif request.startswith("PASS"):
            if not self.user_authenticated:
                self.user_authenticated = True  # Simulate successful authentication
                return "230 User logged in, proceed."
            else:
                return "503 Already logged in."
        elif request == "QUIT":
            return "221 Goodbye."
        else:
            return "502 Command not implemented."

