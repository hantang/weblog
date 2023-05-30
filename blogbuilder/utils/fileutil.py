"""file utils"""
import logging
import re

from .configutil import check_config_sep, loads_config, obtain_config_type


def divide_textfile(path, encoding="utf-8"):
    """
    解析markdown文件，拆分为两部分：
        meta: meta-type, meta-data, meta-extra
        body: text, resources
    """
    logging.debug(f"--> read text, path={path}")
    raw_texts = _read_textfile(path, encoding)
    (meta_raw, meta_type), body_raw = _divide_text_parts(raw_texts, path)
    meta_data = loads_config("".join(meta_raw), meta_type)

    logging.debug("--> read text, metatype={}, meta={}, body={}".format(meta_type, len(meta_raw), len(body_raw)))
    return (meta_raw, meta_type, meta_data), body_raw


def alter_html_images(html_text, is_sub=True):
    """
    本地图片都替换到文件同级目录下。
    todo bug 还是潜在风险： 比如图片是在代码块中的（非图片元素）。

    通过正则得到图片路径字符串并替换:
    结果=[全部图片字符串，前缀，字符串路径，盘符，根目录，子目录，文件名，文件后缀，后缀]
    """
    pchar1 = r'/\\'
    pchar2 = r'<>'
    pchar4 = r'"()\^' + pchar2 + pchar1
    image_suffix = '(jpeg|jpg|png|gif|webp|svg|tiff|bmp|jp2|heic)'
    pattern_image = rf'(\w:)?([{pchar1}]?)((?:[^{pchar4}]+[{pchar1}])*?)([^{pchar4}]*\.{image_suffix})'  # 匹配的图片格式
    pattern2 = rf'((<img\s+[^{pchar2}]*?src=")({pattern_image})("(?:\s+[^{pchar2}]+)?>))'  # html<img>标签

    images = re.findall(pattern2, html_text)
    image_paths = sorted(set([img[2] for img in images]))
    if is_sub:
        new_text = re.sub(pattern2, r'\2\7\9', html_text)  # 从1开始
    else:
        new_text = html_text

    logging.debug('find local images-count={}/{}, images={}'.format(
        len(images), len(image_paths), image_paths[:5]))
    return image_paths, new_text


def _read_textfile(path, encoding):
    """读取文件并去除首尾连续的空白行"""
    with open(path, encoding=encoding) as f:
        lines = f.readlines()
    first_non_blank, last_non_blank = 0, 0
    for i, line in enumerate(lines):
        if len(line.strip()) > 0:
            first_non_blank = i
            break
    for i, line in enumerate(lines[::-1]):
        if len(line.strip()) > 0:
            last_non_blank = i
            break
    texts = lines[first_non_blank:len(lines) - last_non_blank]
    return texts


def _divide_text_parts(texts, path, date2str=True):
    """按行判断得到meta(front matter)和body（正文）"""
    meta_raw = []
    meta_type = None
    body_raw = []
    if len(texts) == 0:
        return (meta_raw, meta_type), body_raw
    line_index = 0
    line_sep = texts[line_index].rstrip()

    if check_config_sep(line_sep):
        meta_type = obtain_config_type(line_sep)
        line_index += 1
        is_end = False
        for line in texts[line_index:]:
            line_index += 1
            if line.rstrip() == line_sep:
                is_end = True
                break
            assert len(line.strip()) > 0, \
                f"error: frontmatter parsing exists empty lines, filepath={path}"
            meta_raw.append(line)
        assert is_end, f"error: frontmatter not ends with {line_sep}, filepath={path}"
    body_raw = texts[line_index:]
    return (meta_raw, meta_type), body_raw
