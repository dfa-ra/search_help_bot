class HelpService:
    def execute(self, commands):
        commands_str = ""

        for command in commands:
            commands_str += f"/{command[0]} - {command[1]}\n"

        return commands_str
