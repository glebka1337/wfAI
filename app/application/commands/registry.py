from typing import Union
from app.application.commands.contract import ICommand
import logging

logger = logging.getLogger(__name__)

class CommandRegistry:
    
    def __init__(self, commands: list[ICommand]) -> None:
        self._cmd_map = {
            cmd.name: cmd
            for cmd in commands
        }
        
        logger.info(f'Command map was created: {list(self._cmd_map.keys())}')
    
    def get_commands(self) -> list[ICommand]:
        return list(self._cmd_map.values())
    
    async def process_input(
        self,
        query: str,
        session_id: str
    ) -> Union[str, None]: 
        
        if not query.startswith('/'):
            return None
        
        parts = query.split(' ', 1) # ['/cmdname', 'arg1=val1 arg2=val2' ...]
        cmd_name = parts[0].replace('/', '').lower()
        args = parts[1] if len(parts) > 1 else '' # meaning command without arguments
        
        cmd = self._cmd_map.get(cmd_name)
        if not cmd: return f'Command {cmd_name} was not found'
        
        try:
            args_schema = cmd.parse_payload(args)
            return await cmd.execute(args=args_schema, session_id=session_id)
            
        except ValueError as ve:
            return f'Arguments error: {ve}'
        except Exception as e:
            return f'Unexpected error occured: {e}'