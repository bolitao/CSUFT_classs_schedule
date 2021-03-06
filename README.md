# CSUFT_classs_schedule

将中南林业科技大学教务系统课表导出为 ics 日历。

## Usage

### 可执行文件运行

原库不小心删了🌚，release 二进制文件已删除，请使用源码运行。

[release](https://github.com/bolitao/CSUFT_classs_schedule/releases) 页下载对应平台的可执行文件，在终端执行程序。Windows 也可双击 exe 文件直接运行。

运行后会在同级目录生成 `课程表.ics` 文件。

### 通过源码运行

下载或 clone 本项目，切换分支到 `csuft`。

本项目运行需要 Python 3，安装依赖：

```bash
pip install -r requirements.txt
```

本项目中 BeautifulSoup 使用的 HTML 解析器是 [lxml](https://github.com/lxml/lxml)，还需安装 lxml 才能正常运行：

```bash
pip install lxml
```

运行：

```bash
python main.py
```

## BUG

- 暂无法解析周次形如 `1-6,8,10-17` 的课程

## TODO

- 解决周次为 `1-6,8,10-17` 或分割次数更多的奇葩
- 登录失败处理
- 多次输错密码时对验证码的处理
- 重构代码，参考 [Wakeup 课程表](https://github.com/YZune/WakeupSchedule_Kotlin) 优化解析过程
- 单双周


