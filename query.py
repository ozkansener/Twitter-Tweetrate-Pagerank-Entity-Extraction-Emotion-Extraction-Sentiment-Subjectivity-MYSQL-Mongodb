import csv
import sys


def get_file():

    file = input('Filename: ')
    return file

def get_headers(csv_file):

    """
    Read in the CSV and extract the column names. Strip
    any whitespace, replace spaces underscore and make lowercase.

    """

    try:
        with open (csv_file, newline='') as f:
            reader = csv.reader(f)
            header_row = next(reader)
            headers = []
            for i in header_row:
                i = i.strip().replace(' ', '_').lower()
                headers.append(i)
            headers_minus_last = headers[:-1]
            last_header = headers[-1]
        return headers, headers_minus_last, last_header
    except FileNotFoundError as e:
        print('Sorry! The file cannot be found.')
        return
    except:
        print('An error has occured.', sys.exc_info()[0])
        return

def create_table_lines(tbl_nm, headers_minus_last, last_header):

    """
    Create the SQL commands that will be used to create the database table.
    This includes the column name from the first row of the CSV file and
    the column type (VARCHAR).

    """

    column_type = 'VARCHAR(255)'

    try:
        lines_to_write_table = []
        lines_to_write_table.append('CREATE TABLE {}\n('.format(tbl_nm))

        for i in headers_minus_last:
            lines_to_write_table.append(i + ' {},'.format(column_type))
        lines_to_write_table.append(last_header + ' {}'.format(column_type) + '\n);\n')
        return lines_to_write_table
    except:
        print('An error has occured.', sys.exc_info()[0])
        return


def create_data_lines(csv_file, tbl_nm, hdrs):

    """
    Create the SQL commands that will be used to load the data from the
    CSV file into the database table.

    """

    try:
        field_terminator = "','"
        line_terminator = "'\\r\\n'"
        enclosed_by = "'\"'"
        ignore_lines = '1'
        lines_to_write_data_load = []
        lines_to_write_data_load.append('LOAD DATA LOCAL INFILE {}'.format(csv_file))
        lines_to_write_data_load.append('INTO TABLE {}'.format(tbl_nm))
        lines_to_write_data_load.append('FIELDS TERMINATED BY {}'.format(field_terminator))
        lines_to_write_data_load.append('ENCLOSED BY {}'.format(enclosed_by))
        lines_to_write_data_load.append('LINES TERMINATED BY {}'.format(line_terminator))
        lines_to_write_data_load.append('IGNORE {} LINES'.format(ignore_lines))
        lines_to_write_data_load.append('(')
        for i in hdrs[:-1]:
            lines_to_write_data_load.append(i + ',')
        lines_to_write_data_load.append(hdrs[-1] + '\n);')
        return lines_to_write_data_load
    except:
        print('An error has occured.', sys.exc_info()[0])
        return


def write_lines_to_file(csv_file, tbl_nm, tbl_lines, data_lines):

    """
    Write the SQL statements to file.

    """

    try:
        with open (tbl_nm + '.sql', 'w') as f:
            for i in tbl_lines:
                f.write(i + '\n')
            for i in data_lines:
                f.write(i + '\n')
        print('Success! Results output to {}.sql'.format(tbl_nm))
    except:
        print('An error has occured.', sys.exc_info()[0])
        return


def main():

    try:
        file = get_file()
        table_name = file.split('.')[0]
        headers, headers_minus_last, last_header = get_headers(file)
        lines_to_write_table = create_table_lines(table_name, headers_minus_last, last_header)
        lines_to_write_data_load = create_data_lines(file, table_name, headers)

        get_headers(file)
        create_table_lines(table_name, headers_minus_last, last_header)
        create_data_lines(file, table_name, headers)
        write_lines_to_file(file, table_name, lines_to_write_table, lines_to_write_data_load)
    except:
        return


if __name__ == '__main__':
    main()
