- ```
  # 修改字母表加入分号，有两处alphabet和initials。 下面以小鹤双拼+辅助码举例：打开文件 flypy_flypy.schea.yaml，添加;号
  
  speller:
    # 如果不想让什么标点直接上屏，可以加在 alphabet，或者编辑标点符号为两个及以上的映射
    alphabet: ;zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA[
    initials: ;zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA
    # 第一位<空格>是拼音之间的分隔符；第二位<'>表示可以手动输入单引号来分割拼音。
  