from typing import Union, List, Dict
import math
from enum import Enum, auto

class BaseConversionError(Exception):
    """Custom exception for base conversion errors."""
    pass

class ConversionMode(Enum):
    """Enumeration of conversion modes for cognitive flexibility."""
    STANDARD = auto()
    EDUCATIONAL = auto()
    PERFORMANCE = auto()

class CognitiveBaseConverter:
    """
    Advanced base conversion engine with cognitive transformation capabilities.
    
    Implements a multi-dimensional approach to number system conversions,
    tracking cognitive complexity and providing educational insights.
    """
    
    def __init__(
        self, 
        mode: ConversionMode = ConversionMode.STANDARD,
        max_bit_width: int = 64
    ):
        """
        Initialize the conversion engine with cognitive tracking.
        
        Args:
            mode (ConversionMode): Conversion operational mode
            max_bit_width (int): Maximum bit width for conversions
        """
        self.mode = mode
        self.max_bit_width = max_bit_width
        self.conversion_history: List[Dict] = []
    
    def convert(
        self, 
        value: Union[int, float], 
        source_base: int, 
        target_base: int
    ) -> Dict:
        """
        Advanced base conversion with cognitive complexity tracking.
        
        Args:
            value (Union[int, float]): Value to convert
            source_base (int): Source base (2-36)
            target_base (int): Target base (2-36)
        
        Returns:
            Dict containing conversion details and cognitive insights
        """
        # Validate input bases
        self._validate_bases(source_base, target_base)
        
        # Convert to decimal (intermediate representation)
        decimal_value = self._to_decimal(value, source_base)
        
        # Convert from decimal to target base
        target_representation = self._from_decimal(decimal_value, target_base)
        
        # Generate cognitive conversion metadata
        conversion_metadata = {
            "source_value": value,
            "source_base": source_base,
            "target_base": target_base,
            "decimal_intermediate": decimal_value,
            "target_representation": target_representation,
            "cognitive_complexity": self._calculate_complexity(
                source_base, 
                target_base, 
                decimal_value
            )
        }
        
        # Track conversion history if in educational mode
        if self.mode in [ConversionMode.EDUCATIONAL, ConversionMode.STANDARD]:
            self.conversion_history.append(conversion_metadata)
        
        return conversion_metadata
    
    def _validate_bases(self, source_base: int, target_base: int) -> None:
        """
        Validate base input constraints.
        
        Args:
            source_base (int): Source base to validate
            target_base (int): Target base to validate
        
        Raises:
            BaseConversionError: For invalid base inputs
        """
        valid_bases = range(2, 37)  # Standard base range
        if source_base not in valid_bases or target_base not in valid_bases:
            raise BaseConversionError(
                f"Bases must be between 2 and 36. "
                f"Received: source_base={source_base}, target_base={target_base}"
            )
    
    def _to_decimal(self, value: Union[int, float], source_base: int) -> float:
        """
        Convert value from source base to decimal.
        
        Args:
            value (Union[int, float]): Value to convert
            source_base (int): Source base
        
        Returns:
            float: Decimal representation
        """
        # Handle integer and fractional parts separately
        str_value = str(value)
        
        # Split integer and fractional parts
        parts = str_value.split('.')
        integer_part = parts[0]
        fractional_part = parts[1] if len(parts) > 1 else ''
        
        # Convert integer part
        integer_decimal = sum(
            int(digit, source_base) * (source_base ** power)
            for power, digit in enumerate(reversed(integer_part))
        )
        
        # Convert fractional part
        fractional_decimal = sum(
            int(digit, source_base) * (source_base ** -(power + 1))
            for power, digit in enumerate(fractional_part)
        ) if fractional_part else 0.0
        
        return integer_decimal + fractional_decimal
    
    def _from_decimal(self, value: float, target_base: int) -> str:
        """
        Convert decimal value to target base representation.
        
        Args:
            value (float): Decimal value to convert
            target_base (int): Target base
        
        Returns:
            str: Representation in target base
        """
        # Separate integer and fractional parts
        integer_part = int(value)
        fractional_part = value - integer_part
        
        # Convert integer part
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        integer_conversion = []
        
        while integer_part > 0:
            integer_conversion.insert(0, digits[integer_part % target_base])
            integer_part //= target_base
        
        # Convert fractional part
        fractional_conversion = []
        precision = 10  # Number of fractional digits
        
        while fractional_part > 0 and len(fractional_conversion) < precision:
            fractional_part *= target_base
            digit = int(fractional_part)
            fractional_conversion.append(digits[digit])
            fractional_part -= digit
        
        # Combine parts
        result = ''.join(integer_conversion or ['0'])
        if fractional_conversion:
            result += '.' + ''.join(fractional_conversion)
        
        return result
    
    def _calculate_complexity(
        self, 
        source_base: int, 
        target_base: int, 
        value: float
    ) -> float:
        """
        Calculate cognitive complexity of the conversion.
        
        Args:
            source_base (int): Source base
            target_base (int): Target base
            value (float): Value being converted
        
        Returns:
            float: Cognitive complexity score
        """
        base_difference = abs(source_base - target_base)
        value_magnitude = abs(value)
        
        # Complexity is a function of base difference and value magnitude
        complexity = (
            base_difference * 
            (1 + math.log(value_magnitude + 1)) / 
            math.log(max(source_base, target_base))
        )
        
        return min(complexity, 10.0)  # Cap complexity at 10
    
    def get_conversion_history(self) -> List[Dict]:
        """
        Retrieve conversion history for analysis.
        
        Returns:
            List[Dict]: Historical conversion metadata
        """
        return self.conversion_history
    
    def reset_conversion_history(self) -> None:
        """Reset conversion history tracking."""
        self.conversion_history = []
