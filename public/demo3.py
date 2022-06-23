# str='abcabcbb'
# same=''
# diff=''
# for i in range(len(str)):
#     if str.count(str[i]) > 1:
#         same+=str[i]
#     else:
#         diff+=str[i]
# # print('重复的元素有：%s'%same)
# # print('不重复的元素有：%s'%diff)
#
# class Solution:
#    def solve(self, s):
#       def dp(i, j):
#          if i >= j:
#             return 0
#          if s[i] == s[j]:
#             return dp(i + 1, j - 1)
#          else:
#             return min(dp(i + 1, j), dp(i, j - 1)) + 1
#       return dp(0, len(s) - 1)
# ob = Solution()
# s = "google"
#print('需要删减的最少字符个数=',ob.solve(s))
#
# def lengthOfLongestSubstring(s):
#     d = {}
#     start = 0
#     ans = 0
#     for i, c in enumerate(s):  # 取字符串中第i个字符为c
#         if c in d:  # 如果c在字典里
#             start = max(start, d[c] + 1)  # 将开始位置重新定位
#         d[c] = i  # 记录 c 在字符串的最新位置
#         ans = max(ans, i - start + 1)  # 记录最大不重复值
#     return ans
#
#
# n = lengthOfLongestSubstring('abcabcbb')
# print("不重复最长字符串长度=",n)
# def func(n):
#     if n == 0:
#         return 1
#     else:
#         return n * func(n-1)
#
# print(func(5))
x1=[1,2,3]
x2=[2,3]
x3=[3,4]
print(list(set(x1+x2+x3)))
