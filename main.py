from pypdf import PdfReader, PdfWriter

# page marked 1
OFFSET = 17
INPUT_FILE = "in.pdf"
TITLE = "Calculus With Concepts in Calculus"
AUTHOR = ""
CASE_TITLE = False

with open("ignore.txt", "r", encoding="utf-8") as f:
    ignore = f.read().splitlines()


def case(title):
    arr = title.lower().split(" ")
    return " ".join([word.capitalize() for word in arr if word not in ignore])


def get_bookmark_data():
    with open("in.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    line_idx = 0

    def get_indent_level(line):
        indent_level = 0
        for char in line:
            if char == " ":
                indent_level += 1
            else:
                break

        indent_level = indent_level // 4
        return indent_level

    def parse_line(line):
        line = line.strip()
        page_number = line.split(" ")[-1]
        title = line[: -len(page_number) - 1].strip()
        if CASE_TITLE:
            title = case(title)

        return title, int(page_number)

    def parse_bookmarks(level=0):
        bookmarks = []

        nonlocal line_idx

        while line_idx < len(lines):
            line = lines[line_idx]

            if line == "":
                line_idx += 1
                continue

            indent_level = get_indent_level(line)

            title, page_number = parse_line(line)

            bookmark = {"title": title, "page": page_number, "children": []}

            # hacky nesting logic
            if indent_level == level:
                bookmarks.append(bookmark)
            elif indent_level > level:
                children = parse_bookmarks(level=indent_level)
                bookmarks[-1]["children"].extend(children)
            elif indent_level < level:
                line_idx -= 1
                return bookmarks

            line_idx += 1

        return bookmarks

    return parse_bookmarks()


def add_bookmarks(writer, bookmarks, parent=None):
    for bookmark_to_create in bookmarks:
        bookmark = writer.add_outline_item(
            bookmark_to_create["title"],
            bookmark_to_create["page"] + OFFSET - 2,
            parent=parent,
        )
        add_bookmarks(writer, bookmark_to_create["children"], parent=bookmark)


if __name__ == "__main__":
    b = get_bookmark_data()
    print("Finished reading bookmarks")
    reader = PdfReader(INPUT_FILE)  # open input
    writer = PdfWriter()  # open output

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(
        {
            "/Title": TITLE,
            "/Author": AUTHOR,
        }
    )

    print("Finished copying pages")

    add_bookmarks(writer, b)
    print("Finished adding bookmarks")

    with open("result.pdf", "wb") as fp:  # creating result pdf JCT
        writer.write(fp)  # writing to result pdf JCT
    print("Finished writing to file")
