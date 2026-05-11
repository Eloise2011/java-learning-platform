#!/usr/bin/env python3
"""Generate the complete index.html with properly escaped JavaScript."""
import json, re

# Read all the part files that are still available
# Actually the parts were deleted. Let me read the current (broken) index.html
# and fix it properly.

with open('index.html', 'r') as f:
    content = f.read()

# Strategy: Instead of trying to fix the corrupted quiz strings with regex,
# convert ALL remaining single-quoted strings that are inside the quiz data
# to use double-quote delimiters, escaping any internal double quotes.

# Find the script section
script_start = content.find('<script>') + len('<script>')
script_end = content.find('</script>')
before = content[:script_start]
js_code = content[script_start:script_end]
after = content[script_end:]

# APPROACH: Find the curriculum array (between 'const curriculum = [' and the closing '];')
# and within it, convert quiz string delimiters from single quotes to double quotes.
# This handles apostrophes naturally.

# We need to process the curriculum JS carefully.
# Find start and end of curriculum
curr_start = js_code.find('const curriculum = [')
app_start = js_code.find('// ============ APPLICATION STATE ============')

# We'll work character by character to properly handle string boundaries
# For quiz field values that are single-quoted strings containing apostrophes,
# change the delimiter from ' to " and escape any " inside.

# Actually, let's take a simpler approach:
# 1. Find all patterns like: question: '...', or explanation: '...'
# 2. If the content between outer ' has an apostrophe (inner '),
#    change outer ' to ` (backtick)

# The challenge is matching the content correctly when it contains '
# Pattern: explanation: '<content>' followed by space+} or ,}
# Non-greedy match won't work if content has '

# NEW APPROACH: Use a character-by-character scanner to find strings
# This is more reliable than regex for nested quotes

result = []
i = 0
in_curriculum = False
fixes = 0

while i < len(js_code):
    # Check if we've entered/exited the curriculum
    if not in_curriculum and js_code[i:i+len('const curriculum = [')] == 'const curriculum = [':
        in_curriculum = True

    if in_curriculum:
        # Check for quiz string patterns: question: ', explanation: ', options: [', hint: ', instruction: '
        prefixes = ["question: '", "explanation: '", "hint: '", "instruction: '"]
        matched = None
        for p in prefixes:
            if js_code[i:i+len(p)] == p:
                matched = p
                break

        if matched:
            # Found a single-quoted string. Find the closing ' that ends this string.
            # The closing ' is followed by ' ,' or ' }'
            result.append(matched)
            i += len(matched)
            content_start = i

            # Find the END of this string by looking for a ' followed by space and , or }
            pos = i
            while pos < len(js_code):
                if js_code[pos] == "'":
                    # Check what follows
                    after_str = js_code[pos+1:pos+3].strip() if pos+1 < len(js_code) else ''
                    next_chars = js_code[pos+1:pos+4] if pos+3 < len(js_code) else ''
                    # Closing ' is followed by , or } or space+} or space+,
                    if next_chars.startswith(',') or next_chars.startswith(' }') or next_chars.startswith('],') or next_chars.startswith('] }'):
                        # This is the closing quote
                        inner = js_code[content_start:pos]
                        if "'" in inner:
                            # Has apostrophe - change to backtick
                            result.append('`' + inner + '`')
                            fixes += 1
                        else:
                            # No apostrophe - keep as single quote
                            result.append("'" + inner + "'")
                        i = pos + 1
                        break
                pos += 1
            else:
                # No closing quote found - copy remaining as-is
                result.append(js_code[i:])
                break
            continue

        # Handle options arrays
        if js_code[i:i+10] == "options: [":
            result.append("options: [")
            i += 10
            # Process array elements
            while i < len(js_code) and js_code[i] != ']':
                if js_code[i] == "'":
                    # Start of a single-quoted option
                    content_start = i + 1
                    pos = content_start
                    while pos < len(js_code):
                        if js_code[pos] == "'":
                            next_ch = js_code[pos+1:pos+2] if pos+1 < len(js_code) else ''
                            if next_ch in (',', ']'):
                                inner = js_code[content_start:pos]
                                if "'" in inner:
                                    result.append('`' + inner + '`')
                                    fixes += 1
                                else:
                                    result.append("'" + inner + "'")
                                i = pos + 1
                                break
                        pos += 1
                    else:
                        result.append(js_code[i])
                        i += 1
                else:
                    result.append(js_code[i])
                    i += 1
            continue

    result.append(js_code[i])
    i += 1

fixed_js = ''.join(result)
print(f"Fixed {fixes} strings with apostrophes")

# Assemble the final file
final = before + fixed_js + after
with open('index.html', 'w') as f:
    f.write(final)

# Verify with node
script_start = final.find('<script>') + len('<script>')
script_end = final.find('</script>')
with open('/tmp/test-final.js', 'w') as f:
    f.write(final[script_start:script_end])

import subprocess
r = subprocess.run(['node', '--check', '/tmp/test-final.js'], capture_output=True, text=True, timeout=10)
if r.returncode == 0:
    print("JS syntax VALID!")
else:
    lines = r.stderr.split('\n')
    for line in lines[:5]:
        print(line)

print("Done")
