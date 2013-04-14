import os.path

CLIENT_ID = 'd968b2b8df7f127'


def upload(image):  # image could be 'path' , 'file' or 'image data'
    try:
        import requests
    except ImportError:
        print "moudle requests not found"
        print "try 'pip install requests' to install"
        raise ImportError
    url = "https://api.imgur.com/3/upload"
    headers = {'Authorization': 'Client-ID %s' % CLIENT_ID}
    if isinstance(image, str):
        image_data = open(image, 'rb').read()
    elif isinstance(image, file):
        image_data = image.read()
    else:
        image_data = image
    files = {'image': image_data}

    response = requests.post(url, headers=headers, files=files, verify=False)
    result = response.json()
    if result.get('status'):
        link = result.get('data').get('link')
        base, ext = os.path.splitext(link)
        return (link, base + 'l' + ext)
        #return {
        #    'origin': link,
        #    'small': base + 's' + ext,
        #    'large': base + 'l' + ext,
        #}


if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-u', '--upload', dest='upload', metavar='FILE',
                      help="upload file to imgur.com")

    opts, args = parser.parse_args()
    if opts.upload:
        print upload(opts.upload)
    else:
        parser.print_help()
