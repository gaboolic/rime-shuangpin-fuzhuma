
自用rime配置文件,词库使用最强简体词库——[雾凇拼音](https://github.com/iDvel/rime-ice)，在雾凇拼音的基础上实现自然码双拼、小鹤双拼，以及对应的辅助码。

配置文件参考[小鹤双拼+自然快手/小鹤双形辅助码](https://github.com/functoreality/rime-flypy-zrmfast)

[魔改自然碼 Rime 方案 (自然碼雙拼+輔助碼+外語混輸+簡繁方案+emoji)](https://github.com/ksqsf/rime-moran)

主要配置文件:

flypy_flypy.schema.yaml # 小鹤双拼+鹤形辅助码
zrm_zrm.schema.yaml # 自然码双拼+自然码辅助码

注意：默认关了用户词库（为了固定词频），如有需要，修改flypy_flypy.schema.yaml enable_user_dict: true 开启

词库文件见flypy_flypy.extended.dict.yaml(zrm_zrm.extended.dict.yaml)，如有需要可自行修改

3字词，用o引导简码，如：阿波罗 oabl。4字词、多字词，用e引导简码，如：阿坝藏族羌族自治州 eabz。

changcijian、changcijian3文件是自动从雾凇词库里取的

### 输入效果

整句输入插入字辅：
![醉洛阳](readmeimg/qimhzly.png)

打词时插入辅助码：
![寄宿](readmeimg/jisub.png)
![极速](readmeimg/jimsu.png)

不认识的字可以笔画输入 `ab`引导 hspnz横竖撇捺折
![笔画](readmeimg/bihua.png)

也可以部件组字输入 `az`引导
![部件](readmeimg/bujian.png)
![部件](readmeimg/bujian2.png)

也可以输入仓颉码 `acj`引导
![仓颉](readmeimg/cangjie5.png)

日期时间相关输入：date time week datetime timestamp。
符号输入/fh，更多符号查看symbols_caps_v.yaml

### 配置文件路径

windows %APPDATA%\Rime

mac ~/Library/Rime

linux ~/.local/share/fcitx5/rime

android <https://github.com/fcitx5-android/fcitx5-android> /Android/adata/org.fcitx.fcitx5.android/files/data/rime

### 并击相关

并击双拼方案：

自然码：double_pinyin_zrm.schema.yaml

小鹤：double_pinyin_xh.schema.yaml

并击双拼原理：
左手能控制23个声母，右手能控制24个韵母，把右手上左手没有的键，映射到左手。左手键映射到右手。

```
chord_composer:
  # 字母表，包含用并击按键
  # 击键一律以字母表顺序排列
  alphabet: "aqzswxdecfrvgtbhynjumki,lo.;p',./"
  algebra:
    # - "xform/^,$/,/"
    # - "xform/^\.$/./"
    # 定义左手11键       
    - xform/^at(?![左右])/y左/
    - xform/^ar(?![左右])/u左/
    - xform/^ae(?![左右])/i左/
    - xform/^aw(?![左右])/o左/
    - xform/^qf(?![左右])/p左/
    - xform/^as(?![左右])/l左/
    - xform/^ad(?![左右])/k左/
    - xform/^af(?![左右])/j左/
    - xform/^ag(?![左右])/h左/
    - xform/^ac(?![左右])/m左/
    - xform/^av(?![左右])/n左/

    # 定义右手15键
    - xform/jp(?![左右])$/q右/
    - xform/jo(?![左右])$/w右/
    - xform/ji(?![左右])$/e右/
    - xform/ul(?![左右])$/r右/
    - xform/yl(?![左右])$/t右/
    - xform/l;(?![左右])$/s右/
    - xform/kl(?![左右])$/d右/
    - xform/jk(?![左右])$/f右/
    - xform/hl(?![左右])$/g右/    
    - xform/mk(?![左右])$/z右/
    - xform/nk(?![左右])$/x右/
    - xform/ml(?![左右])$/c右/
    - xform/nl(?![左右])$/v右/
    - xform/ni(?![左右])$/b右/
    - xform/;(?![左右])$/a右/
  # 并击完成后套用式样
  output_format:
    - "xform/^(.*)左/$1/"
    - "xform/^(.*)右$/$1/"
    - "xform/^(.*)左(.*)右$/$1$2/"
```

这样相当于左右手都能控制26个字母。（这段配置参考了星空键道）
我可以做到只用左手打字，也可以实现左右手并击，敲一次出一个字。因为我的字母顺序是左手字母在前，这样并击出来的字符就一定是声母在前。

例如：

地，本来就是左手声母，只需要并击d和i即可
皮，p在右手需要映射到左手，用qf，所以并击qf就出现p，并击qfi 就出现皮
么，m在右手，e在左手，正好相反。需要并击ac出m 并击ji出e，并击acji出么
我的方案优点是可串击可并击，可正常打字，可用单手。
我只是在正常双拼基础上，加了左右手映射。映射规则基本上就是镜像一下再加个字母，例如yuio镜像到左手分别是trew加上a，p是q加上f

### 参考

雾凇词库 <https://github.com/iDvel/rime-ice>

小鹤双拼+辅助码 <https://gitee.com/functoreality/rime-flypy-zrmfast>

星空键道：<https://github.com/xkinput/Rime_JD>

魔然（自然码双拼辅助码）：<https://github.com/ksqsf/rime-moran>

手机版trime皮肤 <https://github.com/SivanLaai/rime-pure>

词库&各个发行版配置 <https://github.com/Bambooin/rimerc>
