- ```
  # 第一步，修改分号为始码按键并且不让其自动上屏 下面以小鹤双拼+辅助码举例：打开文件 flypy_flypy.schea.yaml，添加;号
  
  speller:
    # 如果不想让什么标点直接上屏，可以加在 alphabet，或者编辑标点符号为两个及以上的映射
    alphabet: ;zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA[
    # initials 定义仅作为始码的按键，排除 ` 让单个的 ` 可以直接上屏
    initials: ;zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA
    # 第一位<空格>是拼音之间的分隔符；第二位<'>表示可以手动输入单引号来分割拼音。
  
  # 第二步，添加置顶词 custom_phrase_xhkf.txt
  
  https://flypy.com xhgw
  😊 oi
  
  # 快符
  ：“ ;q
  ？ ;w
  （ ;e
  ） ;r
  @ ;t
  · ;y
  + ;u
  - ;i
  [ ;o
  ] ;p
  ！ ;a
  …… ;s
  、 ;d
  《 ;g
  * ;h
  / ;j
  ( ;k
  ) ;l
  “ ;z
  → ;x
  ” ;c
  —— ;v
  》 ;b
  < ;n
  > ;m
  
  #符号
  ！ oa
  % ob
  一 oba 111
  ```