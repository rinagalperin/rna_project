def table2list(table):
    """
        Convert a <table> into a <ul>.
        Each cell, <td>, gets converted into a list item <li>, as follows:
        1) <table border="1"> --> <ul>, </table> --> </ul>
        2) <th>, </th>, <tbody>, </tbody> --> delete
        3) <tr>, <td> --> <li>, </tr>, </td> --> </li>
        """
    list = table\
        .replace('<table border="1">', '<ul>')\
        .replace('</table>', '</ul>')\
        .replace('<tr>', '<li>')\
        .replace('</tr>', '</li>')\
        .replace('<td>', ':   ')\
        .replace('</td>', '')\
        .replace('<th>', '')\
        .replace('</th>', '')\
        .replace('<tbody>', '')\
        .replace('</tbody>', '')

    style = '<style>\
                ul {\
                  list-style: none;\
                  color: black;\
                }\
                li::before {\
                  content: \"\2022\";\
                  color: black;\
                  font-weight: bold;\
                  display: inline-block;\
                  width: 1em;\
                  margin-left: -1em;\
                }</style>'

    list_with_style = list# + style

    return list_with_style
