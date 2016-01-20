#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class CodeBuilder(object):
    """Used to generate python code"""
    def __init__(self, indent=0):
        self.indent = indent
        self.code = []

    INDENT_STEP = 4

    def indent(self):
        """Increase the indent for next line"""
        self.indent += INDENT_STEP
    def dedent(self):
        """Decrease the indent for next line"""
        self.indent -= INDENT_STEP

    def emit_line(self, line):
        """Add a line to the output, linefeed are added"""
        self.code.append('{}{}\n'.format(' '*self.indent, line))

    def __str__(self):
        return "".join(str(c) for c in self.code)

    def add_section(self):
        """Add a placeholder, i.e. a sub-codebuilder"""
        section = CodeBuilder(self.indent)
        self.code.append(section)
        return section

    def get_globals(self):
        """Execute the code, and retrieve the globals it defines"""
        code = str(self)
        global_namespace = {}
        exec(code, global_namespace)
        return global_namespace

class Template():
    """Create a Template"""
    def __init__(self, text, *contexts):
        self.text = text
        self.context = {}
        for context in contexts:
            self.context.update(context)

        self.all_vars = set()

        code_builder = CodeBuilder()
        code_builder.emit_line('def render_function(context, dot_func):')
        code_builder.indent()
        var_defs = code_builder.add_section()
        code_builder.emit_line('result = []')
        code_builder.emit_line('extend_result = result.extend')
        code_builder.emit_line('append_result = result.append')

        buffered = []
        def flush_output():
            """emit output string according to buffer"""
            if len(buffered) == 1:
                code_builder.emit_line('append_result({})'.format(buffered[0]))
            elif len(buffered) > 1:
                code_builder.emit_line('extend_result([{}])'.format(','.join(buffered)))
            del buffered[:]

        # compile the template_string into codes
        tokens = re.split(r'(?s)({{.*?}}|{%.*?%}|{#.*?#})', self.text)

        for token in tokens:
            if token.startswith('{#'):
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                buffered.append('to_str({})'.format(expr))
            elif token.startswith('{%'):
                pass
            else:
                buffered.append(token)

        flush_output()

        # add variables

        # post process
        code_builder.emit_line('return ''.join(result)')
        code_builder.dedent()
        self._render_function = code_builder.get_globals()['render_function']
