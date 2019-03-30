from bs4 import BeautifulSoup, Tag, BeautifulStoneSoup


def table2ul(content, flatten_rows=False):
    """
    Convert a <table> into a <ul>.
    Each cell, <td>, gets converted into a list item <li> unless
    the flatten_rows paramter is given. In this case, all content from
    a table row, <tr>, gets converted into a list item.
    """
    soup = BeautifulSoup(content, 'html.parser')

    for table in soup.findAll('table'):
        ul = Tag(soup, 'ul')

        if flatten_rows:
            for row in table.findAll('tr'):
                li = Tag(soup, 'li')
                for cell in row.findAll('td'):
                    li.contents.extend(cell.contents)
                ul.append(li)
        else:
            for cell in table.findAll('td'):
                li = Tag(soup, 'li')
                li.contents = cell.contents
                ul.append(li)
        table.replaceWith(ul)

    return soup.prettify()