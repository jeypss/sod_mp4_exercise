import click

valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

while True:
    # click.echo('Continue? [yn] ', nl=False)
    c = click.getchar()
    hex_c = ''.join(['\\' + hex(ord(i))[1:] if i not in valid_chars else i for i in c])
    # click.echo()
    if c == 'y':
        click.echo('We will go on')
    elif c == 'n':
        click.echo('Abort!')
        break
    elif c == '\xe0K':
        click.echo('Left arrow <-')
    elif c == '\xe0M':
        click.echo('Right arrow ->')
    elif hex_c == r'\xd':
        click.echo('enter')
    else:
        click.echo('Invalid input :(')
        print(c)
        print(hex_c)
        click.echo('You pressed: "' + hex_c + '"')
