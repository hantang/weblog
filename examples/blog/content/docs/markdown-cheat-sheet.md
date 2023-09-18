---
title: "Markdown: Cheat Sheet"
author:
date: 2023-05-29 22:38:00
lastmod:
draft: false
layout:
summary: "Markdown语法速查表"
comment: "来自<https://markdown.com.cn/cheat-sheet.html>"
---


> 参考自:
> * <https://markdown.com.cn/cheat-sheet.html>
> * <https://keatonlao.gitee.io/a-study-note-for-markdown/syntax/>

## 基本语法

### 标题heading, `H1-H6`
```markdown
# 这是 H1
## 这是 H2
### 这是 H3
#### 这是 H4
##### 这是 H5
##### 这是 H6
```

### 段落和换行符
```markdown
段落1：段落之间间隔1行及以上的空白行

段落2

段落3部分1(方式1：尾部有2个空格)
部分2(方式2：html-br标签换行)<br>
部分3(方式3：反斜杠，不推荐)\
```

### 引用
```markdown
> 这是一个引用段落
>
> 引用段落2**加粗**
>
> ## 某个标题
>> 嵌套引用
```

### 无序列表、有序列表
```markdown
* 无序列表（用`*`,`-`或`+`，可以嵌套）
* 项目A
    * 子项目A1
    * 子项目A1
* 项目B
* 项目C

1. 有序列表（`数字.`，数字实际值不重要）
1. 有序2
2. 还是有序
```

### 分隔线
```markdown
连续3个以上减号、星号、下划线，单独一行

---
***
___
```

### 链接
```markdown
* 行内链接：

This is [an example](http://example.com/ "Title") inline link.
[This link](http://example.net/) has no title attribute.

* 参考链接：方括号引用

This is [an example][id] reference-style link.
[id]: http://example.com/  "Optional Title Here"

* 自动链接：尖括号
<http://example.com/>
```

### 图片
```markdown
和链接语法相似

![Alt text](/path/to/img.jpg)
![Alt text](/path/to/img.jpg "Optional title")
```

### 强调（斜体、粗体）
```markdown
强调（斜体<em>）
*斜体*
_斜体_

粗体(<strong>)
**double asterisks**

加粗强调（加粗斜体）
***加粗斜体***

补充：\* 进行转义
```

### （行内）代码
```markdown
用单个反引号

Use the `printf()` function.
``Use `code` in your Markdown file.`` （``转义，内部有反引号）
```

### 代码块
```markdown
+ 方式1: 缩进4个空格

    print("Hello")

+ 方式2: 3个反引号
    ```c
    print("Hello")
    ```
```

## 扩展语法

### 任务列表
```markdown
- [ ] 无需列表后增加`[]`，中间空表示未完成，中间x表示完成
    - [x] 完成了
    - [ ] 没完成
- [x] 也完成了
```

### 表格

* 语法：
```markdown

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
```

* 输出：

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |

### 数学公式
```markdown
行内公式$a^2+b^2=c^2$

行间公式
$$
E = mc^2
$$
```

### 脚注
```markdown
在这段文字后添加一个脚注[^footnote]。

[^footnote]: 这里是脚注的内容。
```

### 目录
```markdown
[toc]
```

### 标题编号
```markdown
### My Great Heading {#custom-id}
```

### 删除线
```markdown
~~删除线~~
```

### Front Matter
```markdown
比如一组3个横线包括的YAML语法段落，比如

---
title: "文章标题"
athor: "我"
date: 2023-01-01

---

```

### 流程图【略】

### 其他
```markdown
* 下划线，直接HTML标签：<u>Underline</u>
* Emoji, 用emoji shortcode: :smile:
* 上标：x^2, x<sup>2</sup>
* 下标：H_2, H<sub>2</sub>
* 直接用HTML标签
```

