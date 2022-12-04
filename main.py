from PyPDF2 import PdfFileReader, PdfFileWriter

OFFSET = 7


def get_bookmark_data():
    bookmarks = []
    with open('in.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line == '':
                continue

            top_level = False
            if line.startswith('$ '):
                line = line.replace('$ ', '')
                top_level = True

            page_number = line.split(' ')[-1]
            title = line[:-len(page_number) - 1]

            if title.startswith('PERIOD') or top_level:
                parent = bookmarks
            else:
                if title.startswith('Chapter') or title.startswith('Period'):
                    parent = bookmarks[-1]['children']
                else:
                    parent = bookmarks[-1]['children'][-1]['children']

            parent.append({
                'title': title,
                'page': int(page_number),
                'children': []
            })
    return bookmarks


def add_bookmarks(bookmarks, parent=None):
    for bookmark_to_create in bookmarks:
        bookmark = writer.addBookmark(
            bookmark_to_create['title'], bookmark_to_create['page'] + OFFSET - 2, parent=parent)
        add_bookmarks(bookmark_to_create['children'], parent=bookmark)


if __name__ == '__main__':
    b = get_bookmark_data()
    print('Finished reading bookmarks')
    reader = PdfFileReader("AMSCO 2016 Answer Key.pdf")  # open input
    writer = PdfFileWriter()  # open output

    for page in reader.pages:
        writer.addPage(page)

    writer.add_metadata({
        '/Title': 'AMSCO 2016',
        '/Author': 'John Newman and John Schmalbach',
        '/Subject': 'AP United States History',
        '/Keywords': 'AMSCO AP United States History 2016',
        '/Creator': 'AMSCO',
        '/Producer': 'AMSCO School Publications, Inc.',
        '/CreationDate': 'D:20161001000000Z',
        '/ModDate': 'D:20161001000000Z',
        '/Trapped': '/False'
    })

    print('Finished copying pages')

    add_bookmarks(b)
    print('Finished adding bookmarks')

    with open("result.pdf", "wb") as fp:  # creating result pdf JCT
        writer.write(fp)  # writing to result pdf JCT
    print('Finished writing to file')