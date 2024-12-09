
""" Shows differences between two texts with changes highlighted. Two version are provided:
    - show_differences_combined: Returns a single string with changes highlighted, containing extracts from both text1 and text2.
    - show_differences_separate: Returns two strings with changes highlighted separately, one containing extracts from text1 and the other from text2. """

def show_differences_combined(text1, text2):
    import difflib

    if text1 == text2:
        return ''

    words1 = text1.split()
    words2 = text2.split()

    sm = difflib.SequenceMatcher(None, words1, words2)
    opcodes = sm.get_opcodes()

    if len(words1) <= 10 or len(words2) <= 10:
        # Return full text with changes highlighted
        result_words = []
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                result_words.extend(words1[i1:i2])
            elif tag == 'replace':
                result_words.append('~~' + ' '.join(words1[i1:i2]) + '~~')
                result_words.append('**' + ' '.join(words2[j1:j2]) + '**')
            elif tag == 'delete':
                result_words.append('~~' + ' '.join(words1[i1:i2]) + '~~')
            elif tag == 'insert':
                result_words.append('**' + ' '.join(words2[j1:j2]) + '**')
        return ' '.join(result_words)
    else:
        # Process differences with context and ellipsis
        diff_blocks = _get_diff_blocks(opcodes)

        result_words = []
        prev_a_end = 0

        for diff_block in diff_blocks:
            a_start = diff_block['a_start']
            a_end = diff_block['a_end']
            b_start = diff_block['b_start']
            b_end = diff_block['b_end']

            # Context start and end
            context_start = max(a_start - 2, prev_a_end)
            context_end = min(a_end + 2, len(words1))

            # Before the context start, skipped words
            if context_start > prev_a_end:
                if prev_a_end != 0:
                    result_words.append('...')
                result_words.append('...')

            # Append context before difference
            context_before_diff = words1[context_start:a_start]
            result_words.extend(context_before_diff)

            # Append difference
            diff_a_words = words1[a_start:a_end]
            diff_b_words = words2[b_start:b_end]
            if diff_a_words:
                result_words.append('~~' + ' '.join(diff_a_words) + '~~')
            if diff_b_words:
                result_words.append('**' + ' '.join(diff_b_words) + '**')

            # Append context after difference
            context_after_diff = words1[a_end:context_end]
            result_words.extend(context_after_diff)

            prev_a_end = context_end

        # After last diff_block
        if prev_a_end < len(words1):
            remaining_words = words1[prev_a_end:]
            if remaining_words:
                result_words.append('...')
                if result_words[-1] != '...':
                    result_words.append('...')

        # Remove duplicate '...' if any
        final_result_words = _remove_duplicate_ellipses(result_words)

        return ' '.join(final_result_words)

def show_differences_separate(text1, text2):
    import difflib

    if text1 == text2:
        return ['', '']

    words1 = text1.split()
    words2 = text2.split()

    sm = difflib.SequenceMatcher(None, words1, words2)
    opcodes = sm.get_opcodes()

    if len(words1) <= 10 or len(words2) <= 10:
        # Return full texts with changes highlighted separately
        result_words1 = []
        result_words2 = []
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                result_words1.extend(words1[i1:i2])
                result_words2.extend(words2[j1:j2])
            elif tag == 'replace':
                result_words1.append('~~' + ' '.join(words1[i1:i2]) + '~~')
                result_words2.append('**' + ' '.join(words2[j1:j2]) + '**')
            elif tag == 'delete':
                result_words1.append('~~' + ' '.join(words1[i1:i2]) + '~~')
            elif tag == 'insert':
                result_words2.append('**' + ' '.join(words2[j1:j2]) + '**')
        return [' '.join(result_words1), ' '.join(result_words2)]
    else:
        # Process differences with context and ellipsis
        diff_blocks = _get_diff_blocks(opcodes)

        result_words1 = []
        result_words2 = []
        prev_a_end = 0
        prev_b_end = 0

        for diff_block in diff_blocks:
            a_start = diff_block['a_start']
            a_end = diff_block['a_end']
            b_start = diff_block['b_start']
            b_end = diff_block['b_end']

            # Context start and end for text1
            context_start_a = max(a_start - 2, prev_a_end)
            context_end_a = min(a_end + 2, len(words1))

            # Context start and end for text2
            context_start_b = max(b_start - 2, prev_b_end)
            context_end_b = min(b_end + 2, len(words2))

            # Before the context start, skipped words
            if context_start_a > prev_a_end:
                if prev_a_end != 0:
                    result_words1.append('...')
                result_words1.append('...')
            if context_start_b > prev_b_end:
                if prev_b_end != 0:
                    result_words2.append('...')
                result_words2.append('...')

            # Append context before difference
            context_before_diff_a = words1[context_start_a:a_start]
            context_before_diff_b = words2[context_start_b:b_start]
            result_words1.extend(context_before_diff_a)
            result_words2.extend(context_before_diff_b)

            # Append difference
            diff_a_words = words1[a_start:a_end]
            diff_b_words = words2[b_start:b_end]
            if diff_a_words:
                result_words1.append('~~' + ' '.join(diff_a_words) + '~~')
            if diff_b_words:
                result_words2.append('**' + ' '.join(diff_b_words) + '**')

            # Append context after difference
            context_after_diff_a = words1[a_end:context_end_a]
            context_after_diff_b = words2[b_end:context_end_b]
            result_words1.extend(context_after_diff_a)
            result_words2.extend(context_after_diff_b)

            prev_a_end = context_end_a
            prev_b_end = context_end_b

        # After last diff_block
        if prev_a_end < len(words1):
            remaining_words1 = words1[prev_a_end:]
            if remaining_words1:
                result_words1.append('...')
                if result_words1[-1] != '...':
                    result_words1.append('...')
        if prev_b_end < len(words2):
            remaining_words2 = words2[prev_b_end:]
            if remaining_words2:
                result_words2.append('...')
                if result_words2[-1] != '...':
                    result_words2.append('...')

        # Remove duplicate '...' if any
        final_result_words1 = _remove_duplicate_ellipses(result_words1)
        final_result_words2 = _remove_duplicate_ellipses(result_words2)

        return [' '.join(final_result_words1), ' '.join(final_result_words2)]

def _get_diff_blocks(opcodes):
    # Identify blocks of differences considering proximity
    diff_blocks = []
    current_block = None

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            if current_block is not None:
                length = i2 - i1
                if length < 5:
                    # Include equal block in current_block
                    current_block['a_end'] = i2
                    current_block['b_end'] = j2
                else:
                    # Close current_block
                    diff_blocks.append(current_block)
                    current_block = None
            else:
                pass
        else:
            # tag is 'replace', 'delete', 'insert'
            if current_block is None:
                # Start new current_block
                current_block = {'a_start': i1, 'a_end': i2, 'b_start': j1, 'b_end': j2}
            else:
                # Extend current_block
                current_block['a_end'] = i2
                current_block['b_end'] = j2

    # After processing all opcodes, check for unfinished block
    if current_block is not None:
        diff_blocks.append(current_block)

    return diff_blocks

def _remove_duplicate_ellipses(words_list):
    final_result_words = []
    prev_word = None
    for word in words_list:
        if word == '...' and prev_word == '...':
            continue
        final_result_words.append(word)
        prev_word = word
    return final_result_words
