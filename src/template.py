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
