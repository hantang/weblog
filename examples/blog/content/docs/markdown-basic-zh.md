---
title: "Markdown基础（中文翻译）"
author: 
date: 2023-05-28
draft: false
summary: "Markdown基础语法"
comment: "翻译自<https://daringfireball.net/projects/markdown/>"
---

> 翻译自<https://daringfireball.net/projects/markdown/>

## 了解Markdown格式化语法的要点

本文简要说明了如何使用Markdown。
语法页面对所有特征提供完整、详细的文档，
但实际上Markdown通过找几个例子就很容易上手。
本文中的例子都以一种“之前、之后”的方式写作，
分别表示以Markdown语法的写作内容和对应生成的HTML输出内容。

直接试试写Markdown也很有用。
Dingus提供了一个网页程序，
你可以在上面写你自己的Markdown格式的文本，并转换成XHTML格式。

**注意：** 本文档就是以markdown写成的；
你可以在URL上加上`.text`看得开源代码。

## 段落，标题，块引用

一个段落就是简单的一行或多行连续都文本，被一个或多个空白行分隔。
（空白行指的是任何看起来是空白的行——比如什么都没有
但有一些空格或制表符。）常规段落不用空格或制表符缩进。

Markdown提供了两种风格的标题：Setext和atx。
Setext风格的标题中，`<h1>`和`<h2>`分别用等号（`=`）和连字符（`-`）以下划线的方式标注。
atx风格的标题，你需要在每行开头填放1到6个井字符（`#`）,井字符数量等同于产生的HTML标题层级。

块引用是用邮件风格'`>`'的尖括号。

Markdown:

```markdown
一级标题
=======

二级标题
-------

Now is the time for all good men to come to
the aid of their country. 这仅仅是一个
普通段落。

The quick brown fox jumped over the lazy
dog's back.

### 标题3

> 这是一个块引用。
> 
> 这是块引用中的第二个段落。
> 
> ## 这是块引用的H2标题
```

输出：

```html
<h1>一级标题</h1>

<h2>二级标题</h2>

<p>Now is the time for all good men to come to
the aid of their country. 这仅仅是一个
普通段落。</p>

<p>The quick brown fox jumped over the lazy
dog's back.</p>

<h3>标题3</h3>

<blockquote>
<p>这是一个块引用。</p>

<p>这是块引用中的第二个段落。</p>

<h2>这是块引用的H2标题</h2>
</blockquote>
```

### 短语强调

Markdown使用星号和下划线实现强调效果。

Markdown:

```markdown
这些词中有些是被*强调的*。
这些词中有些_也被强调了_。

用两个星号实现**加粗强调**。
你也可以__用两个下划线__。
```

输出：
```html
<p>这些词中有些是被<em>（斜体）强调的</em>。
这些词中有些<em>也被强调了</em>。</p>

<p>用两个星号实现<strong>加粗强调</strong>。
你也可以<strong>用两个下划线</strong>。</p>
```

## 列表

无需（项目符号）列表可以用星号，加号和连字符（`*`, `+`和`-`）
作为列表标记符，这3个标记符是可以互相替换的；比如这个：
```markdown
* Candy.
* Gum.
* Booze.
```

这个：
```markdown
+ Candy.
+ Gum.
+ Booze.
```

和这个：
```
- Candy.
- Gum.
- Booze.
```

都会得到相同的输出：
```html
<ul>
<li>Candy.</li>
<li>Gum.</li>
<li>Booze.</li>
</ul>
```

有序（数字排序的）列表使用常规的数字，周期性的排序，
比如列表标记：
```markdown
1. Red
2. Green
3. Blue
```

输出：
```html
<ol>
<li>Read</li>
<li>Green</li>
<li>Blue</li>
</ol>
```

如果你在项目之间放入了空白行，你会在列表
文本中得到`<p>`标记。你可以通过缩进4个空格
或1个制表符创建多个段落的列表项目：

```markdown
* 一个列表项目。

    多个段落。

* 另一个列表中的项目。
```

输出：
```markdown
<ul>
<li><p>一个列表项目。</p>
<p>多个段落。</p></li>
<li><p>另一个列表中的项目。<p></li>
</ul>
```

## 链接

Markdown支持两个风格的创建链接方式：*行内*和*引用*。两种风格，
你都需要对要变成链接的文本框住一个方括号。

行内风格紧跟在链接文本后使用圆括号。比如：
```markdown
这是一个[示例链接])(http://example.com/)。
```

输出：
```html
<p>这是一个<a href="http://example.com/">示例链接</a>。
```

可选的是，你可以在圆括号内包含一个标题属性：
```markdown
这是一个[示例链接])(http://example.com/ "带一个标题说明")。
```

输出：
```html
<p>这是一个<a href="http://example.com/" title="带一个标题说明">示例链接</a>。
```

引用风格的链接你可以对引用的链接命名，名字可以定义在文档他处：
```markdown
我从[Google][1]得到流量是[Yahoo][2]或者[MSN][3]的10倍以上。

[1]: http://google.com/        "Google"
[2]: http://search.yahoo.com/  "Yahoo Search"
[3]: http://search.msn.com/    "MSN Search"
```
输出
```html
<p>我从<a href="http://google.com/" title="Google">Google<a>
得到流量是<a href="http://search.yahoo.com/" title="Yahoo Search">
Yahoo</a>或者<a href="http://search.msn.com/" title="MSN Search">
MSN</a>的10倍以上。</p>
```

标题属性是可选的。链接的名字可以字母、数字和空格，但是大小写无关：
```markdown
我以一杯咖啡和一份[《纽约时报》][NY Times]开始我的早晨。
I start my morning with a cup of coffee and

[ny times]: http://www.nytimes.com/
```
输出：
```
我以一杯咖啡和一份<a href="http://www.nytimes.com/">
《纽约时报》</a>开始我的早晨。
```

### 图片

图片语法和链接语法非常相似。

行内（标题可选）：
```
![alt文本](/路径/目录/图片名.jpg "标题")
```
引用风格：
```
![alt文本][id]

[id]: /路径/目录/图片名.jpg "标题"
```

场面两个例子都输出一样的结果：
```html
<img src="/路径/目录/图片名.jpg" alt="alt文本" title="标题" />
```

### 代码

在一个普通的段落里，你可以对文本用反引号包住而得到一个代码块。
与字符（`&`）和尖括号（`<`或`>`）都会自动转成成HTML实体。
这些都很容易用Markdown写HTML例子都代码：
```markdown
我强烈建议反对使用任何`<blink>`符号。

我希望SmartyPants使用类似`&mdash;`的命名实体而不是
十进制编码的实体，比如`&#8212;`。
```

输出：
```
<p>我强烈建议反对使用任何<code>&lt;blink&gt;</code>符号。</p>

<p>我希望SmartyPants使用类似<code>&amp;mdash;</code>
的命名实体而不是十进制编码的实体，比如<code>&amp;#8212;</code>。
```

如果需要对一整个文本块都进行代码格式化，需要块中的每行都缩进4个空格或1个制表符。
和行内代码一样，字符`&`、`<`和`>` 都会自动转义。

Mardkown:
```markdown
如果你想要你的页面能够通过XHTML 1.0严格验证，
你需要在你的的引用块里放上段落标记：

    <blockquote>
        <p>比如说.</p>
    </blockquote>
```

输出：
```html
<p如果你想要你的页面能够通过XHTML 1.0严格验证，
你需要在你的的引用块里放上段落标记：</p>

    <pre><code>&lt;blockquote&gt;
        &lt;p&gt;比如说&lt;/p&gt;
    &lt;/blockquote&gt;
    </code></pre>
```

