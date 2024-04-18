
def generate_numbers(nums):
    result = []
    for num in nums:
        # 進行一些演算，這裡以乘以3並減去2作為示例
        new_num = num * 3 - 2
        # 確保結果小於或等於39
        if new_num <= 39:
            result.append(new_num)
        # 如果已經得到六個結果，就停止迭代
        if len(result) == 6:
            break
    return result

# 給定的數字
input_numbers = [3, 5, 15, 24, 9, 13, 33, 21, 29, 24]

# 產生六個小於或等於39的號碼
output_numbers = generate_numbers(input_numbers)

# 輸出結果
print(output_numbers)
