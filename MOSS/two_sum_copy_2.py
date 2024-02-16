
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Create a dictionary to store the indices of seen numbers
        num_indices = {}
        
        # Iterate through the list of numbers
        for i, num in enumerate(nums):
            # Calculate the complement needed to reach the target
            complement = target - num
            
            # Check if the complement is already in the dictionary
            if complement in num_indices:
                # Return the indices of the two numbers
                return [num_indices[complement], i]
            
            # If complement is not in the dictionary, store the current number's index
            num_indices[num] = i
        
        # If no solution is found, return an empty list or handle it as needed
        return []
