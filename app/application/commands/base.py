import shlex
import logging
from typing import TypeVar, Generic, Dict, Any
from pydantic import BaseModel, ValidationError
from app.application.commands.contract import ICommand

logger = logging.getLogger(__name__)

# We bind ArgsSchema to BaseModel here because this specific BaseCommand 
# relies on Pydantic's validation and introspection features.
ArgsSchema = TypeVar("ArgsSchema", bound=BaseModel)

class BaseCommand(ICommand[ArgsSchema], Generic[ArgsSchema]):
    """
    Base implementation with built-in argument parsing and validation.
    
    It uses 'shlex' to handle quoted strings correctly (e.g., name="Hitagi Senjougahara")
    and Pydantic to validate data types and constraints.
    """
    
    def parse_payload(self, raw_payload: str) -> ArgsSchema:
        try:
            # 1. Handle empty payload
            if not raw_payload.strip():
                # Attempt to create the model with defaults.
                # If fields are required, Pydantic will raise a ValidationError here.
                return self.args_schema()

            # 2. Tokenize the input string (handling quotes)
            try:
                tokens = shlex.split(raw_payload)
            except ValueError:
                # Fallback for unbalanced quotes
                tokens = raw_payload.split()

            parsed_kwargs: Dict[str, Any] = {}
            unnamed_args = []

            for token in tokens:
                if "=" in token:
                    # Format: key=value
                    key, value = token.split("=", 1)
                    parsed_kwargs[key] = value
                else:
                    unnamed_args.append(token)

            # 3. Handle positional arguments (Fallback logic)
            # If the user provided inputs without keys (e.g., "/remember buy milk"),
            # we assign the entire payload to the first field of the schema.
            if unnamed_args and not parsed_kwargs:
                # Introspection: get the name of the first field defined in the Pydantic model
                first_field_name = next(iter(self.args_schema.model_fields.keys()))
                parsed_kwargs[first_field_name] = raw_payload.strip()

            # 4. Create and validate the Pydantic model
            return self.args_schema(**parsed_kwargs)

        except ValidationError as e:
            # Transform Pydantic errors into a human-readable format
            error_messages = []
            for err in e.errors():
                field_name = err['loc'][0]
                message = err['msg']
                # Simplify common error messages if needed
                if "valid number" in message:
                    message = "must be a number"
                
                error_messages.append(f"Error in parameter '{field_name}': {message}")
            
            raise ValueError("\n".join(error_messages))

        except Exception as e:
            raise ValueError(f"Failed to parse command arguments: {str(e)}")