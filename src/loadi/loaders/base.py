import pynapple as nap
from typing import TypedDict

class PositionDict(TypedDict):
    Px: nap.Tsd
    Py: nap.Tsd

class BaseExperiment:

    def __init__(self, experiment_structure):
        self.data_paths = experiment_structure
        self.session_class = BaseSession
        self.containing_folder = None

    def __repr__(self):
        return self._generate_terminal_tree(self.data_paths)

    def _repr_html_(self):
        return self._generate_html(self.data_paths)

    def _generate_terminal_tree(self, data, indent=""):
        lines = []
        items = list(data.items())
        
        for i, (key, value) in enumerate(items):
            # Determine if this is the last item in the current nesting level
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "
            
            if isinstance(value, dict):
                # Header for a nested section
                lines.append(f"{indent}{connector}\033[1m{key}\033[0m")
                
                # Create the prefix for the next level
                next_indent = indent + ("    " if is_last else "│   ")
                lines.append(self._generate_terminal_tree(value, next_indent))
            else:
                # Leaf node
                lines.append(f"{indent}{connector}\033[1m{key}\033[0m: loadable data: {value}")
                
        return "\n".join(lines)

    def _generate_html(self, data):
        html = "<div style='font-family: monospace; margin-left: 20px;'>"
        
        for key, value in data.items():
            if isinstance(value, dict):
                # If the value is a dict, we nest another details tag
                html += f"""
                <details style="margin-bottom: 5px;">
                    <summary style="cursor: pointer; font-weight: bold;">
                        {key}
                    </summary>
                    {self._generate_html(value)}
                </details>
                """
            else:
                # If it's a leaf node, just show the key-value pair
                html += f"<p><strong>{key}</strong>, loadable data: {value}</p>"
        
        html += "</div>"
        return html
    
    def get_session():
        pass
        
    def __iter__(self):
        # We delegate the iteration to our recursive helper
        return self._walk(self.data_paths, [])

    def _walk(self, current_node, path):
        if isinstance(current_node, list) or isinstance(current_node, str):
            yield self.get_session(*path)
        elif isinstance(current_node, dict):
            for key, value in current_node.items():
                yield from self._walk(value, path + [key])

class BaseSession():

    def load_units(self) -> nap.TsGroup:
        pass
