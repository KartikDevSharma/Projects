import re
import ast
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodePreprocessor:
    def __init__(self):
        pass

    def preprocess(self, code: str, language: str) -> str:
        """
        Preprocess the code based on the programming language.
        Currently supports Python. Add more languages as needed.
        """
        if language.lower() in ['python', 'python3']:
            return self.preprocess_python(code)
        else:
            logger.warning(f"Unsupported language: {language}. Returning original code.")
            return code

    def preprocess_python(self, code: str) -> str:
        """
        Preprocess Python code:
        1. Remove comments
        2. Remove empty lines
        3. Standardize variable names
        4. Remove whitespace
        """
        # Remove comments
        code = self.remove_comments_python(code)
        
        # Remove empty lines
        code = "\n".join([line for line in code.split("\n") if line.strip()])
        
        # Standardize variable names
        code = self.standardize_variables_python(code)
        
        # Remove whitespace
        code = self.remove_whitespace(code)
        
        return code

    def remove_comments_python(self, code: str) -> str:
        """Remove single-line and multi-line comments from Python code."""
        # Remove single-line comments
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments
        code = re.sub(r'"""[\s\S]*?"""', '', code)
        code = re.sub(r"'''[\s\S]*?'''", '', code)
        
        return code

    def standardize_variables_python(self, code: str) -> str:
        """Rename all variables to a standard format (var1, var2, etc.)"""
        try:
            tree = ast.parse(code)
            variable_map = {}
            var_counter = 1

            class VariableRenamer(ast.NodeTransformer):
                def visit_Name(self, node):
                    if isinstance(node.ctx, ast.Store):
                        if node.id not in variable_map:
                            variable_map[node.id] = f'var{var_counter}'
                            nonlocal var_counter
                            var_counter += 1
                    node.id = variable_map.get(node.id, node.id)
                    return node

            VariableRenamer().visit(tree)
            return ast.unparse(tree)
        except SyntaxError:
            logger.warning("Failed to parse Python code. Returning original code.")
            return code

    def remove_whitespace(self, code: str) -> str:
        """Remove all unnecessary whitespace."""
        # Remove leading and trailing whitespace from each line
        code = "\n".join([line.strip() for line in code.split("\n")])
        
        # Remove multiple spaces
        code = re.sub(r'\s+', ' ', code)
        
        return code

if __name__ == "__main__":
    preprocessor = CodePreprocessor()
    
    # Test Python preprocessing
    python_code = """
    # This is a comment
    def solution(nums):
        \"\"\"This is a docstring\"\"\"
        result = 0
        for num in nums:
            result += num  # Compute sum
        return result
    """
    
    
    preprocessed_code = preprocessor.preprocess(python_code, 'python')
    logger.info(f"Original code:\n{python_code}")
    logger.info(f"Preprocessed code:\n{preprocessed_code}")
