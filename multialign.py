import sublime
import sublime_plugin
import re


class multialignCommand(sublime_plugin.TextCommand):

    def load_settings(self):
        view_settings   = self.view.settings()
        plugin_settings = sublime.load_settings('multiAlign.sublime-settings')

        # read settings from view
        self.tab_size                 = int(view_settings.get('tab_size', 4))
        self.translate_tabs_to_spaces = view_settings.get('translate_tabs_to_spaces')

        # read settings from plugin setting file, view or set default values
        self.break_at_empty_lines        = plugin_settings.get('break_at_empty_lines', view_settings.get('multiAlign_break_at_empty_lines', True))
        self.break_at_non_matching_lines = plugin_settings.get('break_at_non_matching_lines', view_settings.get('multiAlign_break_at_non_matching_lines', True))
        self.align_chars                 = plugin_settings.get('align_chars',
            view_settings.get('multiAlign_align_chars', [
                {
                    'char':            ' import ',
                    'alignment':       'right',
                    'spaces_left':     0,
                    'spaces_right':    0,
                    'is_in_scope':     ['source.python'],
                    'is_left_of_char': ['from ']
                },
                {
                    'char':            ' as ',
                    'alignment':       'right',
                    'spaces_left':     0,
                    'spaces_right':    0,
                    'is_in_scope':     ['source.python'],
                    'is_left_of_char': ['import ']
                },
                {
                    'char':         '#',
                    'alignment':    'right',
                    'spaces_left':  3,
                    'spaces_right': 1,
                    'is_in_scope':  ['source.python']
                },
                {
                    'char':         '::',
                    'alignment':    'right',
                    'spaces_left':  1,
                    'spaces_right': 1,
                    'is_in_scope':  ['source.modern-fortran', 'source.fixedform-fortran']
                },
                {
                    'char':             ' intent',
                    'alignment':        'right',
                    'spaces_left':      0,
                    'spaces_right':     0,
                    'is_in_scope':      ['source.modern-fortran', 'source.fixedform-fortran'],
                    'is_right_of_char': ['::']
                },
                {
                    'char':         '&',
                    'alignment':    'right',
                    'spaces_left':  1,
                    'spaces_right': 0,
                    'is_in_scope':  ['source.modern-fortran', 'source.fixedform-fortran']
                },
                {
                    'char':         '=>',
                    'alignment':    'right',
                    'spaces_left':  1,
                    'spaces_right': 1
                },
                {
                    'char':            '=',
                    'alignment':       'right',
                    'spaces_left':     1,
                    'spaces_right':    1,
                    'prefixes':        ['+', '-', '*', '/', '.', '%', '<', '>', '!', '=', '~', '&', '|'],
                    'not_enclosed_by': ['()', '[]']
                },
                {
                    'char':            ':',
                    'alignment':       'left',
                    'spaces_left':     0,
                    'spaces_right':    1,
                    'not_enclosed_by': ['[]']
                }
            ])
        )

    def set_defaults_for_missing_settings(self):
        default_settings = {
            'alignment':         'right',
            'spaces_left':       1,
            'spaces_right':      1,
            'prefixes':          [],
            'is_in_scope':       [],
            'not_in_scope':      [],
            'not_enclosed_by':   [],
            'not_left_of_char':  [],
            'not_right_of_char': [],
            'is_enclosed_by':    [],
            'is_left_of_char':   [],
            'is_right_of_char':  []
        }
        valid_align_chars = []
        for align_char in self.align_chars:
            # skip alignment characters without 'char' setting
            if 'char' in align_char:
                # set default values for missing settings
                for setting in default_settings:
                    if setting not in align_char:
                        align_char[setting] = default_settings[setting]
                valid_align_chars.append(align_char)
        self.align_chars = valid_align_chars

    def compile_regex_objects(self):
        regex_string = ''
        for align_char in self.align_chars:
            # add logical or if more than one alignment character is configured
            if regex_string and regex_string[-1] != '|':
                regex_string += '|'

            # compile regex for alignment character
            align_char_regex_string      = self.get_regex_string(align_char)
            align_char['compiled_regex'] = re.compile(align_char_regex_string)

            # add alignment character
            regex_string += align_char_regex_string

        # compile regex for all alignment characters
        self.regex_align_chars = re.compile(regex_string)

        # compile regex for line indentation
        self.regex_indentation = re.compile('^(\s*)\S')

    def get_regex_string(self, align_char):
        if align_char['is_in_scope'] and self.scope not in align_char['is_in_scope']:
            regex_string = '(^$)'
        elif align_char['not_in_scope'] and self.scope in align_char['not_in_scope']:
            regex_string = '(^$)'
        else:
            regex_string = '(\s*)('
            # add prefixes
            if align_char['prefixes']:
                regex_string += '([{0:s}]?)'.format(''.join([re.escape(prefix) for prefix in align_char['prefixes']]))

            # add alignment character
            regex_string += re.escape(align_char['char'])
            if align_char['alignment'] == 'left':
                regex_string += ')(\s*)'
            else:
                regex_string += ')()'
        return regex_string

    def get_match_objects(self, row):
        return list(self.regex_align_chars.finditer(self.get_line(row)))

    def get_match_object_groups(self, match_obj):
        return [element for element in match_obj.groups() if element is not None]

    def get_match_objects_for_main_row(self):
        self.align_chars_main_row = self.get_align_chars(self.main_row, is_main_row=True)

    def get_align_chars(self, row, is_main_row=False):
        def is_enclosed_by(char_list):
            enclose_level = 0
            for enclose_char in char_list:
                char_left     = enclose_char[0]
                char_right    = enclose_char[1]
                if char_left != char_right:
                    regex_string = '{0:s}|{1:s}'.format(re.escape(char_left), re.escape(char_right))
                    for match_obj in re.finditer(regex_string, line):
                        if match_obj.start() < align_char_start:
                            if match_obj.group(0) == char_left:
                                enclose_level += 1
                            elif match_obj.group(0) == char_right:
                                enclose_level -= 1
                        else:
                            break
                else:
                    if is_left_of_char([char_left]) and is_right_of_char([char_right]):
                        enclose_level = 1
                if enclose_level != 0:
                    break
            return enclose_level != 0

        def is_left_of_char(char_list):
            result       = False
            regex_string = '|'.join([re.escape(char) for char in char_list])
            match_obj    = re.search(regex_string, line)
            if match_obj:
                if match_obj.start() < align_char_start:
                    result = True
            return result

        def is_right_of_char(char_list):
            result = False
            regex_string = '(?:{0:s})(?=(?:[^{1:s}])*$)'.format('|'.join([re.escape(char) for char in char_list]), '])|(?:[^'.join(['][^'.join(re.escape(char)) for char in char_list]))
            match_obj = re.search(regex_string, line)
            if match_obj:
                if match_obj.start() > align_char_start:
                    result = True
            return result

        align_chars = []
        line        = self.get_line(row)
        for match_obj in self.get_match_objects(row):
            match_obj_groups          = self.get_match_object_groups(match_obj)
            if len(match_obj_groups) >= 3:
                for align_char in self.align_chars:
                    if align_char['compiled_regex'].search(match_obj_groups[1]):
                        cnt_spaces_left  = len(match_obj_groups[0])
                        cnt_align_char   = len(match_obj_groups[1])
                        align_char_start = match_obj.start() + cnt_spaces_left

                        # skip detected alignment character if any of the checks fails
                        if align_char['not_enclosed_by']:
                            if is_enclosed_by(align_char['not_enclosed_by']):
                                continue
                        if align_char['not_left_of_char']:
                            if is_left_of_char(align_char['not_left_of_char']):
                                continue
                        if align_char['not_right_of_char']:
                            if is_right_of_char(align_char['not_right_of_char']):
                                continue
                        if align_char['is_enclosed_by']:
                            if not is_enclosed_by(align_char['is_enclosed_by']):
                                continue
                        if align_char['is_left_of_char']:
                            if not is_left_of_char(align_char['is_left_of_char']):
                                continue
                        if align_char['is_right_of_char']:
                            if not is_right_of_char(align_char['is_right_of_char']):
                                continue

                        # add detected alignment character to the list
                        if match_obj.start() == 0:
                            target_pos = cnt_spaces_left + cnt_align_char
                        else:
                            target_pos = match_obj.start() + align_char['spaces_left'] + cnt_align_char

                        if is_main_row:
                            # store match_obj, corresponding align_char and checking parameters
                            align_chars.append({
                                'align_char':           align_char,
                                'target_pos':           target_pos,
                                'alignment_required':   False,
                                'match_objects_by_row': {}
                            })
                        else:
                            # store match_obj and corresponding align_char
                            align_chars.append({
                                'align_char': align_char,
                                'match_obj':  match_obj,
                                'target_pos': target_pos
                            })
                        break
        return align_chars

    def get_line(self, row):
        view       = self.view
        text_point = view.text_point(row, 0)
        line       = view.line(text_point)
        return view.substr(line).replace('\t', ' ' * self.tab_size)

    def get_indent(self, row):
        match_obj = self.regex_indentation.search(self.get_line(row))
        if match_obj:
            if self.translate_tabs_to_spaces:
                indent = int(len(match_obj.group(1)) / self.tab_size)
            else:
                indent = len(match_obj.group(1))
        else:
            indent = None
        return indent

    def find_matches_in_all_selections(self):
        self.align_chars_by_row = []

        # loop through all selections beginning at the start row of each selection
        for select in self.selection:
            start_row   = self.view.rowcol(self.view.lines(select)[0].a)[0]
            align_chars = self.get_align_chars(start_row)

            # add match objects for start row of selection
            if align_chars:
                self.align_chars_by_row.append({
                    'row':         start_row,
                    'start_row':   start_row,
                    'direction':   0,
                    'align_chars': align_chars
                })

                # get indent of start_row
                start_indent = self.get_indent(start_row)

                # check lines above and below start_row
                for direction in [-1, 1]:
                    row = start_row + direction
                    while 0 <= row and row <= self.line_cnt:
                        # get indent of current row
                        indent = self.get_indent(row)

                        # handle empty line
                        if indent is None:
                            if self.break_at_empty_lines:
                                break
                            else:
                                row += direction
                                continue

                        # handle indent change
                        elif indent != start_indent:
                            break

                        align_chars = self.get_align_chars(row)
                        align_chars_checked = []

                        # check if align_chars match align_chars_main_row
                        if align_chars:
                            for i, main_align_char in enumerate(self.align_chars_main_row):
                                if len(align_chars) > i:
                                    if align_chars[i]['align_char']['char'] == main_align_char['align_char']['char']:
                                        align_chars_checked.append(align_chars[i])
                                    else:
                                        break

                        # add match objects for current row
                        if align_chars_checked:
                            self.align_chars_by_row.append({
                                'row':         row,
                                'start_row':   start_row,
                                'direction':   direction,
                                'align_chars': align_chars_checked
                            })

                        # skip all lines following in that direction
                        elif self.break_at_non_matching_lines:
                            break

                        # next row
                        row += direction

    def find_max_target_positions(self):
        for i, main_align_char in enumerate(self.align_chars_main_row):
            for row_obj in self.align_chars_by_row:
                if len(row_obj['align_chars']) > i:
                    align_char = row_obj['align_chars'][i]
                    if align_char['align_char']['char'] == main_align_char['align_char']['char']:
                        if main_align_char['target_pos'] < align_char['target_pos']:
                            main_align_char['target_pos'] = align_char['target_pos']

    def check_alignment_to_be_made(self):
        break_at = {}
        for i, main_align_char in enumerate(self.align_chars_main_row):
            main_alignment    = main_align_char['align_char']['alignment']
            main_spaces_left  = main_align_char['align_char']['spaces_left']
            main_spaces_right = main_align_char['align_char']['spaces_right']
            main_target_pos   = main_align_char['target_pos']
            for row_obj in self.align_chars_by_row:
                row       = row_obj['row']
                start_row = row_obj['start_row']
                direction = row_obj['direction']
                if len(row_obj['align_chars']) > i:
                    align_char = row_obj['align_chars'][i]
                    if self.break_at_non_matching_lines and start_row in break_at:
                        if direction == break_at[start_row]['in_direction']:
                            if row * direction > break_at[start_row]['from_row'] * break_at[start_row]['in_direction']:
                                break
                    if align_char['align_char']['char'] == main_align_char['align_char']['char']:
                        # add match object to main alignment character dict
                        match_obj = align_char['match_obj']
                        main_align_char['match_objects_by_row'][row] = match_obj

                        if main_alignment == 'left':
                            # check if alignment is already in target position
                            if match_obj.end() != main_target_pos + main_spaces_right:
                                main_align_char['alignment_required'] = True

                            # check if number of spaces left of alignment character is correct
                            new_match_obj = re.search('^(\s*)\S', self.get_line(row)[match_obj.start():])
                            if new_match_obj:
                                if len(new_match_obj.group(1)) != main_spaces_left:
                                    main_align_char['alignment_required'] = True

                        else:
                            # check if alignment is already in target position
                            if match_obj.end() != main_target_pos:
                                main_align_char['alignment_required'] = True

                            # check if number of spaces right of alignment character is correct
                            new_match_obj = re.search('^(\s*)\S', self.get_line(row)[main_target_pos:])
                            if new_match_obj:
                                if len(new_match_obj.group(1)) != main_spaces_right:
                                    main_align_char['alignment_required'] = True

                    # skip rows if alignment characters order is different
                    elif self.break_at_non_matching_lines:
                        if start_row not in break_at:
                            break_at[start_row] = {}
                        break_at[start_row]['from_row']     = row
                        break_at[start_row]['in_direction'] = direction

            # skip checking other characters
            if main_align_char['alignment_required']:
                break

    def apply_alignment(self, edit):
        for i, main_align_char in enumerate(self.align_chars_main_row):
            if main_align_char['alignment_required']:
                main_alignment    = main_align_char['align_char']['alignment']
                main_spaces_left  = main_align_char['align_char']['spaces_left']
                main_spaces_right = main_align_char['align_char']['spaces_right']
                main_target_pos   = main_align_char['target_pos']

                for row in main_align_char['match_objects_by_row']:
                    match_obj        = main_align_char['match_objects_by_row'][row]
                    match_obj_groups = self.get_match_object_groups(match_obj)
                    cnt_align_char   = len(match_obj_groups[1])
                    line             = self.get_line(row)
                    i_start          = match_obj.start()
                    i_end            = match_obj.end()

                    if main_alignment == 'left':
                        spaces_left  = main_spaces_left
                        spaces_right = main_target_pos - i_start - cnt_align_char + main_spaces_right

                    else:
                        spaces_left  = main_target_pos - i_start - cnt_align_char
                        spaces_right = main_spaces_right

                    # do not add spaces at EOL
                    if i_end == len(line):
                        spaces_right = 0

                    # align line
                    aligned_line = ''.join([
                        line[:i_start],
                        ' ' * spaces_left,
                        match_obj_groups[1],
                        ' ' * spaces_right,
                        line[i_end:].strip()
                    ])

                    # replace existing line with aligned line
                    region = self.view.line(self.view.text_point(row, 0))
                    self.view.replace(edit, region, aligned_line)

                # leave loop after alignment
                break

    def run(self, edit):
        self.selection = self.view.sel()
        self.scope     = self.view.scope_name(self.selection[0].begin()).split()[0]
        self.line_cnt  = self.view.rowcol(self.view.size())[0]
        self.main_row  = self.view.rowcol(self.view.lines(self.selection[0])[0].a)[0]

        self.load_settings()
        self.set_defaults_for_missing_settings()
        self.compile_regex_objects()
        self.get_match_objects_for_main_row()
        self.find_matches_in_all_selections()
        self.find_max_target_positions()
        self.check_alignment_to_be_made()
        self.apply_alignment(edit)
