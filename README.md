# 说明

- [此仓库](https://github.com/gaboolic/rime-shuangpin-fuzhuma)为rime配置文件,词库使用最强简体词库——[雾凇拼音](https://github.com/iDvel/rime-ice)，在雾凇拼音的基础上实现自然码双拼、小鹤双拼，以及对应的辅助码。本人用的是这个方案，所以更新有保证
- 配置文件参考[小鹤双拼+自然快手/小鹤双形辅助码](https://github.com/functoreality/rime-flypy-zrmfast)
- [魔改自然碼 Rime 方案 (自然碼雙拼+輔助碼+外語混輸+簡繁方案+emoji)](https://github.com/ksqsf/rime-moran)
- 主要配置文件:
  - `flypy_flypy.schema.yaml # 小鹤双拼+鹤形辅助码`
  - `zrm_zrm.schema.yaml # 自然码双拼+自然码辅助码`
- 词库文件分别为`flypy_flypy.extended.dict.yaml`和`zrm_zrm.extended.dict.yaml`，默认只开启了我用[雾凇词库](https://github.com/iDvel/rime-ice)转换的词典文件。此外还有从其他地方获取的细胞词库，例如历史类、地名类、古诗文、计算机、动漫、电影、游戏、电商等，可自行打开注释或从[细胞词库](https://github.com/Bambooin/rimerc/tree/master/luna_pinyin)获取。如无特殊需求，词典文件只配置词即可，rime引擎会自动计算编码。
- 注意：默认关了用户词库（为了固定词频），如有需要，修改`flypy_flypy.schema.yaml enable_user_dict: true`开启
- 默认固定词频，编辑`cn_dicts_xh/user.dict.yaml`来添加自定义的词
- 默认显示2字以下的辅助码编码，可在`flypy_flypy.schema.yaml`中`translator/spelling_hints`调整为更多或不显示
- 词库文件见`flypy_flypy.extended.dict.yaml(zrm_zrm.extended.dict.yaml)`，如有需要可自行修改
- 三字词，用e引导简码，简码取声母，如：阿波罗 eabl,差不多 eibd,巴不得 ebbd。
- 四字词、多字词，用e引导简码，简码取前3个字+末字声母，如：兵败如山倒 ebbrd,霸王硬上弓 ebwyg,天有不测风云 etyby,当仁不让 edrbr
- `changcijian`、`changcijian3`文件是自动从雾凇词库里取的

### 输入效果

- 整句输入插入字辅：

![醉洛阳](readmeimg/qimhzly.png)

- 打词时插入辅助码：

![寄宿](readmeimg/jisub.png)

![极速](readmeimg/jimsu.png)

- 不认识的字可以笔画输入 `ab`引导 hspnz横竖撇捺折

![笔画](readmeimg/bihua.png)

- 也可以部件组字输入 `az`引导

![部件](readmeimg/bujian.png)

![部件](readmeimg/bujian2.png)

- 也可以输入仓颉码 `acj`引导

![仓颉](readmeimg/cangjie5.png)

- 日期时间相关输入：`date time week` `datetime` `timestamp`

  ![datetime](readmeimg\datetime.png)

- 快捷日期输入：N开头

  - ![Nmoshi](readmeimg\Nmoshi.png)

- 符号输入`/fh`，更多符号查看`symbols_caps_v.yaml`

  - ![fh](readmeimg\fh.png)

- 大写数字：`R开头`
  ![R123456](readmeimg/R123456.png)

- 直接输入unicode：U开头
  ![u2ffb](readmeimg/u2ffb.png)

- V模式，计算器模式 感谢[ChaosAlphard](https://github.com/ChaosAlphard)的pr
  ![alt text](readmeimg/v_jsq.png)

- 英文输入：aw开头

  - ![aw](readmeimg\aw.png)

- 日文输入：aj开头

  - ![aj](readmeimg\aj.png)

- O符快符：o开头，可以参考[小鹤应用 · 符号 (flypy.cc)](https://flypy.cc/#/fh)

  - ![ofu](readmeimg\ofu.png)

- 分号符：

  - 因为实现分号符后，分号无法自动上屏，如果希望能使用分号符，可以进行以下操作

  - ```
    # 第一步，修改分号为始码按键并且不让其自动上屏 flypy_flypy.schea.yaml
    speller:
      # 如果不想让什么标点直接上屏，可以加在 alphabet，或者编辑标点符号为两个及以上的映射
      alphabet: ;zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA
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

### 配置文件路径

- windows %APPDATA%\Rime
- mac ~/Library/Rime
- linux ~/.local/share/fcitx5/rime
- android <https://github.com/fcitx5-android/fcitx5-android> /Android/adata/org.fcitx.fcitx5.android/files/data/rime

推荐直接用git管理配置，首次：例如mac可以打开~/Library文件夹，然后`git clone https://github.com/gaboolic/rime-shuangpin-fuzhuma Rime`  后面在Rime文件夹执行`git pull`即可

### 飞键 模糊音相关

```
# flypy_flypy.shema.yaml 里飞键 可选择性开启
- derive/^([yh])j/$1q/    # yj hj就可以打yq hq
- derive/^qx/qw/  # qx就可以打qw
模糊音同理，也是使用derive把平舌音翘舌音互转、前后鼻音互转
```

### 并击相关

- [并击原理](https://github.com/gaboolic/rime-shuangpin-fuzhuma/wiki/%E5%B9%B6%E5%87%BB%E5%8E%9F%E7%90%86)

### todo

```
4码时 2字词优先
6码时 3字词优先
8码时 4字词优先


精简不必要的文件

加火星文支持

41448大字辅助码补完计划

2码 空格打字 tab打词

小鹤双拼 + 自然码部首辅助码

emoji的词库 弄个更好的
```

### 鸣谢

雾凇词库 <https://github.com/iDvel/rime-ice>

小鹤双拼+辅助码 <https://gitee.com/functoreality/rime-flypy-zrmfast>

魔然（自然码双拼辅助码）：<https://github.com/ksqsf/rime-moran>

星空键道：<https://github.com/xkinput/Rime_JD>

手机版trime皮肤 <https://github.com/SivanLaai/rime-pure>

细胞词库&各个发行版配置 <https://github.com/Bambooin/rimerc>

拆字使用的词典 <https://github.com/mirtlecn/rime-radical-pinyin>
