class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        nmap = {}
        length = len(nums)

        for j in range(length):
            comp = target - nums[j]
            if comp in nmap:
                return [nmap[comp], j]
            nmap[nums[i]] = j

        return []  # No solution found