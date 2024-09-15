# 说明

重磅发布：墨奇音形，支持自然码、小鹤、搜狗、微软双拼。墨奇音形是一个基于字形描述信息、递归拆分，最后取首末双形音托的码表开源的方案。详见[墨奇码拆分规则](https://github.com/gaboolic/rime-shuangpin-fuzhuma/wiki/%E5%A2%A8%E5%A5%87%E7%A0%81%E6%8B%86%E5%88%86%E8%A7%84%E5%88%99)。[墨奇码](https://github.com/gaboolic/moqima-tables)的拆分码表已开源，目前已经拆分完成全部的通用规范汉字、常用繁体字，总计支持4万字（方案选单中支持大字集和小字集切换）。未来准备支持gb18030-2022标准的8万字。墨奇音形的方案支持ctrl+p开关显示墨奇辅助码+首末字形，ctrl+l开关显示墨奇拆字的拆分。

重磅发布2：现在词库独立演进维护，改为使用745396750字的高质量语料，进行分词，重新统计字频、词频，归一化的[白霜词库](https://github.com/gaboolic/rime-frost)，白霜词库是目前rime方案下最好的词库，在不使用智能模型的情况下可以超越使用智能模型的词库方案。

重磅发布3：墨奇万象词库版，通过拼写运算实现的各种双拼和辅助码排列组合。例如小鹤双拼+虎码首末，微软双拼+墨奇码，自然码双拼+五笔前两码，紫光双拼+仓颉首末码等等。支持的双拼、辅助码运算规则在<https://github.com/gaboolic/rime-shuangpin-fuzhuma/blob/main/moqi_speller.yaml>。让天下双拼用户人人用得上辅助码。

更新日志：[更新日志.md](md/update-log.md)

在线试用：[墨奇音形顶屏版](https://my-rime.vercel.app/?plum=gaboolic/rime-shuangpin-fuzhuma@master:moqi_single_xh)

[墨奇音形大词库版](https://my-rime.vercel.app/?plum=gaboolic/rime-shuangpin-fuzhuma@master:moqi_xh,moqi_zrm) (词库多，加载较慢)

- [此仓库](https://github.com/gaboolic/rime-shuangpin-fuzhuma)为rime配置文件,词库使用基于[雾凇拼音](https://github.com/iDvel/rime-ice)的最强简体词库——[白霜词库](https://github.com/gaboolic/rime-frost)，实现自然码双拼、小鹤双拼、搜狗双拼、微软双拼等多种双拼，以及墨奇码（原创拆分开源支持4万字）、自然码部首辅、小鹤音形（鹤形辅）多种辅助码。本人日常用的是此仓库的方案，高强度使用，所以更新有保证。
- 配置文件参考[小鹤双拼+自然快手/小鹤双形辅助码](https://github.com/functoreality/rime-flypy-zrmfast)
- [魔改自然碼 Rime 方案 (自然碼雙拼+輔助碼+外語混輸+簡繁方案+emoji)](https://github.com/ksqsf/rime-moran)
- 主要配置文件:
  - schema: moqi_xh # 墨奇辅助码 鹤拼版 大词库版本 非自动上屏，支持4万字
  - schema: moqi_zrm # 墨奇辅助码 自然双拼版 大词库版本 非自动上屏，支持4万字
  - schema: flypy_flypy # 鹤形+鹤拼, 小鹤官方就只有8000字左右
  - schema: zrm_zrm # 自然码+自然码部首辅助码
  - schema: moqi_single_xh # 墨奇码·顶屏版·小鹤双拼，为了4码自动上屏 只收录了8000字
  - schema: moqi_sogou # 墨奇辅助码搜狗双拼版 大词库版本 非自动上屏，支持4万字
  - schema: moqi_ms # 墨奇辅助码微软双拼版 大词库版本 非自动上屏，支持4万字
- 写给选择困难症：如果第一次接触双拼，直接使用`moqi_xh.schema.yaml`，墨奇辅助码 鹤拼版，这是作者用的方案；如果以前接触过双拼没有接触过形并且熟练掌握双拼，使用moqi_xx.schema.yaml；如果熟练小鹤音形，使用`flypy_flypy.schema.yaml`;如果追求类似五笔的4码自动上屏体验，则使用`moqi_single_xh`墨奇码·顶屏版
- 词库文件分别为`moqi.extended.dict.yaml`（墨奇音形）、`flypy_flypy.extended.dict.yaml`（鹤拼鹤形）和`zrm_zrm.extended.dict.yaml`（自然码拼+自然码部首辅），默认只开启了我用[雾凇词库](https://github.com/iDvel/rime-ice)转换的词典文件。此外还有从其他地方获取的细胞词库，例如历史类、地名类、古诗文、计算机、动漫、电影、游戏、电商等，可自行打开注释或从[细胞词库](https://github.com/Bambooin/rimerc/tree/master/luna_pinyin)获取。如无特殊需求，词典文件只配置词即可，rime引擎会自动计算编码。
- 注意：默认关了用户词库（为了固定词频），如有需要，修改`你使用的方案.schema.yaml enable_user_dict: true`开启
- 默认固定词频，编辑`cn_dicts_common/user.dict.yaml`来添加自定义的词；推荐在用户词库关闭的情况下使用ac引导造词，这样自造词是在系统词库后面，不会影响系统词的字频和词序。
- 默认显示单字的辅助码编码，可在`你使用的方案.schema.yaml`中`translator/spelling_hints`调整为更多或不显示
- 超级简拼：1码、2码、3码时，按下Tab（或者是/，或者是。都可以）自动上屏1字、2字词、3字词，不和空格上屏的单字冲突
- 三字词，用e引导简码，简码取声母，如：阿波罗 eabl,差不多 eibd,巴不得 ebbd。
- 四字词、多字词，用e引导简码，简码取前3个字+末字声母，如：兵败如山倒 ebbrd,霸王硬上弓 ebwyg,天有不测风云 etyby,当仁不让 edrbr
- `changcijian`、`changcijian3`文件是自动从雾凇词库里取的

### FAQ（常见问题）q羣696353204/10885687

  更多配置及功能请看：[FAQ.md](md/FAQ.md)

### 如何安装&配置文件路径

下载本仓库的压缩包Code - Download ZIP（或者下载[releases](https://github.com/gaboolic/rime-shuangpin-fuzhuma/releases)最新的source-code.zip），解压到如下路径即可

- windows：%APPDATA%\Rime
- mac
  - [鼠须管](https://github.com/rime/squirrel)路径为~/Library/Rime
  - [fcitx5-mac版](https://github.com/fcitx-contrib/fcitx5-macos)路径为~/.local/share/fcitx5/rime
- linux
  - [fcitx5-rime](https://github.com/fcitx/fcitx5-rime)路径为~/.local/share/fcitx5/rime
  - fcitx5 flatpak版的路径~/.var/app/org.fcitx.Fcitx5/data/fcitx5/rime
  - [ibus-rime](https://github.com/rime/ibus-rime)路径为~/.config/ibus/rime
- android
  - [fcitx5-安卓版](https://github.com/fcitx5-android/fcitx5-android)路径为 /Android/data/org.fcitx.fcitx5.android/files/data/rime
  - [同文](https://github.com/osfans/trime)路径为 /rime
- ios [仓输入法](https://github.com/imfuxiao/Hamster) 目前已内置，也可以通过【输入方案设置 - 右上角加号 - 方案下载 - 覆盖并部署】来更新墨奇音形。

如果会使用git基本操作，可以直接用git管理配置，首次：例如mac可以打开~/Library文件夹，然后`git clone --depth 1 https://github.com/gaboolic/rime-shuangpin-fuzhuma Rime`  后面在Rime文件夹执行`git pull`即可

现在也支持[东风破](https://github.com/rime/plum)，选择配方（recipes/*.recipe.yaml）来进行安装或更新：

- ℞ 安装或更新全部文件 执行`bash rime-install gaboolic/rime-shuangpin-fuzhuma:recipes/full`
- ℞ 安装或更新所有的词库文件 执行`bash rime-install gaboolic/rime-shuangpin-fuzhuma:recipes/all_dicts`

### 输入效果

- 整句输入插入字辅：

![醉洛阳](readmeimg/qimhzly.png)

- 打词时插入辅助码：

![寄宿](readmeimg/jisub.png)

![极速](readmeimg/jimsu.png)

- 整句输入时增强单字性能，增加syffo或者syff/ 5码上屏单字的功能
![zssr](readmeimg/zssr.png)

- 不认识的字可以笔画输入 `ab`引导 hspnz横竖撇捺折

![笔画](readmeimg/bihua.png)

- 也可以部件组字输入 `az`引导

![部件](readmeimg/bujian.png)

![部件](readmeimg/bujian2.png)

- 也可以输入仓颉码 `acj`引导

![仓颉](readmeimg/cangjie5.png)

- 通过opencc支持繁简转换、火星文、首末拆分字形(墨奇音形)

![繁体](readmeimg/fantizi.png)

![火星文](readmeimg/huoxingwen.png)

![拆分](readmeimg/shoumo-chai.png)

![全拆](readmeimg/quanchai.png)

- 超级简拼：1码、2码、3码时，按下Tab（或者是/，或者是。都可以）自动上屏1字、2字词、3字词，不和空格上屏的单字冲突
![等-蛋糕](readmeimg/dg-蛋糕.png)

墨奇音形的方案支持ctrl+p开关显示墨奇辅助码+首末字形,ctrl+l开关显示墨奇拆字的拆分

- 日期时间相关输入：`date time week` `datetime` `timestamp`

  ![datetime](readmeimg/datetime.png)

- 快捷日期输入：N开头

  - ![Nmoshi](readmeimg/Nmoshi.png)

- 符号输入`/fh`，更多符号查看`symbols_caps_v.yaml`

  - ![fh](readmeimg/fh.png)

- 大写数字：`R开头`
  ![R123456](readmeimg/R123456.png)

- 直接输入unicode：U开头
  ![u2ffb](readmeimg/u2ffb.png)

- 计算器功能(V模式) 感谢[ChaosAlphard](https://github.com/ChaosAlphard)的[pr](https://github.com/gaboolic/rime-shuangpin-fuzhuma/pull/41)
  ![alt text](readmeimg/v_jsq.png)

  - [计算器功能介绍](md/calc.md)
  - ![1](md/assets/1.png)
  
- 英文输入：aw开头

  - ![aw](readmeimg/aw.png)

- 日文输入：aj开头

  - ![aj](readmeimg/aj.png)

- 翻译功能：ctrl + E开启英汉、汉英互译。
  
  - ![ink](readmeimg/ink.png)
  - ![奇特](readmeimg/qite.png)

- O符快符：o开头，快速输入各种符号偏旁部件，可以参考[快符](md/fuhao.md)      [部件](md/bujian.md)

  - ![ofu2](readmeimg/ofu2.png)
  - ![ofu](readmeimg/ofu.png)

- 分号符：

  - 因为实现分号符后，分号无法自动上屏，如果希望能使用分号符，可以进行以下操作 [分号符](md/fenhaofu.md)

### 飞键 模糊音相关

```
# `你使用的方案.shema.yaml` 里飞键 可选择性开启
- derive/^([yh])j/$1q/    # yj hj就可以打yq hq
- derive/^qx/qw/  # qx就可以打qw
模糊音同理，也是使用derive把平舌音翘舌音互转、前后鼻音互转，详见issue中的faq
```

### 并击相关

- [并击原理](https://github.com/gaboolic/rime-shuangpin-fuzhuma/wiki/%E5%B9%B6%E5%87%BB%E5%8E%9F%E7%90%86)

### todo

```

4字成语的码表优化 补全

简码回显 - doing

墨奇音形自然码下 e简码问题修复

墨奇音形自动上屏版，4码为词，4码+/自动上屏单字，a-z顶词

置顶词、删除词

出简让全的开关、tab提示的开关

字典功能，反查时生僻字显示读音和释义

```

### 鸣谢

雾凇拼音 <https://github.com/iDvel/rime-ice> 参考了其中很多配置

白霜词库 <https://github.com/gaboolic/rime-frost> 本项目使用的词库和词频来自白霜词库

墨奇码码表 <https://github.com/gaboolic/moqima-tables> 墨奇音形的拆分

小鹤双拼+辅助码 <https://gitee.com/functoreality/rime-flypy-zrmfast>

魔然（自然码双拼辅助码）：<https://github.com/ksqsf/rime-moran>

细胞词库&各个发行版配置 <https://github.com/Bambooin/rimerc>

az部件组字模式使用的词典 <https://github.com/mirtlecn/rime-radical-pinyin>

声笔输入法 <https://github.com/sbsrf/sbsrf> 使用了其中的lua脚本，参考了tab上屏简拼功能

星空键道：<https://github.com/xkinput/Rime_JD>

英汉/汉英字典 <https://github.com/lxs602/Chinese-Mandarin-Dictionaries>

墨奇本猫：

<img src="readmeimg/moqi1.jpg" width=30%>

<img src="readmeimg/moqi2.jpg" width=30%>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=gaboolic/rime-shuangpin-fuzhuma&type=Date)](https://star-history.com/#gaboolic/rime-shuangpin-fuzhuma&Date)
