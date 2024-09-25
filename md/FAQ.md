# 配置和功能

1. ## 如何不显示形码的辅助码

   - flypy_flypy.schema.yaml中
   - ```
    translator:
       dictionary: flypy_flypy.extended
     enable_completion: false
     
     # 默认为不超过 2 个字的候选项显示输入码；将 2 改为 0 可关闭编码提示，
     # 改为 1 则是只显示单字的输入码，依此类推。
     spelling_hints: 2

   

2. ## 开启用, .翻页

   - 在default.yaml

   - ```
     key_binder:
       bindings:
         __patch:
           - key_bindings:/emacs_editing
           - key_bindings:/move_by_word_with_tab
           - key_bindings:/paging_with_minus_equal
     
           # 使用,和.来翻页
           # - key_bindings:/paging_with_comma_period
           
           - key_bindings:/numbered_mode_switch
     ```

3. ## 模糊音

   - ```
     这个功能类似飞键。
     以不分平翘舌音为例：
     在flypy_flypy.schema.yaml中，修改以下部分
     speller:
     algebra:
     ## 模糊音 可选择性开启
     - derive/^z([a-z])/v$1/
     - derive/^c([a-z])/i$1/
     - derive/^s([a-z])/u$1/
     - derive/^v([a-z])/z$1/
     - derive/^i([a-z])/c$1/
     - derive/^u([a-z])/s$1/
     
     添加韵母的话，和上面类似
     
     比如添加in和ing的模糊音，如果in是b，ing是k的话，可以这样：
     derive/^([a-z])b/$1k/ 派生/^（[a-z]）b/$1k/
     derive/^([a-z])k/$1b/
     ```

4. ## 数字大写

   1. 照搬了<https://github.com/iDvel/rime-ice>
      输入R开头即可
      [![image](https://private-user-images.githubusercontent.com/3831173/323869887-f4aedf70-2584-429d-98cf-25b7cf5ecc58.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTU1MzA4OTYsIm5iZiI6MTcxNTUzMDU5NiwicGF0aCI6Ii8zODMxMTczLzMyMzg2OTg4Ny1mNGFlZGY3MC0yNTg0LTQyOWQtOThjZi0yNWI3Y2Y1ZWNjNTgucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDUxMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA1MTJUMTYxNjM2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODZiMGMxZDBiMGY4OWFjODY4MGJkNDlmMWQ1YzE2OTkzOTU5NmU2NjYyZDQ4OGY0Yjg1OTc4ZDUyYTQwYjYyYiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.-TlzIy9alKUnTv4je8MdY1jk5aebtWzPp7zmy_duEWI)](https://private-user-images.githubusercontent.com/3831173/323869887-f4aedf70-2584-429d-98cf-25b7cf5ecc58.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTU1MzA4OTYsIm5iZiI6MTcxNTUzMDU5NiwicGF0aCI6Ii8zODMxMTczLzMyMzg2OTg4Ny1mNGFlZGY3MC0yNTg0LTQyOWQtOThjZi0yNWI3Y2Y1ZWNjNTgucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDUxMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA1MTJUMTYxNjM2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ODZiMGMxZDBiMGY4OWFjODY4MGJkNDlmMWQ1YzE2OTkzOTU5NmU2NjYyZDQ4OGY0Yjg1OTc4ZDUyYTQwYjYyYiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.-TlzIy9alKUnTv4je8MdY1jk5aebtWzPp7zmy_duEWI)

5. ## 自定义配置

   1. ```
      自定义配置建议放在 对应输入法的*.custom.yaml文件中,以patch开头即可，比如小鹤+鹤辅助码：flypy_flypy.custom.yaml 文件
      patch:
        #engine/translators/@last: '' ## 禁用英文单词输入功能
        #punctuator/half_shape: {} ## 恢复默认引号
        #menu/page_size: 5 ## 自定义候选项个数
      ```

6. ## 启用光标回退至特定音节后、补充辅助码的功能  [#5](https://github.com/gaboolic/rime-shuangpin-fuzhuma/issues/5)

   - ```
     文件：flypy_flypy.schema.yaml
     
     key_binder:
     import_preset: default
     bindings:
     #- { when: composing, accept: Tab, send: '[' } ## 取消注释后：tab引导辅助码
     - { when: composing, accept: Control+m, send: Return }
     - { when: composing, accept: Control+w, send: Control+BackSpace }
     - { when: has_menu, accept: semicolon, send: 2 }
     - { when: has_menu, accept: slash, send: 3 }
     - { when: composing, accept: Control+i, send: Shift+Right }
     - { when: composing, accept: Control+o, send: Shift+Left }
     ## 对以下4行取消注释后：启用光标回退至特定音节后、补充辅助码的功能
     ## （自然码等其他双拼用户请在 pinyin_switch.yaml 中设置）
     #- { when: composing, accept: Control+1, send_sequence: '{Home}{Shift+Right}[' }
     #- { when: composing, accept: Control+2, send_sequence: '{Home}{Shift+Right}{Shift+Right}[' }
     #- { when: composing, accept: Control+3, send_sequence: '{Home}{Shift+Right}{Shift+Right}{Shift+Right}[' }
     #- { when: composing, accept: Control+4, send_sequence: '{Home}{Shift+Right}{Shift+Right}{Shift+Right}{Shift+Right}[' }
     ```

7. ## 关于飞键 qu qv，ju jv

   1. 打开`# - derive/^([jqxy])u/$1v/`的注释，即可qu qv，ju jv互相飞键
   2. 再去掉custom_phrase.txt中的短语

8. ## 快符，o符，分号符

   1. o符快符使用可以参考：[https://flypy.cc/#/fh](https://flypy.cc/#/fh)   [#19](https://github.com/gaboolic/rime-shuangpin-fuzhuma/issues/19)   [#13](https://github.com/gaboolic/rime-shuangpin-fuzhuma/issues/13)
   2. 举例：
      希腊字母
      ofxx αβγ
      ofxd ΑΒΓ

9. ## 以词定字

   以词定字的功能关了，因为有辅助码了 就不太需要以词定字
   如果想打开 可以看[#15 (comment)](https://github.com/gaboolic/rime-shuangpin-fuzhuma/issues/15#issuecomment-2087710504)

10. ## 预输入框中显示双拼与全拼 来自 [ChaosAlphard](https://github.com/ChaosAlphard)

    详见[#18](https://github.com/gaboolic/rime-shuangpin-fuzhuma/pull/18)

    [image](https://private-user-images.githubusercontent.com/26186575/326491822-021f1e8f-cfae-4cd6-98fd-34834fd04653.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTUzMjYzNDksIm5iZiI6MTcxNTMyNjA0OSwicGF0aCI6Ii8yNjE4NjU3NS8zMjY0OTE4MjItMDIxZjFlOGYtY2ZhZS00Y2Q2LTk4ZmQtMzQ4MzRmZDA0NjUzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA1MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNTEwVDA3MjcyOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWUxYTg3Njg5MjcxNjRkNjMyY2Q2NWYzYmI4MTZjMDBiZTJhNWI1MzRjYmU2MTRiOWU1MDkwMTI2NzczODY4YzQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.WDEpgZZKVAs9-tWyDoe4v__UH-s9lvDxs6W-iAMb3Yc)

11. ## weasel.custom.yaml相关：横向显示、内嵌编码、自定义配色

    %appdata%目录下`\Roaming\Rime\weasel.custom.yaml`

    ```yaml
    # weasel.custom.yaml
    patch:
      style/horizontal: true      # 候選橫排
      style/inline_preedit: true  # 內嵌編碼（僅支持TSF）
      style/display_tray_icon: false  # 顯示托盤圖標
      style/corner_radius: 20 # 圆角
      style/font_face: "楷体"
      style/font_point: 18
      style/color_scheme: tf # 选择配色方案
      "preset_color_schemes/tf": # 自定义配色方案
        name: tf
        author: d
        text_color: 1710618
        back_color: 16382457
        border_color: 15658734
        label_color: 11184810
        hilited_text_color: 1710618
        hilited_back_color: 15790320
        candidate_text_color: 1710618
        comment_text_color: 1710618
        hilited_candidate_text_color: 1710618
        hilited_comment_text_color: 1710618
        hilited_candidate_back_color: 15790320
        hilited_label_color: 11184810
    ```

    

    在`patch:`下添加`"style/horizontal": true`后重新部署即可

12. ## 新对话框设置默认英文状态

    对应的方案文件下

    ```
    switches:
      - name: ascii_mode
        reset: 1               # 1为默认英文状态，0为默认中文状态
    ```

    

13. ...
