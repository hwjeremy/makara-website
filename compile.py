"""
Makara Website
Page Compilation Tool
author: hugh@blinkybeach.com
copyright: Blinky Beach Pty Ltd
"""
import os
import sys

JS_DIRECTORY = 'javascript'
STYLE_DIRECTORY = 'styles'
HTML_FILENAME = 'template.html'
ANALYTICS_FILENAME = 'analytics.js'

DEBUG = False
if len(sys.argv) > 2:
    raise RuntimeError('Only one argument may be supplied (--debug)')
if len(sys.argv) > 1:
    if sys.argv[1] != '--debug':
        raise RuntimeError('Unknown argumend supplied')
    DEBUG = True

def join_files(directory: str, extension: str, separator: str) -> str:
    """
    Loop through each file in a directory, check for a file extension, and join
    the contents of files with that extension into a big string. Return that
    string.
    """
    joined_files = ''
    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        if not filepath.endswith(extension):
            continue
        with open(filepath) as file_to_join:
            start = '\n' + separator + '\n'
            end = '\n' + separator[0] + '/' + separator[1:] + '\n'
            content = start + file_to_join.read() + end
            joined_files += content
            continue
    return joined_files

def compile(debug=DEBUG) -> None:
    js_classes = join_files(JS_DIRECTORY + '/classes', '.js', '<script>')
    js_scripts = join_files(JS_DIRECTORY + '/scripts', '.js', '<script>')
    styles = join_files(STYLE_DIRECTORY, '.css', '<style>')

    analytics = '<!-- Analytics excluded (debug / development mode) -->'
    if debug is False:
        with open(ANALYTICS_FILENAME) as analytics_file:
            analytics = analytics_file.read()

    with open('./template.html') as template_file:
        template = template_file.read()

    HTML = template.format(
        js_scripts=js_scripts,
        js_classes=js_classes,
        styles=styles,
        analytics=analytics
    )

    with open('index.html', 'w') as index_file:
        index_file.write(HTML)

if __name__ == '__main__':
    compile()
